# 🏥 Hospital System – Telemedicine & Video Consultation App

A complete, modern Flask telemedicine web application featuring real-time WebRTC video consultations, secure Stripe payments, role-based dashboards, and cutting-edge AI-powered medical assistants.

## 👩‍💻 Developed By
**Yusra Perween**

---

## 🚀 Key Features

### 👤 Authentication & Security
- Patient & Doctor Registration
- Secure password hashing using `werkzeug.security`
- Role-based Access Control (Patient vs. Doctor dashboards)

### 📅 Appointment & Booking System
- Browse approved doctors
- Select available dates and times
- Dynamic dashboard rendering based on user role
- Cancel & Complete appointment feature

### 💳 Real Stripe Payment Integration
- Secure Stripe Checkout Sessions
- Payment verification before confirming appointments
- Seamless redirect flows

### 🎥 Real-Time WebRTC Video Consultation
- Built-in WebRTC peer-to-peer video calling
- `Flask-SocketIO` backend for fast, real-time signaling
- Native camera and microphone access with mute/video-off controls

### 🤖 AI-Powered Features (OpenAI)
- **AI Symptom Checker:** Patients describe symptoms and get immediate triage and specialist recommendations.
- **AI Report Summarizer:** Patients can paste complex medical reports to get plain-English summaries.
- **AI Doctor Notes Assistant:** Doctors type brief shorthand notes, and the AI expands them into professional clinical documentation.

---

## 🛠️ Tech Stack

| Technology | Used For |
|------------|----------|
| **Backend** | Python, Flask, Flask-SQLAlchemy, Flask-SocketIO |
| **Database** | SQLite (Plug-and-play, no external DB needed!) |
| **Frontend** | HTML5, Vanilla CSS, JavaScript, Jinja2 Templates |
| **Video Calling** | WebRTC (RTCPeerConnection), Socket.io |
| **Payments** | Stripe API |
| **Artificial Intelligence** | OpenAI GPT-3.5 API |

---

## ⚙️ How to Run This Project Locally

This project has been completely refactored to use **SQLite** and an **ORM**, meaning you **NO LONGER NEED XAMPP OR MYSQL**. It runs perfectly right out of the box!

### 🔹 Step 1 — Clone the Repository
```bash
git clone https://github.com/Yusra-Perween/Telemedicine-Video-Consultation-App.git
cd Telemedicine-Video-Consultation-App
```

### 🔹 Step 2 — Set Up Environment Variables
Rename `.env.example` to `.env` and fill in your keys:
```env
SECRET_KEY=your_secret_flask_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
OPENAI_API_KEY=your_openai_api_key
```

### 🔹 Step 3 — Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 🔹 Step 4 — Run the Application
Because this project uses Flask-SocketIO, start the app using:
```bash
python app.py
```
The database (`app.db`) and all tables will automatically be created on the first run.

### 🔹 Step 5 — Open in Browser
Visit **http://127.0.0.1:5000** and start testing!
