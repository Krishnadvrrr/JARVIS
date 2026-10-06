# Skill: REST API Standards (FastAPI & Flask)
keywords: [api, rest, endpoint, fastapi, flask, backend, routes, json, server]

## 1. RESTful Conventions
- Use standard HTTP methods: `GET` (retrieve), `POST` (create), `PUT`/`PATCH` (update), `DELETE` (remove).
- Return semantic status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Error.
- Standard response envelope:
  ```json
  {
    "status": "success" | "error",
    "data": { ... },
    "message": "Human readable context"
  }
  ```

## 2. Request Validation & Schemas
- Validate all incoming JSON payloads before processing.
- Reject unexpected or malicious fields.
- Avoid passing raw request parameters directly to database queries.

## 3. CORS & Middleware
- Enable CORS explicitly for trusted origins.
- Include request logging and error-catching middleware to prevent unhandled server crashes.
