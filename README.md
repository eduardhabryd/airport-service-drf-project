# Airport Service API DRF Project

Django REST Framework Project for Airport Service

## Test Details

Test User:
```
login: test@test.com
password: test@test.com

```

Test Data:
```python manage.py loaddata data.json``` - to load test data

## Features

### Users
- Anonim User:
  - Can see Routes, Airports and Flights
  - Can't create anything
  - Anonim User can register an account on the following endpoint:
    - api/user/register/

- Authenticated User:
  - Can see Routes, Airports, Flights, and his Orders
  - Can create orders

- Admin User:
  - Can see all instances
  - Can create everything, also, update and delete everything except for Orders

- In API Root View availiable only enpoints that are allowed for specific user type (Anonim, Authenticated, Admin)

### Additional Features
- JWT Token Implemented on the following endpoints:
  - /api/user/token/
  - /api/user/token/refresh/

- Username was disabled and Email was used instead

- DRF Spectacular was added and is available on the following endpoints:
  - api/schema/
  - api/doc/swagger/
  - api/doc/redoc/

## Demo

![Website interface]()