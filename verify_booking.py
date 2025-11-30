import os
import django
from django.conf import settings
from django.test import RequestFactory
from django.utils import timezone
from datetime import timedelta
from django.contrib.messages.storage.fallback import FallbackStorage

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldcinema_backend.settings')
django.setup()

from users.models import Movie, Booking, CustomUser, Notification
from users.views import create_booking

def verify_booking_flow():
    print("--- Verifying Booking Flow with Scheduled Date ---")

    # 1. Setup Data
    print("1. Setting up test data...")
    
    # Create a test user
    email = "booker@example.com"
    user, created = CustomUser.objects.get_or_create(email=email)
    if created:
        user.set_password("password123")
        user.balance = 5000
        user.save()
    else:
        user.balance = 5000 # Reset balance
        user.save()
    
    # Create a test movie with scheduled date
    movie_title = "Scheduled Booking Test"
    scheduled_date = timezone.now() + timedelta(days=2)
    # Round to minutes to match what we might expect (seconds usually ignored in simple inputs)
    scheduled_date = scheduled_date.replace(second=0, microsecond=0)
    
    movie, created = Movie.objects.get_or_create(title=movie_title)
    movie.scheduled_date = scheduled_date
    movie.category = "movie"
    movie.price = 500
    movie.duration = "2h"
    movie.save()
    print(f"   Movie: {movie.title}, Scheduled: {movie.scheduled_date}")

    # 2. Simulate Booking Request
    print("\n2. Simulating booking request...")
    factory = RequestFactory()
    
    # We don't pass date/time in POST anymore!
    data = {
        "movie_name": movie.title,
        "selected_seats": "C1,C2"
    }
    
    request = factory.post('/book/create/', data)
    request.user = user
    
    # Add message support
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    # Execute view
    response = create_booking(request)
    
    # 3. Verify Booking
    print("\n3. Verifying booking...")
    
    # Check if booking exists
    booking = Booking.objects.filter(user=user, movie_name=movie.title).last()
    
    if booking:
        print(f"   Booking found: {booking}")
        print(f"   Booking Date: {booking.date}")
        print(f"   Booking Time: {booking.time}")
        
        expected_date = scheduled_date.date()
        expected_time = scheduled_date.strftime("%H:%M")
        
        if booking.date == expected_date and booking.time == expected_time:
            print("   SUCCESS: Booking date and time match scheduled date.")
        else:
            print(f"   FAILURE: Date/Time mismatch. Expected {expected_date} {expected_time}")
            
        # Check balance deduction
        user.refresh_from_db()
        expected_balance = 5000 - (500 * 2) # 2 seats
        if user.balance == expected_balance:
             print(f"   SUCCESS: Balance deducted correctly. Current: {user.balance}")
        else:
             print(f"   FAILURE: Balance mismatch. Expected {expected_balance}, Got {user.balance}")

    else:
        print("   FAILURE: No booking created.")
        # Check messages if any
        storage = messages
        for message in storage:
            print(f"   Message: {message}")

    # 4. Cleanup
    print("\n4. Cleanup...")
    if booking:
        booking.delete()
    movie.delete()
    # user.delete()
    print("   Done.")

if __name__ == "__main__":
    verify_booking_flow()
