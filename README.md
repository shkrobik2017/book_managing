# Book Management Platform

This is a web application for managing books, authors, and users. The system includes CRUD functionality for all
entities, as well as authentication and authorization features.

I planned for the project to include raw database queries, but I don't have experience working with them, so to meet the
deadline, I implemented everything using Tortoise ORM.

## Installation

### 1. Clone the Repository

Clone the repository to your computer using the following command:

``` bash
    git clone https://github.com/shkrobik2017/book_managing.git
```

### 2. Configure Environment Variables

Create a `.env` file using the `env-example` as a template:

``` bash
    cp env-example .env
```

Fill in the `.env` file with the correct values, such as database parameters and security keys.

### 3. Install Dependencies

To install dependencies, follow these steps:

1. Ensure that **Docker** and **Docker Compose** are installed.
2. Build and start the containers:

``` bash
    docker-compose up --build
```

This will install all necessary dependencies via Poetry and set up the PostgreSQL database.

## Usage

- The application will be available at: `http://localhost:8081` (the specified port can be changed in
  `docker-compose.yml`).

### Main APIs:

- **Authentication**
    - Register: `POST /v1/api/auth/register`
    - Login: `POST /v1/api/auth/token`

- **Authors**
    - Create an author: `POST /v1/api/authors/`
    - Get all authors: `GET /v1/api/authors/`
    - Get author by ID: `GET /v1/api/authors/{id}`
    - Update an author: `PUT /v1/api/authors/{id}`
    - Delete an author: `DELETE /v1/api/authors/{id}`

- **Books**
    - Create a book: `POST /v1/api/books/`
    - Import books from JSON or CSV: `POST /v1/api/books/import`
    - Get all books: `GET /v1/api/books/`
    - Find a book by ID: `GET /v1/api/books/{id}`
    - Search books: `GET /v1/api/books/search`
    - Update a book: `PUT /v1/api/books/{id}`
    - Delete a book: `DELETE /v1/api/books/{id}`

Details about each endpoint can be found in the automatically generated Swagger documentation at:
`http://localhost:8081/docs`.

### Testing

To run tests, use the following command when the container is running:

``` bash
    poetry run pytest src/tests/test_endpoints.py -v
```

## Project Structure

The project is organized as follows:

- **src/db/**: Database interaction logic.
    - **common/**: Common model for all models.
    - **models/**: Definitions of models for users, books, and authors.
    - **singleton_tortoise/**: Database singleton class.
    - **db_setup.py**: Database setup.

- **src/routers/**: Definitions of FastAPI routes.
    - **auth/**: Authentication and authorization routes.
    - **authors/**: CRUD for working with authors.
    - **books/**: CRUD for working with books.

- **src/routers/router.py**: Central router connecting modules.
- **src/routers/depends.py**: Contains dependencies for authentication.
- **src/settings.py**: Application configuration, including environment variables.
- **tests/**: Tests to verify API functionality.

## Technologies

- Programming Language: Python 3.12
- Framework: FastAPI
- Database: PostgreSQL
- Dependency Management: Poetry
- Testing: Pytest
- User registration and authorization are performed using JWT tokens.

## Deployment

To deploy on a server:

1. Install Docker and Docker Compose.
2. Configure the environment variables in the `.env` file.
3. Start the Docker containers:

``` bash
    docker-compose up --build -d
```

The application will be available at the specified address.
