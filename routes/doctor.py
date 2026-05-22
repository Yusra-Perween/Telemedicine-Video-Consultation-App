from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models import Appointment

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/complete/<int:appointment_id>')
def complete_appointment(appointment_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    appointment = Appointment.query.get(appointment_id)
    if appointment:
        appointment.status = 'completed'
        db.session.commit()
        flash('Appointment marked as completed!', 'success')

    return redirect(url_for('patient.dashboard'))
