# eTaskify

This project provides a task management solution as a SaaS platform. 

## Features

- User can create his/her own company.
- User can create staff users for this own company.
- Password automated creation for these staff users.
- When user create staff email notification is sent them.
- When task assigned to user , email notification is sent them.

## Technologies I Used

- Python 3.12
- Django REST
- SQLite
- Docker / Docker Compose
- Pytest
- Django rest framework simple_jwt (for authentication & authorization)
- Ruff & Black (for linting python codes)
- Factoryboy & Faker (for mock testing)
- Coverage (for calculating code coverage percentage)
- Drf spectacular (for swagger ui)

(You can see a full list from `requirements.txt`)



## Folder Structure


```plaintext

├── apps/
│   ├── company/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── company_viewset.py
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   └── company_serializer.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── __init__.py
│   ├── tasks/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── task_viewset.py
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── task_assign_serializer.py
│   │   │   ├── task_create_serializer.py
│   │   │   ├── task_update_serializer.py
│   │   │   └── task_serializer.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── __init__.py
│   ├── users/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── user_viewset.py
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── user_create_staff_serializer.py
│   │   │   ├── user_list_serializer.py
│   │   │   ├── user_logout_serializer.py
│   │   │   └── user_register_serializer.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── __init__.py
│── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│── permissions/
│   ├── __init__.py
│   └── is_admin.py
├── tests/
│   ├── test_company/
│   │   ├── __init__.py
│   │   ├── factories.py
│   │   └── test_company.py
│   ├── test_tasks/
│   │   ├── __init__.py
│   │   ├── factories.py
│   │   └── test_task.py
│   ├── test_users/
│   │   ├── __init__.py
│   │   ├── factories.py
│   │   ├── test_user_create_staff.py
│   │   ├── test_user_list.py
│   │   ├── test_user_login.py
│   │   ├── test_user_logout.py
│   │   └── test_user_register.py
│   ├── __init__.py
│   └── conftest.py
├── utils/
│   ├── __init__.py
│   └── email_send.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── manage.py
└── README.md

```




## Getting Started

### API Documentation

Base URL: `http://localhost:8000/api/v1`

### Authentication


All endpoints (except /users/register/) require a Bearer token in the `Authorization` header:

```http
Authorization: Bearer <your_token>
```

### Prerequisites

Make sure you have installed:

- Docker & Docker Compose

### Installation of Docker

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---
### Setup

Clone the repository:

```bash
git clone git@github.com:osman-abi/eTaskify.git
cd eTaskify
```

### Build Project

```bash
docker compose up --build -d
```

### After building you need to create super user 

```bash
docker exec -it ${container_name} bash
python manage.py createsuperuser
```

# **Note** 

## __Test coverage is 96%. If you want to see this result build project as below:__


```bash
docker compose up --build
```
