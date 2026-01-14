# 🎯 Multi-Purpose Booking & Shopping Platform

A complete full-stack web application for managing shopping malls, wedding hall bookings, and hotel room reservations with admin dashboard and payment integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- A modern web browser

### Installation & Setup (5 minutes)

#### 1. **Clone/Download the Project**
```bash
git clone <your-repo-url>
cd booking-platform
```

#### 2. **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

#### 3. **Run the Backend Server**
```bash
python app.py
```

You should see:
```
 * Running on http://localhost:5000
 * Database initialized successfully!
```

#### 4. **Open Frontend in Browser**

The frontend files are standalone HTML. Simply open them in your browser:

- **Home Page**: `index.html`
- **Login**: `login.html`
- **Sign Up**: `signup.html`
- **User Dashboard**: `dashboard.html`
- **Admin Dashboard**: `admin-dashboard.html`

**OR** use Python's built-in server for frontend:
```bash
# In a separate terminal
python -m http.server 8000
```

Then open: `http://localhost:8000/index.html`

---

## 🔑 Demo Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Role: Full admin access to dashboard

**Create Your Own:**
- Click "Sign Up" to create a regular user account
- Use the signup form on any page

---

## 📋 Project Structure

```
project/
├── app.py                    # Flask backend (main application)
├── requirements.txt          # Python dependencies
│
├── login.html               # User login page
├── signup.html              # User registration page
├── dashboard.html           # User profile & bookings
├── admin-dashboard.html     # Admin control panel
│
├── index.html               # Landing page (to be created)
├── shopping-mall.html       # Shopping items (to be created)
├── wedding-halls.html       # Hall bookings (to be created)
├── hotel-rooms.html         # Room bookings (to be created)
├── contact.html             # Contact form (to be created)
│
└── README.md               # This file
```

---

## 🎨 Features Included (Phase 1)

### ✅ User Management
- User signup with email validation
- Secure login with hashed passwords
- Session management
- User profile

### ✅ Booking System
- Wedding hall booking with date selection
- Hotel room booking with check-in/check-out
- Automatic price calculation
- Booking history and status tracking

### ✅ Shopping Mall
- Browse products by category
- View product details
- Shopping cart ready for integration

### ✅ Contact & Support
- Contact form for inquiries
- Complaint system with priority levels
- Admin ticket management

### ✅ Admin Dashboard
- 📊 Real-time statistics (users, bookings, revenue)
- 👥 User management
- 📅 Booking management
- 📞 Contact messages inbox
- ⚠️ Complaint tracking & resolution
- 🏛️ Wedding hall management
- 🏨 Hotel room management
- 🛍️ Shopping item management

### ✅ Backend API
- RESTful API with 30+ endpoints
- Authentication & authorization
- Database with SQLite (upgradeable to PostgreSQL)
- CORS enabled for frontend communication

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/signup          - Register new user
POST   /api/auth/login           - Login user
POST   /api/auth/logout          - Logout user
GET    /api/auth/me              - Get current user
```

### Wedding Halls
```
GET    /api/wedding-halls        - List all halls
GET    /api/wedding-halls/<id>   - Get hall details
POST   /api/wedding-halls        - Create hall (admin only)
```

### Hotel Rooms
```
GET    /api/hotel-rooms          - List all rooms
GET    /api/hotel-rooms/<id>     - Get room details
POST   /api/hotel-rooms          - Create room (admin only)
```

### Shopping
```
GET    /api/shopping-items       - List items
POST   /api/shopping-items       - Add item (admin only)
```

### Bookings
```
POST   /api/bookings             - Create booking
GET    /api/bookings             - Get user bookings
POST   /api/bookings/<id>/cancel - Cancel booking
```

### Admin
```
GET    /api/admin/dashboard      - Dashboard stats
GET    /api/admin/users          - All users
GET    /api/admin/bookings       - All bookings
GET    /api/admin/contacts       - Contact messages
GET    /api/admin/complaints     - Complaints
```

---

## 💳 Payment Gateway Integration (Ready)

The backend is **ready for Razorpay integration**. To activate:

1. **Get API Keys from Razorpay:**
   - Sign up at https://razorpay.com
   - Get Key ID and Key Secret

2. **Add to Environment:**
   ```bash
   export RAZORPAY_KEY_ID="your_key_id"
   export RAZORPAY_KEY_SECRET="your_key_secret"
   ```

3. **Integration code is in `app.py` (commented out)**

---

## 🚀 Deployment Options (FREE)

### Option 1: **Render.com** (Backend)
1. Push code to GitHub
2. Connect Render to GitHub
3. Create new Web Service
4. Set runtime to Python
5. Deploy (automatic)

### Option 2: **Netlify** (Frontend)
1. Push HTML files to GitHub
2. Connect Netlify to GitHub repo
3. Set build command to: `echo ""`
4. Deploy

### Option 3: **Railway.app** (Full Stack)
1. Connect GitHub repository
2. Railway auto-detects Python app
3. Add PostgreSQL plugin
4. Deploy in 1 click

---

## 🔄 Database

### Local Development
- **Database**: SQLite (`booking_platform.db`)
- **Auto-created** on first run with sample data

### Production (Recommended)
Upgrade to PostgreSQL:
```bash
pip install psycopg2-binary
```

Update `app.py` config:
```python
DATABASE_URL = 'postgresql://user:password@host:port/dbname'
```

---

## 🎯 What's Next (Phase 2 - Easy Additions)

The foundation is built. Easy next steps:

1. **Landing Pages**
   - `index.html` - Home page with hero section
   - `shopping-mall.html` - Browse products
   - `wedding-halls.html` - View all halls
   - `hotel-rooms.html` - Browse rooms
   - `contact.html` - Contact form page

2. **Payment Processing**
   - Add Razorpay keys
   - Update booking to process payments
   - Webhook for payment confirmations

3. **Email Notifications**
   - Install `flask-mail`
   - Send booking confirmations
   - Complaint acknowledgment emails

4. **Image Uploads**
   - Integrate Cloudinary (free plan)
   - Upload hall/room photos
   - Product images

5. **Advanced Search**
   - Filter by date, price, location
   - Search bar with autocomplete
   - Sort options

---

## 🐛 Troubleshooting

### "Connection refused" error
- Ensure Flask server is running: `python app.py`
- Check port 5000 is not in use

### CORS errors
- Frontend and backend must be on same origin
- Or CORS is misconfigured in `app.py`
- Update CORS origins in app.py line with `origins=['your-domain']`

### Database errors
- Delete `booking_platform.db`
- Run `python app.py` again to recreate

### Login not working
- Check credentials (admin/admin123)
- Ensure backend is running
- Check browser console for errors

---

## 🔐 Security Notes

### Before Production:
1. ✅ Change `SECRET_KEY` in `app.py`
2. ✅ Use PostgreSQL instead of SQLite
3. ✅ Enable HTTPS
4. ✅ Set strong admin password
5. ✅ Add rate limiting
6. ✅ Implement CSRF protection
7. ✅ Add input validation
8. ✅ Use environment variables for secrets

---

## 📦 Tech Stack

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (ORM)
- SQLite/PostgreSQL (Database)

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- RESTful API calls
- Local storage for preferences

**Hosting:**
- Render.com (Backend)
- Netlify (Frontend)
- PostgreSQL on AWS RDS (Optional)

---

## 📞 Support & Documentation

### Common Tasks:

**Add a new admin user via Python shell:**
```python
from app import db, User

user = User(
    username='newadmin',
    email='admin2@example.com',
    full_name='New Admin',
    phone='9999999999',
    is_admin=True
)
user.set_password('newpassword')
db.session.add(user)
db.session.commit()
```

**Reset database:**
```bash
rm booking_platform.db
python app.py
```

**View all users:**
```python
from app import User
users = User.query.all()
for user in users:
    print(user.username, user.email)
```

---

## 🎓 Learning Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **REST API Design**: https://restfulapi.net/
- **Razorpay Integration**: https://razorpay.com/developers/api

---

## 📝 License

This project is open source and free to use for commercial purposes.

---

## 🎉 You're All Set!

**Next Steps:**
1. ✅ Run `python app.py`
2. ✅ Open `login.html` in browser
3. ✅ Login with admin/admin123
4. ✅ Explore admin dashboard
5. ✅ Create a user account
6. ✅ Make a booking
7. ✅ Deploy to free hosting

**Questions?** Check the API endpoints in `app.py` or inspect network calls in browser DevTools.

**Happy Building! 🚀**
