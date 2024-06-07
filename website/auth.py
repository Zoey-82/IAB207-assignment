from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# event booking
@auth_bp.route('/book_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = TicketForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        order = Order(user_id=current_user.id, event_id=event.id, quantity=quantity)
        db.session.add(order)
        db.session.commit()
        flash('Booking successful! Your order ID is {}'.format(order.id))
        return redirect(url_for('index'))
    return render_template('book_event.html', event=event, form=form)

# booking history 
@auth_bp.route('/booking_history')
@login_required
def booking_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('booking_history.html', orders=orders)

# event details 
@auth_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(user_id=current_user.id, event_id=event.id, content=form.content.data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!')
        return redirect(url_for('auth.event_detail', event_id=event.id))
    comments = Comment.query.filter_by(event_id=event.id).all()
    return render_template('event_detail.html', event=event, form=form, comments=comments)

# user logout 
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# user register 
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=hashed_password,
                    contact_number=form.contact_number.data,
                    street_address=form.street_address.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

# event status 
@auth_bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index1.html', events=events)
    
# event creation
@auth_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            owner_id=current_user.id,
            status='Open'
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('auth.index'))
    return render_template('create_event.html', form=form)

$ event updating 
@auth_bp.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        flash('You are not authorized to update this event.')
        return redirect(url_for('auth.index'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('auth.index'))
    return render_template('update_event.html', form=form, event=event)

# event cancel
@auth_bp.route('/cancel_event/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        flash('You are not authorized to cancel this event.')
        return redirect(url_for('auth.index'))

    event.status = 'Cancelled'
    db.session.commit()
    flash('Event cancelled successfully!')
    return redirect(url_for('auth.index'))
