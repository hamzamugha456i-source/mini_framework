# Custom Python Mini-Framework

## Overview
A lightweight, WSGI-compliant MVC web framework built from scratch in Python. This framework demonstrates mastery of OOP, SOLID principles, and Design Patterns (Factory, Observer, Repository).

## Architecture
- **Core**: Request, Response, and Router handling raw WSGI signals.
- **MVC**: 
  - **Models**: In-memory ORM with validation and field types.
  - **Controllers**: Class-based controllers for CRUD operations.
- **Patterns Used**:
  - **Factory**: `ControllerFactory` for dynamic controller creation.
  - **Observer**: `Subject` and `LoggerObserver` for request logging.
  - **Singleton**: Applied to the Application instance (implied).

## SOLID Principles Applied
1. **SRP**: `Request` parses data, `Router` matches URLs, `Model` handles data. Separation of concerns is strict.
2. **OCP**: New validators can be added by extending the `Validator` base class without changing existing code.
3. **LSP**: `ModelController` can be replaced by any child controller without breaking the app.
4. **ISP**: Validator interfaces are kept simple.
5. **DIP**: Controllers depend on the abstract `Model` class, not specific database implementations.

## How to Run
1. Run the server:
   ```bash
   python app.py