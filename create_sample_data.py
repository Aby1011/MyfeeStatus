#!/usr/bin/env python
"""
Script to create sample data for MyFeeStatus application
Run this after running migrations: python create_sample_data.py
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfeestatus.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Student
from fees.models import FeeStructure, StudentFee
from payments.models import Payment

User = get_user_model()

def create_sample_data():
    print("Creating sample data for MyFeeStatus...")
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@myfeestatus.com',
            'first_name': 'System',
            'last_name': 'Administrator',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("+ Created admin user (username: admin, password: admin123)")
    
    # Create finance manager
    finance_user, created = User.objects.get_or_create(
        username='finance_manager',
        defaults={
            'email': 'finance@myfeestatus.com',
            'first_name': 'Finance',
            'last_name': 'Manager',
            'user_type': 'finance_manager',
            'phone_number': '+1234567890',
        }
    )
    if created:
        finance_user.set_password('finance123')
        finance_user.save()
        print("+ Created finance manager (username: finance_manager, password: finance123)")
    
    # Create sample students
    students_data = [
        {
            'username': 'john_doe',
            'email': 'john.doe@student.edu',
            'first_name': 'John',
            'last_name': 'Doe',
            'student_id': 'STU001',
            'course': 'btech',
            'year': 2,
            'semester': 4,
            'parent_name': 'Robert Doe',
            'parent_contact': '+1234567891',
        },
        {
            'username': 'jane_smith',
            'email': 'jane.smith@student.edu',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'student_id': 'STU002',
            'course': 'bsc',
            'year': 3,
            'semester': 5,
            'parent_name': 'Michael Smith',
            'parent_contact': '+1234567892',
        },
        {
            'username': 'mike_johnson',
            'email': 'mike.johnson@student.edu',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'student_id': 'STU003',
            'course': 'mtech',
            'year': 1,
            'semester': 2,
            'parent_name': 'David Johnson',
            'parent_contact': '+1234567893',
        },
        {
            'username': 'sarah_wilson',
            'email': 'sarah.wilson@student.edu',
            'first_name': 'Sarah',
            'last_name': 'Wilson',
            'student_id': 'STU004',
            'course': 'ba',
            'year': 2,
            'semester': 3,
            'parent_name': 'Linda Wilson',
            'parent_contact': '+1234567894',
        },
        {
            'username': 'alex_brown',
            'email': 'alex.brown@student.edu',
            'first_name': 'Alex',
            'last_name': 'Brown',
            'student_id': 'STU005',
            'course': 'bcom',
            'year': 1,
            'semester': 1,
            'parent_name': 'Tom Brown',
            'parent_contact': '+1234567895',
        },
    ]
    
    for student_data in students_data:
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name'],
                'user_type': 'student',
                'phone_number': student_data['parent_contact'],
            }
        )
        if created:
            user.set_password('student123')
            user.save()
            
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': student_data['student_id'],
                    'course': student_data['course'],
                    'year': student_data['year'],
                    'semester': student_data['semester'],
                    'admission_date': date.today() - timedelta(days=365),
                    'parent_name': student_data['parent_name'],
                    'parent_contact': student_data['parent_contact'],
                    'address': f"123 Main St, City, State 12345",
                }
            )
            print(f"+ Created student user: {student_data['username']} - {student_data['first_name']} {student_data['last_name']}")
    
    # Create fee structures
    fee_structures_data = [
        {
            'name': 'Tuition Fee',
            'description': 'Semester tuition fee',
            'course': 'btech',
            'year': 2,
            'semester': 4,
            'amount': Decimal('5000.00'),
            'late_fee_amount': Decimal('250.00'),
            'due_date': date.today() + timedelta(days=30),
        },
        {
            'name': 'Laboratory Fee',
            'description': 'Laboratory and equipment usage fee',
            'course': 'btech',
            'year': 2,
            'semester': 4,
            'amount': Decimal('800.00'),
            'late_fee_amount': Decimal('40.00'),
            'due_date': date.today() + timedelta(days=45),
        },
        {
            'name': 'Tuition Fee',
            'description': 'Semester tuition fee',
            'course': 'bsc',
            'year': 3,
            'semester': 5,
            'amount': Decimal('4000.00'),
            'late_fee_amount': Decimal('200.00'),
            'due_date': date.today() + timedelta(days=30),
        },
        {
            'name': 'Tuition Fee',
            'description': 'Semester tuition fee',
            'course': 'mtech',
            'year': 1,
            'semester': 2,
            'amount': Decimal('6000.00'),
            'late_fee_amount': Decimal('300.00'),
            'due_date': date.today() + timedelta(days=30),
        },
        {
            'name': 'Tuition Fee',
            'description': 'Semester tuition fee',
            'course': 'ba',
            'year': 2,
            'semester': 3,
            'amount': Decimal('3500.00'),
            'late_fee_amount': Decimal('175.00'),
            'due_date': date.today() + timedelta(days=30),
        },
        {
            'name': 'Admission Fee',
            'description': 'One-time admission processing fee',
            'course': 'bcom',
            'year': 1,
            'semester': 1,
            'amount': Decimal('1500.00'),
            'late_fee_amount': Decimal('75.00'),
            'due_date': date.today() + timedelta(days=15),
        },
    ]
    
    for fee_data in fee_structures_data:
        fee_structure, created = FeeStructure.objects.get_or_create(
            name=fee_data['name'],
            course=fee_data['course'],
            year=fee_data['year'],
            semester=fee_data['semester'],
            defaults=fee_data
        )
        if created:
            print(f"+ Created fee structure: {fee_data['name']} for {fee_data['course']} Year {fee_data['year']}")
    
    # Assign fees to students
    students = Student.objects.all()
    fee_structures = FeeStructure.objects.all()
    
    for student in students:
        # Find matching fee structures for this student
        matching_structures = fee_structures.filter(
            course=student.course,
            year=student.year,
            semester=student.semester
        )
        
        for structure in matching_structures:
            student_fee, created = StudentFee.objects.get_or_create(
                student=student,
                fee_structure=structure,
                defaults={
                    'total_amount': structure.amount,
                    'due_date': structure.due_date,
                }
            )
            if created:
                print(f"+ Assigned fee {structure.name} to student {student.user.username}")
    
    # Create some sample payments
    sample_payments = [
        {
            'student_id': 'STU001',
            'fee_name': 'Tuition Fee',
            'amount': Decimal('5000.00'),
            'payment_mode': 'credit_card',
            'status': 'completed',
        },
        {
            'student_id': 'STU002',
            'fee_name': 'Tuition Fee',
            'amount': Decimal('2000.00'),
            'payment_mode': 'upi',
            'status': 'completed',
        },
        {
            'student_id': 'STU003',
            'fee_name': 'Tuition Fee',
            'amount': Decimal('3000.00'),
            'payment_mode': 'debit_card',
            'status': 'completed',
        },
    ]
    
    for payment_data in sample_payments:
        try:
            student = Student.objects.get(student_id=payment_data['student_id'])
            student_fee = StudentFee.objects.get(
                student=student,
                fee_structure__name=payment_data['fee_name']
            )
            
            payment, created = Payment.objects.get_or_create(
                student_fee=student_fee,
                amount=payment_data['amount'],
                defaults={
                    'payment_mode': payment_data['payment_mode'],
                    'status': payment_data['status'],
                }
            )
            
            if created:
                # Update student fee with payment
                student_fee.amount_paid += payment_data['amount']
                student_fee.update_status()
                print(f"+ Created payment: {payment.transaction_id}")
        except Exception as e:
            print(f"- Error creating payment for {payment_data['student_id']}: {e}")
    
    print("\n[Success] Sample data creation completed!")
    print("\nLogin credentials:")
    print("Admin: username=admin, password=admin123")
    print("Finance Manager: username=finance_manager, password=finance123")
    print("Students: username=john_doe/jane_smith/mike_johnson/sarah_wilson/alex_brown, password=student123")

if __name__ == "__main__":
    create_sample_data()
