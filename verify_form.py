import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldcinema_backend.settings')
django.setup()

from users.forms import MovieForm

def verify_movie_form():
    print("--- Verifying MovieForm ---")
    
    # Test data with scheduled_date
    data = {
        "title": "Test Movie Form",
        "genre": "Action",
        "duration": "2h",
        "category": "movie",
        "description": "Test description",
        "price": 1000,
        "scheduled_date": "2025-12-01T14:30" # Format for datetime-local
    }
    
    form = MovieForm(data=data)
    
    if form.is_valid():
        print("SUCCESS: Form is valid with scheduled_date.")
        print(f"Cleaned date: {form.cleaned_data['scheduled_date']}")
    else:
        print("FAILURE: Form is invalid.")
        print(form.errors)

if __name__ == "__main__":
    verify_movie_form()
