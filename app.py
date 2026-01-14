from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///booking_platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize extensions
db = SQLAlchemy(app)
CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://localhost:5000', '*'])

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='user', lazy=True, cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }


class WeddingHall(db.Model):
    __tablename__ = 'wedding_halls'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    amenities = db.Column(db.String(500))  # Comma-separated
    rating = db.Column(db.Float, default=4.5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='wedding_hall', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'capacity': self.capacity,
            'price_per_day': self.price_per_day,
            'description': self.description,
            'amenities': self.amenities.split(',') if self.amenities else [],
            'rating': self.rating
        }


class HotelRoom(db.Model):
    __tablename__ = 'hotel_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    hotel_name = db.Column(db.String(120), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # Single, Double, Suite
    capacity = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.String(500))  # Comma-separated
    rating = db.Column(db.Float, default=4.0)
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='hotel_room', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hotel_name': self.hotel_name,
            'room_type': self.room_type,
            'capacity': self.capacity,
            'price_per_night': self.price_per_night,
            'amenities': self.amenities.split(',') if self.amenities else [],
            'rating': self.rating,
            'available': self.available
        }


class ShoppingItem(db.Model):
    __tablename__ = 'shopping_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)  # Electronics, Fashion, Home, etc
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=10)
    description = db.Column(db.Text)
    rating = db.Column(db.Float, default=4.0)
    vendor = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='item', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'stock': self.stock,
            'description': self.description,
            'rating': self.rating,
            'vendor': self.vendor
        }


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_type = db.Column(db.String(50), nullable=False)  # 'wedding_hall', 'hotel_room'
    wedding_hall_id = db.Column(db.Integer, db.ForeignKey('wedding_halls.id'))
    hotel_room_id = db.Column(db.Integer, db.ForeignKey('hotel_rooms.id'))
    
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    guests = db.Column(db.Integer)
    special_requests = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    payment_id = db.Column(db.String(100))  # Razorpay payment ID
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'booking_type': self.booking_type,
            'check_in_date': self.check_in_date.isoformat(),
            'check_out_date': self.check_out_date.isoformat(),
            'total_price': self.total_price,
            'guests': self.guests,
            'special_requests': self.special_requests,
            'status': self.status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat()
        }


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('shopping_items.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, delivered
    payment_id = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='orders')


class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))
    message = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), default='unread')  # unread, read, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    complaint_type = db.Column(db.String(50), nullable=False)  # booking, payment, service, other
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    admin_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)


# ==================== AUTHENTICATION DECORATOR ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password', 'full_name', 'phone']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
        phone=data['phone']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    session['user_id'] = user.id
    
    return jsonify({
        'message': 'Signup successful',
        'user': user.to_dict()
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['user_id'] = user.id
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    user = User.query.get(session['user_id'])
    return jsonify(user.to_dict()), 200


# ==================== WEDDING HALL ROUTES ====================

@app.route('/api/wedding-halls', methods=['GET'])
def get_wedding_halls():
    halls = WeddingHall.query.all()
    return jsonify([hall.to_dict() for hall in halls]), 200


@app.route('/api/wedding-halls/<int:hall_id>', methods=['GET'])
def get_wedding_hall(hall_id):
    hall = WeddingHall.query.get_or_404(hall_id)
    return jsonify(hall.to_dict()), 200


@app.route('/api/wedding-halls', methods=['POST'])
@admin_required
def create_wedding_hall():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'location', 'capacity', 'price_per_day']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    hall = WeddingHall(
        name=data['name'],
        location=data['location'],
        capacity=data['capacity'],
        price_per_day=data['price_per_day'],
        description=data.get('description'),
        amenities=data.get('amenities', '')
    )
    
    db.session.add(hall)
    db.session.commit()
    
    return jsonify({
        'message': 'Wedding hall created',
        'hall': hall.to_dict()
    }), 201


# ==================== HOTEL ROOM ROUTES ====================

@app.route('/api/hotel-rooms', methods=['GET'])
def get_hotel_rooms():
    rooms = HotelRoom.query.all()
    return jsonify([room.to_dict() for room in rooms]), 200


@app.route('/api/hotel-rooms/<int:room_id>', methods=['GET'])
def get_hotel_room(room_id):
    room = HotelRoom.query.get_or_404(room_id)
    return jsonify(room.to_dict()), 200


@app.route('/api/hotel-rooms', methods=['POST'])
@admin_required
def create_hotel_room():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'hotel_name', 'room_type', 'capacity', 'price_per_night']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    room = HotelRoom(
        name=data['name'],
        hotel_name=data['hotel_name'],
        room_type=data['room_type'],
        capacity=data['capacity'],
        price_per_night=data['price_per_night'],
        amenities=data.get('amenities', '')
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify({
        'message': 'Hotel room created',
        'room': room.to_dict()
    }), 201


# ==================== SHOPPING ROUTES ====================

@app.route('/api/shopping-items', methods=['GET'])
def get_shopping_items():
    category = request.args.get('category')
    
    if category:
        items = ShoppingItem.query.filter_by(category=category).all()
    else:
        items = ShoppingItem.query.all()
    
    return jsonify([item.to_dict() for item in items]), 200


@app.route('/api/shopping-items/<int:item_id>', methods=['GET'])
def get_shopping_item(item_id):
    item = ShoppingItem.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200


@app.route('/api/shopping-items', methods=['POST'])
@admin_required
def create_shopping_item():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'category', 'price', 'vendor']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    item = ShoppingItem(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        stock=data.get('stock', 10),
        description=data.get('description'),
        vendor=data['vendor']
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'message': 'Shopping item created',
        'item': item.to_dict()
    }), 201


# ==================== BOOKING ROUTES ====================

@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    data = request.get_json()
    
    if not data or 'booking_type' not in data:
        return jsonify({'error': 'Missing booking type'}), 400
    
    from datetime import datetime
    check_in = datetime.fromisoformat(data['check_in_date']).date()
    check_out = datetime.fromisoformat(data['check_out_date']).date()
    
    # Calculate price based on booking type
    total_price = 0
    if data['booking_type'] == 'wedding_hall':
        hall = WeddingHall.query.get(data['wedding_hall_id'])
        if not hall:
            return jsonify({'error': 'Hall not found'}), 404
        days = (check_out - check_in).days
        total_price = hall.price_per_day * days
    
    elif data['booking_type'] == 'hotel_room':
        room = HotelRoom.query.get(data['hotel_room_id'])
        if not room:
            return jsonify({'error': 'Room not found'}), 404
        nights = (check_out - check_in).days
        total_price = room.price_per_night * nights
    
    booking = Booking(
        user_id=session['user_id'],
        booking_type=data['booking_type'],
        wedding_hall_id=data.get('wedding_hall_id'),
        hotel_room_id=data.get('hotel_room_id'),
        check_in_date=check_in,
        check_out_date=check_out,
        total_price=total_price,
        guests=data.get('guests', 1),
        special_requests=data.get('special_requests')
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Booking created',
        'booking': booking.to_dict()
    }), 201


@app.route('/api/bookings', methods=['GET'])
@login_required
def get_user_bookings():
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200


@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
@login_required
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != session['user_id'] and not User.query.get(session['user_id']).is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(booking.to_dict()), 200


@app.route('/api/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if booking.status in ['completed', 'cancelled']:
        return jsonify({'error': 'Cannot cancel this booking'}), 400
    
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Booking cancelled', 'booking': booking.to_dict()}), 200


# ==================== CONTACT ROUTES ====================

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'email', 'message']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user_id = session.get('user_id')
    
    contact = Contact(
        user_id=user_id if user_id else 1,  # Anonymous contact uses admin user
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        message=data['message']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({
        'message': 'Contact message submitted successfully',
        'contact_id': contact.id
    }), 201


# ==================== COMPLAINT ROUTES ====================

@app.route('/api/complaints', methods=['POST'])
@login_required
def submit_complaint():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['complaint_type', 'subject', 'description']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    complaint = Complaint(
        user_id=session['user_id'],
        complaint_type=data['complaint_type'],
        subject=data['subject'],
        description=data['description'],
        priority=data.get('priority', 'medium')
    )
    
    db.session.add(complaint)
    db.session.commit()
    
    return jsonify({
        'message': 'Complaint submitted',
        'complaint': {
            'id': complaint.id,
            'status': complaint.status
        }
    }), 201


@app.route('/api/complaints', methods=['GET'])
@login_required
def get_user_complaints():
    complaints = Complaint.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        'id': c.id,
        'complaint_type': c.complaint_type,
        'subject': c.subject,
        'status': c.status,
        'priority': c.priority,
        'created_at': c.created_at.isoformat()
    } for c in complaints]), 200


# ==================== ADMIN ROUTES ====================

@app.route('/api/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    total_contacts = Contact.query.count()
    total_complaints = Complaint.query.count()
    
    pending_complaints = Complaint.query.filter_by(status='open').count()
    unread_contacts = Contact.query.filter_by(status='unread').count()
    
    # Revenue calculation
    completed_bookings = Booking.query.filter_by(status='completed', payment_status='paid').all()
    total_revenue = sum(b.total_price for b in completed_bookings)
    
    return jsonify({
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_contacts': total_contacts,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'unread_contacts': unread_contacts,
        'total_revenue': total_revenue
    }), 200


@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route('/api/admin/bookings', methods=['GET'])
@admin_required
def get_all_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings]), 200


@app.route('/api/admin/contacts', methods=['GET'])
@admin_required
def get_all_contacts():
    contacts = Contact.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'message': c.message,
        'status': c.status,
        'created_at': c.created_at.isoformat()
    } for c in contacts]), 200


@app.route('/api/admin/contacts/<int:contact_id>/resolve', methods=['POST'])
@admin_required
def resolve_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    contact.status = 'resolved'
    db.session.commit()
    return jsonify({'message': 'Contact marked as resolved'}), 200


@app.route('/api/admin/complaints', methods=['GET'])
@admin_required
def get_all_complaints():
    complaints = Complaint.query.all()
    return jsonify([{
        'id': c.id,
        'user_id': c.user_id,
        'complaint_type': c.complaint_type,
        'subject': c.subject,
        'description': c.description,
        'status': c.status,
        'priority': c.priority,
        'admin_notes': c.admin_notes,
        'created_at': c.created_at.isoformat()
    } for c in complaints]), 200


@app.route('/api/admin/complaints/<int:complaint_id>/update', methods=['POST'])
@admin_required
def update_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    data = request.get_json()
    
    if 'status' in data:
        complaint.status = data['status']
    if 'admin_notes' in data:
        complaint.admin_notes = data['admin_notes']
    if 'priority' in data:
        complaint.priority = data['priority']
    
    db.session.commit()
    return jsonify({'message': 'Complaint updated'}), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ==================== INITIALIZATION ====================

with app.app_context():
    db.create_all()
    
    # Create admin user if doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@bookingplatform.com',
            full_name='Admin User',
            phone='9999999999',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Add sample data
        hall1 = WeddingHall(
            name='The Grand Palace',
            location='Mumbai',
            capacity=500,
            price_per_day=50000,
            description='Luxurious wedding hall with modern amenities',
            amenities='AC, Sound System, Parking, Catering'
        )
        
        room1 = HotelRoom(
            name='Deluxe Suite',
            hotel_name='Taj Hotels',
            room_type='Suite',
            capacity=2,
            price_per_night=15000,
            amenities='AC, WiFi, TV, Mini Bar'
        )
        
        item1 = ShoppingItem(
            name='Wedding Decoration Set',
            category='Decorations',
            price=5000,
            stock=20,
            vendor='Decor Store',
            description='Complete decoration set for weddings'
        )
        
        db.session.add_all([hall1, room1, item1])
        db.session.commit()
    
    print("Database initialized successfully!")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
