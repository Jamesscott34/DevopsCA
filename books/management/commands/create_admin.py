from django.core.management.base import BaseCommand
from books.models import User

class Command(BaseCommand):
    help = 'Creates an admin user with username "admin" and password "admin"'

    def handle(self, *args, **options):
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(
                self.style.WARNING('Admin user already exists!')
            )
            admin_user = User.objects.get(username='admin')
            self.stdout.write(f"Username: {admin_user.username}")
            self.stdout.write(f"Email: {admin_user.email}")
            return
        
        # Create admin user
        admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='admin'  # This will be hashed automatically by the model's save method
        )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Admin user created successfully!')
        )
        self.stdout.write(f"Username: {admin_user.username}")
        self.stdout.write(f"Email: {admin_user.email}")
        self.stdout.write("Password: admin")
        self.stdout.write("\nYou can now log in with:")
        self.stdout.write("Username: admin")
        self.stdout.write("Password: admin") 