# airbnb-clone-project

The **Airbnb Clone Project** is a comprehensive, real-world application designed to simulate the development of a robust booking platform similar to Airbnb.  
The goal of this project is to understand complex architectures, workflows, and collaborative team dynamics while building a scalable web application.

This project utilizes tools and technologies including **Django**, **PostgreSQL**, **Docker**, **GraphQL**, **Celery**, and **Redis**.


## Team Roles

- **Backend Developer**: Implements API endpoints, database schemas, and core business logic.  
- **Database Administrator (DBA)**: Designs and optimizes the database structure, manages indexing, and ensures data integrity.  
- **DevOps Engineer**: Oversees deployment pipelines, monitors system performance, and manages backend scalability using tools like Docker and Redis.  
- **QA Engineer**: Develops and runs test suites to ensure backend functionalities meet quality standards and are bug-free.


## Technology Stack

- **Django**: A high-level Python web framework used for building the RESTful API.
- **Django REST Framework**: Provides tools for creating and managing RESTful APIs.
- **PostgreSQL**: A powerful relational database used for data storage.
- **GraphQL**: Allows for flexible and efficient querying of data.
- **Celery**: For handling asynchronous tasks such as sending notifications or processing payments.
- **Redis**: Used for caching and session management.
- **Docker**: Containerization tool for consistent development and deployment environments.
- **CI/CD Pipelines**: Automated pipelines for testing and deploying code changes.


## Database Design

- **Users**
  - `name`
  - `email`
  - `password`
  - Has many **properties**
  - Can write multiple **reviews**
  - Can make multiple **bookings**
    
- **Properties**
  - `location`
  - `description`
  - Has many **reviews**
  - Has many **bookings**
  - Belongs to a **user**
    
- **Bookings**
  - `price`
  - `date`
  - `is_paid` (boolean)
  - Belongs to a **user**
  - Belongs to a **property**
  - Has one **payment**
    
- **Reviews**
  - `rating`
  - `comment`
  - Belongs to a **user**
  - Belongs to a **property**
    
- **Payments**
  - `amount`
  - `payment_date`
  - Belongs to a **booking**


## Feature Breakdown

- **User Management**
  - Secure user registration and authentication
  - User profile management

- **Property Management**
  - Create, update, and manage property listings

- **Booking System**
  - Allow users to book properties
  - Manage booking details (dates, status, etc.)

- **Payment Processing**
  - Integrate a secure payment system
  - Record and manage transaction details

- **Review System**
  - Enable users to leave ratings and written reviews for properties

- **Data Optimization**
  - Optimize database queries for efficient data retrieval and storage


## API Security

- **Authentication**  
  Required for actions such as booking a property, leaving a review, registering, or creating a property. It ensures that only verified users can access protected endpoints.

- **Authorization**  
  Ensures that users can only manage their own data (e.g., edit or delete their own listings, bookings, or reviews).


## CI/CD Pipeline

A **CI/CD (Continuous Integration/Continuous Deployment)** pipeline is an automated workflow that helps integrate new code into the source codebase smoothly. It ensures all tests pass, verifies system behavior, and then delivers the code to production or staging environments through automated build and deployment processes.

This pipeline bridges the gap between development and operations by streamlining the process from code commit to deployment.

### Tools Used

- **GitHub Actions**
- **Docker**
- **Docker Compose**

### Why Are CI/CD Pipelines Important?

1️⃣ **Automation Saves Time** — No more manual deployments or builds.  
2️⃣ **Reduces Human Error** — Tests, linting, and code reviews run automatically before merging.  
3️⃣ **Faster Feedback Loop** — Developers get immediate feedback when something breaks.  
4️⃣ **Scalability** — The workflow scales with your team and project size.  
5️⃣ **Consistent & Reliable Deployments** — The same steps run every time, ensuring stability.


