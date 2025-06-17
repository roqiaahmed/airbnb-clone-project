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
  
