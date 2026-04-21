from django.contrib.auth.models import User
from catch.models import Profile

def create_missing_profiles():
    count = 0
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)
        count += 1
    print(f"Ensured profiles for {count} users.")

if __name__ == "__main__":
    create_missing_profiles()
