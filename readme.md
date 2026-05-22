# 🏥 Hospital System – Video Calling with Doctors

A complete Flask + MySQL telemedicine web application where patients can book appointments, make payments, video consultations and chat in real-time with doctors.

## 👩‍💻 Developed By
**Yusra Perween**

## 🚀 Features

### 👤 Authentication
- Patient & Doctor Registration  
- Secure Login / Logout  
- Role-based Dashboard  

### 📅 Appointment System
- Patients can book appointments  
- Doctors can view appointments  
- Cancel & Complete appointment feature  

### 💳 Payment Gateway (Demo)
- Fake payment page (Stripe removed)  
- Payment recorded in database  
- Appointment confirmed after payment  

### 🎥 Video Consultation
- Start video call after booking  
- Camera + microphone access  
- WebRTC consultation  

### 💬 Live Chat During Video Call ⭐
- Real-time chat using Flask-SocketIO  
- Instant messaging between doctor & patient during video call  

---

## 🗄️ Database
MySQL database stores:

- Users  
- Doctors  
- Appointments  
- Payments  

---

## 🛠️ Tech Stack

| Technology | Used |
|------------|------|
| Backend | Python Flask |
| Database | MySQL (XAMPP) |
| Frontend | HTML, CSS, JavaScript |
| Video Calling | WebRTC |
| Real-time Chat | Flask-SocketIO |

---

## 📂 Project Structure

Hospital-System-Video-Calling-with-Doctors  
│  
├── static/  
├── templates/  
├── app.py  
├── config.py  
├── database.sql  
├── requirements.txt  
└── README.md  

---

## ⚙️ How to Run This Project

### 🔹 Step 1 — Clone Repository

git clone https://github.com/Yusra-Perween/Hospital-System-Video-Calling-with-Doctors.git

cd Hospital-System-Video-Calling-with-Doctors


### 🔹 Step 2 — Start XAMPP
Open XAMPP Control Panel and start:

- Apache  
- MySQL  

Keep XAMPP running in the background.

---

### 🔹 Step 3 — Create the Database

Open browser and go to:


http://localhost/phpmyadmin


1. Click **New**  
2. Create database → **hospital_db**  
3. Open database → Click **Import**  
4. Import file → **database.sql**

---

### 🔹 Step 4 — Configure Database Connection

Open **config.py** and ensure:


MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "hospital_db"
MYSQL_PORT = 3306


---

### 🔹 Step 5 — Install Required Libraries

Open terminal inside project folder and run:


pip install -r requirements.txt


---

### 🔹 Step 6 — Run the Application


python app.py


You should see:


Running on http://127.0.0.1:5000/


---

### 🔹 Step 7 — Open in Browser


http://127.0.0.1:5000


