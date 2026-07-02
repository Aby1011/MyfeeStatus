# MyFeeStatus - Student Fee Management System

MyFeeStatus is a comprehensive web-based student fee management platform designed to simplify and digitize the fee processing and tracking system for educational institutions. Built with Django, it provides a streamlined workflow for managing student fee records, processing payments, issuing reminders, and generating receipts.

## Features

### Multi-User System
- **Admin**: Complete system oversight, user management, fee structure management
- **Finance Manager**: Payment processing, fee management, transaction monitoring
- **Students**: View fee status, make payments, download receipts

### Core Functionality
- **Fee Management**: Create and manage fee structures for different courses/semesters
- **Payment Processing**: Support for multiple payment modes (Credit Card, Debit Card, UPI, Cash, Bank Transfer)
- **Real-time Status Tracking**: Monitor pending, paid, overdue, and partial payments
- **Automated Calculations**: Late fees, remaining amounts, payment tracking
- **Receipt Generation**: Automatic receipt creation with unique reference numbers
- **Responsive Design**: Mobile-friendly interface with modern UI

### Payment Modes Supported
- Credit Card
- Debit Card
- UPI (Unified Payments Interface)
- Cash payments
- Bank Transfer

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom responsive CSS with Font Awesome icons
- **Forms**: Django Crispy Forms with Bootstrap 4

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Sample Data**
   ```bash
   python create_sample_data.py
   ```

4. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Application**
   - Open your browser and go to `http://localhost:8000`
   - Login with the sample credentials below

## Sample Login Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Role**: System Administrator

### Finance Manager
- **Username**: finance_manager
- **Password**: finance123
- **Role**: Finance Manager

### Student Users
- **Username**: john_doe, jane_smith, mike_johnson, sarah_wilson, alex_brown
- **Password**: student123
- **Role**: Student

## Project Structure

```
myfeestatus/
├── accounts/          # User management and authentication
├── fees/             # Fee structures and management
├── payments/         # Payment processing and receipts
├── dashboard/        # Role-based dashboards
├── templates/        # HTML templates
├── static/          # CSS, JavaScript, images
├── myfeestatus/     # Project settings
└── manage.py        # Django management script
```

## Key Models

### CustomUser
- Extended Django user model with role-based access
- User types: Admin, Finance Manager, Student

### Student
- Student profile information
- Course, year, semester details
- Parent/guardian information

### FeeStructure
- Define fee types for different courses/semesters
- Amount, due dates, late fee configuration

### StudentFee
- Individual fee assignments to students
- Payment tracking and status management

### Payment
- Payment transaction records
- Multiple payment mode support
- Transaction ID generation

### PaymentReceipt
- Automatic receipt generation
- Unique receipt numbering system

## Features by User Role

### Admin Dashboard
- Complete system statistics
- User management
- Fee structure creation and management
- Fee assignment to students
- System monitoring and reports

### Finance Manager Dashboard
- Payment processing and monitoring
- Fee collection statistics
- Overdue fee management
- Transaction reports
- Revenue tracking

### Student Dashboard
- Personal fee status overview
- Payment history
- Upcoming due dates
- Online payment processing
- Receipt download

## Payment Processing Flow

1. **Fee Assignment**: Admin/Finance Manager assigns fees to students
2. **Payment Initiation**: Student selects fee and payment amount
3. **Payment Mode Selection**: Choose from available payment methods
4. **Payment Details**: Enter payment-specific information
5. **Processing**: Simulate payment gateway processing
6. **Receipt Generation**: Automatic receipt creation
7. **Status Update**: Real-time fee status updates

## Security Features

- Basic input validation and sanitization
- CSRF protection on all forms
- Secure payment data handling (no sensitive data storage)
- Role-based access controls
- Session management

## Responsive Design

The application features a fully responsive design that works seamlessly across:
- Desktop computers
- Tablets
- Mobile devices

## API Features

- RESTful URL structure
- JSON data handling for payment processing
- AJAX-ready components for future enhancements

## Future Enhancements

Potential improvements for production deployment:

1. **Email Integration**: Automated fee reminders and receipt delivery
2. **SMS Notifications**: Payment confirmations and due date alerts
3. **Real Payment Gateway**: Integration with actual payment processors
4. **Advanced Reporting**: Detailed analytics and financial reports
5. **Bulk Operations**: Batch fee assignments and payment processing
6. **Document Management**: Upload and manage fee-related documents
7. **Multi-tenancy**: Support multiple institutions
8. **API Development**: RESTful API for mobile app integration

## Development Notes

### Sample Data
The `create_sample_data.py` script creates:
- 1 Admin user
- 1 Finance Manager
- 5 Sample students with different courses
- Multiple fee structures
- Sample payment transactions

### Database Schema
- Uses Django ORM with SQLite for development
- Easily configurable for PostgreSQL/MySQL in production
- Proper foreign key relationships and constraints

### Validation
- Basic form validation for all user inputs
- Payment amount validation against remaining fees
- Date validation for due dates and payment processing

## License

This project is created for educational and demonstration purposes.

## Support

For questions or issues related to this project, please refer to the code documentation and comments within the application files.

---

**Author**: MiniMax Agent
**Version**: 1.0.0
**Last Updated**: October 2025
