from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models import Appointment, Doctor, User, Payment
from datetime import datetime
import stripe
import config

stripe.api_key = config.STRIPE_SECRET_KEY

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session['role']

    if role == 'patient':
        appointments = Appointment.query.filter_by(patient_id=user_id).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
        # the template expects tuples like a.id, a.patient_id, u.name as doctor_name, a.appointment_date, a.appointment_time, a.status
        # We need to map the objects to tuples for backwards compatibility with the templates, or change the templates.
        # Let's map to tuples so we don't have to rewrite templates yet.
        appointment_data = [
            (a.id, a.patient_id, a.doctor_profile.user.name, a.appointment_date, a.appointment_time, a.status)
            for a in appointments
        ]
        return render_template('dashboard.html', appointments=appointment_data)
    elif role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            flash('Doctor profile not found', 'danger')
            return redirect(url_for('auth.login'))
        
        appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
        appointment_data = [
            (a.id, a.doctor_id, a.patient.name, a.appointment_date, a.appointment_time, a.status)
            for a in appointments
        ]
        return render_template('dashboard.html', appointments=appointment_data)
    else:
        return redirect(url_for('auth.login'))

@patient_bp.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        session['temp_appointment'] = {
            'doctor_id': request.form['doctor_id'],
            'appointment_date': request.form['date'],
            'appointment_time': request.form['time']
        }
        return redirect(url_for('patient.payment_page'))

    # The template expects tuples: id, name, specialization, bio
    approved_doctors = Doctor.query.filter_by(approval_status='approved').all()
    doctor_data = [
        (d.id, d.user.name, d.specialization, d.bio)
        for d in approved_doctors
    ]
    return render_template('book_appointment.html', doctors=doctor_data)

@patient_bp.route('/payment')
def payment_page():
    if 'temp_appointment' not in session:
        return redirect(url_for('patient.book_appointment'))
        
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000, # $20.00
                        'product_data': {
                            'name': 'Doctor Consultation',
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.url_root + 'payment_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.url_root + 'dashboard',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(f'Payment error: {str(e)}', 'danger')
        return redirect(url_for('patient.book_appointment'))

@patient_bp.route('/payment_success')
def payment_success():
    session_id = request.args.get('session_id')
    if not session_id or 'temp_appointment' not in session:
        flash('Invalid session or session expired', 'danger')
        return redirect(url_for('patient.book_appointment'))

    try:
        # Verify payment with Stripe
        stripe_session = stripe.checkout.Session.retrieve(session_id)
        if stripe_session.payment_status != 'paid':
            flash('Payment was not successful', 'danger')
            return redirect(url_for('patient.dashboard'))
    except Exception as e:
        flash(f'Payment verification error: {str(e)}', 'danger')
        return redirect(url_for('patient.dashboard'))

    temp_data = session.pop('temp_appointment')
    
    new_appointment = Appointment(
        patient_id=session['user_id'],
        doctor_id=temp_data['doctor_id'],
        appointment_date=datetime.strptime(temp_data['appointment_date'], '%Y-%m-%d').date(),
        appointment_time=datetime.strptime(temp_data['appointment_time'], '%H:%M').time(),
        status='booked'
    )
    db.session.add(new_appointment)
    db.session.flush()

    new_payment = Payment(
        appointment_id=new_appointment.id,
        stripe_payment_id=session_id,
        amount=2000,
        status='completed'
    )
    db.session.add(new_payment)
    db.session.commit()

    flash('Appointment booked and paid successfully!', 'success')
    return redirect(url_for('patient.dashboard'))

@patient_bp.route('/cancel/<int:appointment_id>')
def cancel_appointment(appointment_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.status = 'cancelled'
        db.session.commit()
        flash('Appointment cancelled!', 'success')
    return redirect(url_for('patient.dashboard'))

@patient_bp.route('/video_consultation/<int:appointment_id>')
def video_consultation(appointment_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('patient.dashboard'))

    return render_template('video_call.html', appointment_id=appointment_id)
