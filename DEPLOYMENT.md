# Deployment Guide - Complete Step-by-Step

## 🚀 Option 1: Deploy to Render.com (RECOMMENDED - FREE)

### Backend Deployment (Flask)

#### Step 1: Prepare Your Code
1. Create GitHub account (free at github.com)
2. Create new repository: `booking-platform`
3. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/booking-platform.git
git push -u origin main
```

#### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (free)
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Fill in settings:
   - **Name**: `booking-platform-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free tier

6. Add Environment Variables:
   ```
   SECRET_KEY = your-random-secret-key-here
   DATABASE_URL = sqlite:///booking_platform.db
   ```

7. Click "Create Web Service"
8. Wait 2-3 minutes for deployment
9. Copy the provided URL (e.g., `https://booking-platform-api.onrender.com`)

#### Step 3: Update Frontend
In all HTML files, change:
```javascript
const API_BASE = 'http://localhost:5000/api';
```

To:
```javascript
const API_BASE = 'https://booking-platform-api.onrender.com/api';
```

### Frontend Deployment (Netlify)

#### Step 1: Create HTML Files Folder
1. Create new GitHub repository: `booking-platform-web`
2. Push all HTML files (index.html, login.html, etc.)

#### Step 2: Deploy to Netlify
1. Go to https://netlify.com
2. Sign up with GitHub
3. Click "Add new site" → "Import an existing project"
4. Select your GitHub repository
5. Settings:
   - **Build command**: (leave empty)
   - **Publish directory**: `.` (current folder)

6. Click "Deploy site"
7. Wait for deployment to complete
8. Your site is now live! (e.g., `https://booking-platform-web.netlify.app`)

---

## 🚀 Option 2: Deploy to Railway.app (EASIEST - FREE)

### Full Stack Deployment

#### Step 1: Push to GitHub (same as above)

#### Step 2: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub"
5. Choose your repository
6. Railway auto-detects Python

#### Step 3: Configure
1. Add environment variables:
   - `FLASK_ENV` = production
   - `SECRET_KEY` = your-secret
   - `DATABASE_URL` = postgresql://... (if using PostgreSQL)

2. Railway automatically starts your app

#### Step 4: Get URL
- Your API will be available at Railway's provided URL
- Update frontend API_BASE accordingly

---

## 🚀 Option 3: Deploy with Vercel (Frontend Only)

1. Go to https://vercel.com
2. Import your GitHub repository
3. Select "Other" as framework
4. Deploy

---

## 💾 Database Upgrade (Production)

### From SQLite to PostgreSQL

#### Step 1: Create PostgreSQL Database
- Use AWS RDS (free tier)
- Or Render PostgreSQL add-on
- Or ElephantSQL (free 20MB)

#### Step 2: Update Configuration
In `app.py`, change:
```python
DATABASE_URL = 'postgresql://user:password@host:port/dbname'
```

#### Step 3: Install PostgreSQL Driver
```bash
pip install psycopg2-binary
```

#### Step 4: Migrate Data
```python
# Export from SQLite
sqlite3 booking_platform.db .dump > backup.sql

# Import to PostgreSQL
# Use pgAdmin or PostgreSQL client
```

---

## 🔐 Production Security Checklist

Before going live, ensure:

- [ ] Changed `SECRET_KEY` to random string
- [ ] Set `FLASK_ENV = production`
- [ ] Using PostgreSQL (not SQLite)
- [ ] HTTPS enabled (automatic on Render/Railway)
- [ ] CORS configured for your domains
- [ ] Admin password changed from default
- [ ] Environment variables set securely
- [ ] Database backups configured
- [ ] Error logging enabled
- [ ] Rate limiting added

---

## 🔄 Continuous Deployment

Both Render and Railway support automatic deployment:
- Push to GitHub main branch
- App automatically rebuilds and deploys
- Zero downtime deployments

---

## 📊 Monitoring

### Render
- Real-time logs in dashboard
- Metrics tab for CPU/Memory

### Railway
- Logs visible in dashboard
- Deployment history

### Setup Logging
Add to `app.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    logger.info(f'{request.method} {request.path}')
```

---

## 🆘 Troubleshooting Deployment

### App won't start
- Check logs in dashboard
- Verify all dependencies in requirements.txt
- Ensure PORT 5000 (or RENDER port variable)

### Database connection error
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check connection timeout

### CORS errors
- Update CORS origins in app.py
- Check frontend API_BASE URL
- Verify headers in requests

### Payment gateway not working
- Add Razorpay keys to environment variables
- Update webhook URL to your production domain

---

## 💡 Cost Analysis

| Service | Free Tier | Paid | Notes |
|---------|-----------|------|-------|
| Render | Yes | From $7/mo | Best for beginners |
| Railway | Yes | Pay-as-you-go | Generous free tier |
| Netlify | Yes | From $19/mo | Best for frontend |
| AWS RDS | 12 months | Pay-as-you-go | PostgreSQL DB |
| Razorpay | No setup fee | 2-3% + ₹3/txn | Payment gateway |

**Total for hobby project: ₹0 (using free tiers)**

---

## 🎓 Next Steps

1. ✅ Deploy backend to Render/Railway
2. ✅ Deploy frontend to Netlify
3. ✅ Update API URLs in frontend
4. ✅ Test all features
5. ✅ Set up custom domain (optional)
6. ✅ Configure email notifications
7. ✅ Add payment processing
8. ✅ Monitor logs and errors

---

## 📝 Custom Domain Setup

### Render
1. Dashboard → Settings → Custom Domain
2. Add your domain
3. Update DNS settings
4. SSL automatically issued

### Netlify
1. Domain Settings → Custom Domain
2. Enter your domain
3. Update DNS (they'll guide you)
4. HTTPS auto-enabled

---

## 🔗 Useful Links

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Netlify Docs: https://docs.netlify.com
- Flask Production: https://flask.palletsprojects.com/deploy
- PostgreSQL Setup: https://www.postgresql.org/

---

**Good luck! Your app is now production-ready! 🚀**
