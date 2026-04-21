# AirBnb Backend - FastAPI + PostgreSQL

A modern, high-performance booking system API built with FastAPI and PostgreSQL. This is a complete migration from Java/Spring Boot to Python/FastAPI with relational database support.

## Tech Stack

| Layer                 | Technology                 |
| --------------------- | -------------------------- |
| **Framework**         | FastAPI (Python 3.10+)     |
| **Web Server**        | Uvicorn                    |
| **Database**          | PostgreSQL                 |
| **ORM**               | SQLAlchemy 2.0             |
| **Authentication**    | JWT (PyJWT)                |
| **Password Hashing**  | Bcrypt                     |
| **Payments**          | Stripe API                 |
| **Migration Tool**    | Alembic                    |
| **API Documentation** | Swagger/OpenAPI (Built-in) |
| **Validation**        | Pydantic V2                |
| **Async Support**     | Full async/await support   |

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration and settings
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management endpoints
│   │   ├── hotels.py          # Hotel browse/search endpoints
│   │   ├── bookings.py        # Booking endpoints
│   │   ├── rooms.py           # Room management endpoints
│   │   ├── payments.py        # Payment/webhook endpoints
│   │   └── inventory.py       # Inventory management endpoints
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── hotel.py           # Hotel model
│   │   ├── room.py            # Room model
│   │   ├── booking.py         # Booking model
│   │   ├── guest.py           # Guest model
│   │   ├── inventory.py       # Room inventory model
│   │   └── enums.py           # Enums (Role, Gender, BookingStatus, etc.)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # User Pydantic schemas (DTOs)
│   │   ├── hotel.py           # Hotel schemas
│   │   ├── booking.py         # Booking schemas
│   │   ├── room.py            # Room schemas
│   │   ├── payment.py         # Payment schemas
│   │   └── responses.py       # Common response schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── user_service.py    # User business logic
│   │   ├── hotel_service.py   # Hotel business logic
│   │   ├── booking_service.py # Booking business logic
│   │   ├── room_service.py    # Room business logic
│   │   ├── checkout_service.py # Checkout/payment logic
│   │   ├── inventory_service.py # Inventory management
│   │   └── pricing_service.py # Dynamic pricing strategies
│   │
│   ├── security/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py     # JWT token creation and validation
│   │   └── password.py        # Password hashing utilities
│   │
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py   # Base pricing strategy
│   │   ├── holiday_pricing.py # Holiday pricing strategy
│   │   ├── occupancy_pricing.py # Occupancy-based pricing
│   │   ├── surge_pricing.py   # Surge pricing strategy
│   │   └── urgency_pricing.py # Urgency-based pricing
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py        # Database connection and session
│   │   └── base.py            # Base model for all ORM models
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── custom.py          # Custom exception classes
│   │   └── handlers.py        # Exception handlers
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
│
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_hotels.py
│   ├── test_bookings.py
│   └── test_payments.py
│
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not committed)
├── .env.example             # Example environment file
├── .dockerignore
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose for local development
└── README.md               # This file
```

## Key Features

### Authentication & Security

- JWT-based authentication with access and refresh tokens
- Bcrypt password hashing
- Role-based access control (Admin, User, Host)
- Secure token validation and expiration

### Hotel & Room Management

- Hotel browse and search functionality
- Multi-room hotel management
- Room inventory tracking
- Dynamic pricing strategies

### Booking System

- Room availability checking
- Booking creation and management
- Guest information handling
- Booking status tracking

### Payment Processing

- Stripe integration for payments
- Webhook handling for payment confirmations
- Payment status tracking
- Checkout flow management

### Dynamic Pricing

- Base pricing strategy
- Holiday-based pricing adjustments
- Occupancy-based surge pricing
- Urgency-based pricing adjustments
- Composable pricing strategies

### Database

- Fully normalized PostgreSQL schema
- SQLAlchemy ORM for type-safe queries
- Alembic for database migrations
- Relationships and constraints enforced at DB level

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd airbnb-backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**

   ```bash
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/airbnb_db

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe
STRIPE_API_KEY=sk_test_your_stripe_key_here
STRIPE_WEBHOOK_SECRET=whsec_test_your_webhook_secret_here

# Application
DEBUG=False
ENVIRONMENT=production
```

## API Endpoints

### Authentication

- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

### Users

- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `GET /users/{user_id}` - Get user by ID

### Hotels

- `GET /hotels` - Browse hotels with filters
- `GET /hotels/{hotel_id}` - Get hotel details
- `POST /hotels` - Create hotel (Admin only)
- `PUT /hotels/{hotel_id}` - Update hotel (Admin only)
- `DELETE /hotels/{hotel_id}` - Delete hotel (Admin only)

### Rooms

- `GET /hotels/{hotel_id}/rooms` - Get rooms by hotel
- `POST /hotels/{hotel_id}/rooms` - Add room to hotel
- `PUT /rooms/{room_id}` - Update room details
- `DELETE /rooms/{room_id}` - Delete room

### Bookings

- `GET /bookings` - Get user bookings
- `POST /bookings` - Create new booking
- `GET /bookings/{booking_id}` - Get booking details
- `PUT /bookings/{booking_id}` - Update booking status
- `DELETE /bookings/{booking_id}` - Cancel booking

### Payments

- `POST /payments/checkout` - Initiate payment
- `POST /payments/webhook` - Stripe webhook
- `GET /bookings/{booking_id}/payment-status` - Check payment status

### Inventory

- `GET /inventory` - Get room inventory
- `PUT /inventory/{room_id}` - Update room inventory

## API Documentation

FastAPI provides interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=htmla

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Database Migrations

### Create new migration

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## Docker Setup

### Build and run with Docker Compose

```bash
docker-compose up -d
```

### View logs

```bash
docker-compose logs -f
```

### Stop services

```bash
docker-compose down
```

## Development Workflow

1. **Make changes** to your code
2. **Run tests** to ensure functionality
3. **Check database** changes with migrations
4. **Test API** with Swagger UI at `/docs`
5. **Commit** changes with meaningful messages

## Performance Considerations

- **Async Endpoints**: All I/O operations are async
- **Connection Pooling**: Configured via SQLAlchemy
- **Database Indexes**: Created on frequently queried columns
- **Caching**: Strategy-based caching for pricing calculations
- **Rate Limiting**: Can be added per endpoint as needed

## Security Best Practices

- JWT tokens with expiration
- Password hashing with Bcrypt
- CORS configuration
- HTTPS in production
- Environment-based secrets management
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic

## Migration from Java/Spring Boot

This FastAPI application maintains the same business logic and architecture as the original Spring Boot version:

| Java/Spring Boot   | FastAPI                    |
| ------------------ | -------------------------- |
| Controllers        | API routers                |
| DTOs               | Pydantic schemas           |
| Entities           | SQLAlchemy models          |
| Services           | Service classes            |
| Repositories       | Database session queries   |
| Enums              | Python Enums               |
| Exception Handlers | FastAPI exception handlers |
| JWT Service        | PyJWT utilities            |
| Stripe Config      | Stripe Python SDK          |

## Dependencies

See `requirements.txt` for complete list. Key dependencies:

- **fastapi**: Modern web framework
- **uvicorn**: ASGI server
- **sqlalchemy**: ORM for database operations
- **psycopg2**: PostgreSQL adapter
- **pydantic**: Data validation
- **python-jose**: JWT handling
- **passlib**: Password hashing
- **stripe**: Payment processing
- **alembic**: Database migrations
- **python-dotenv**: Environment configuration

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT

## Author

Created by Amit - FastAPI

## Support

For issues or questions, please open an issue in the repository.

# specific language governing permissions and limitations

# under the License.

wrapperVersion=3.3.2
distributionType=only-script
