#!/usr/bin/env python
"""
Admin User Management Script for Book Catalog
This script handles creating, verifying, and managing admin users.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sba24070_book_catalogue.settings')
django.setup()

from books.models import User
from django.contrib.auth.hashers import check_password, make_password

def create_admin_user():
    """Create admin user if it doesn't exist"""
    if User.objects.filter(username='admin').exists():
        print("INFO: Admin user already exists!")
        return User.objects.get(username='admin')
    
    print("CREATING: Admin user...")
    admin_user = User.objects.create(
        username='admin',
        email='admin@example.com',
        password='admin'  # Will be hashed automatically
    )
    
    print("SUCCESS: Admin user created successfully!")
    return admin_user

def verify_admin_user():
    """Verify admin user exists and password works"""
    try:
        admin_user = User.objects.get(username='admin')
        print("SUCCESS: Admin user found!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: {admin_user.password[:20]}... (hashed)")
        
        # Test password authentication
        if check_password('admin', admin_user.password):
            print("SUCCESS: Password 'admin' is correct!")
            return True
        else:
            print("ERROR: Password 'admin' is incorrect!")
            return False
            
    except User.DoesNotExist:
        print("ERROR: Admin user not found!")
        return False

def test_password_authentication():
    """Test various password scenarios"""
    try:
        admin_user = User.objects.get(username='admin')
        print("\nTESTING: Password authentication:")
        
        # Test correct password
        if check_password('admin', admin_user.password):
            print("SUCCESS: Correct password 'admin' works")
        else:
            print("ERROR: Correct password 'admin' failed")
        
        # Test wrong password
        if check_password('wrong', admin_user.password):
            print("ERROR: Wrong password 'wrong' incorrectly accepted")
        else:
            print("SUCCESS: Wrong password 'wrong' correctly rejected")
        
        # Test empty password
        if check_password('', admin_user.password):
            print("ERROR: Empty password incorrectly accepted")
        else:
            print("SUCCESS: Empty password correctly rejected")
            
    except User.DoesNotExist:
        print("ERROR: Admin user not found for testing")

def show_user_statistics():
    """Show statistics about all users"""
    total_users = User.objects.count()
    admin_users = User.objects.filter(username='admin').count()
    regular_users = total_users - admin_users
    
    print(f"\nSTATISTICS: User Statistics:")
    print(f"   Total users: {total_users}")
    print(f"   Admin users: {admin_users}")
    print(f"   Regular users: {regular_users}")
    
    if total_users > 0:
        print(f"\nUSERS: All users:")
        for user in User.objects.all():
            print(f"   - {user.username} ({user.email}) - Created: {user.created_at}")

def reset_admin_password():
    """Reset admin password to 'admin'"""
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.password = 'admin'  # Will be hashed on save
        admin_user.save()
        print("SUCCESS: Admin password reset to 'admin'")
    except User.DoesNotExist:
        print("ERROR: Admin user not found")

def main():
    """Main function to run all admin management tasks"""
    print("=" * 50)
    print("ADMIN USER MANAGEMENT SCRIPT")
    print("=" * 50)
    
    # Create admin user if needed
    admin_user = create_admin_user()
    
    # Verify admin user
    if verify_admin_user():
        # Test password authentication
        test_password_authentication()
        
        # Show user statistics
        show_user_statistics()
        
        print("\n" + "=" * 50)
        print("LOGIN INSTRUCTIONS:")
        print("=" * 50)
        print("Username: admin")
        print("Password: admin")
        print("\nURL: Go to: http://127.0.0.1:8000/login/")
        print("ADMIN: Admin Dashboard: http://127.0.0.1:8000/admin-dashboard/")
        print("=" * 50)
    else:
        print("ERROR: Admin user verification failed!")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'create':
            create_admin_user()
        elif command == 'verify':
            verify_admin_user()
        elif command == 'test':
            test_password_authentication()
        elif command == 'stats':
            show_user_statistics()
        elif command == 'reset':
            reset_admin_password()
        else:
            print("Usage: python admin_manager.py [create|verify|test|stats|reset]")
            print("Or run without arguments for full setup")
    else:
        main() 