import os
import django
from django.conf import settings
from django.utils import timezone
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldcinema_backend.settings')
django.setup()

from users.forms import MovieForm
from users.models import Movie

def verify_form_rendering():
    print("--- Verifying MovieForm Rendering ---")
    
    # Create a dummy movie instance
    dt = datetime.datetime(2025, 12, 25, 18, 30) # Dec 25, 2025, 6:30 PM
    # Make it timezone aware if settings use TZ
    if settings.USE_TZ:
        dt = timezone.make_aware(dt)
        
    movie = Movie(
        title="Render Test",
        scheduled_date=dt
    )
    
    form = MovieForm(instance=movie)
    rendered = form.as_p()
    
    print("Rendered HTML snippet for scheduled_date:")
    # Extract the relevant line
    for line in rendered.split('\n'):
        if 'scheduled_date' in line:
            print(line)
            if 'value="2025-12-25T18:30"' in line:
                print("SUCCESS: Value format is correct for datetime-local.")
            else:
                print("FAILURE: Value format is incorrect.")
                print(f"Expected: value=\"2025-12-25T18:30\"")

if __name__ == "__main__":
    verify_form_rendering()
