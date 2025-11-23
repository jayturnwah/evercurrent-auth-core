#  EverCurrent Auth & API Core  
### **Modern Django Backend with JWT Authentication, RBAC, CRUD API, Swagger Docs, and CI**

A clean, production-ready backend foundation built with Django, Django REST Framework, SimpleJWT, and GitHub Actions CI.  
Includes a custom user model, role-based access control, reusable CRUD patterns, OpenAPI documentation, and a full test suite.

This project potentially serves as the backend core for all EverCurrent applications — open to updates and evolving versions for all potential products developped

---

##  Features

###  Authentication
- Full JWT auth using `rest_framework_simplejwt`
- Access + refresh tokens
- Secure logout with token blacklisting
- Stateless, scalable, API-friendly

###  Custom User Model
- Fully extendable `User` model
- Role system (`Role` model + M2M relationship)
- Supports Admin, Creator, Client, and any future roles

###  Role-Based Access Control (RBAC)
- Custom permission classes:
  - `HasRole` → protects creation/list endpoints  
  - `IsOwnerOrAdmin` → protects updates/deletes  
- Admins see everything  
- Creators see only their own objects  
- Non-role users are strictly restricted

### Reusable CRUD API (Resource API)
- Built using DRF `ModelViewSet`
- Pagination, ordering, filtering, searching
- Owner-bound records with automatic assignment
- Secure by default

###  Auto-Generated API Docs
- Powered by drf-spectacular  
- Swagger UI at:  
  ```
  /docs/
  ```
- OpenAPI 3 schema at:  
  ```
  /schema/
  ```

###  CI/CD (GitHub Actions)
- Automated test runner on every `push` and `pull_request`
- Python + pytest integration
- Green builds = confidence + professional workflow

### Comprehensive Test Suite
Covers:
- Health check endpoint  
- Creator CRUD flow  
- Anonymous access rejection  
- Missing-role rejection  
- Admin global visibility rules  

---

##  Why I Built This

I built this backend core because I needed a **professional, expandable, and secure foundation** for all the systems I'm creating — from music licensing tools to clothing drop systems, analytics engines, and martial arts applications, and beyond!

I wanted a project that proves:
- I understand real backend engineering  
- I can architect authentication, authorization, and permissions  
- I can design reusable systems and apply professional best practices  
- I can write clean, tested, maintainable code  
- I can work like a real backend engineer with CI, tests, and API docs  

This project is the **blueprint** for my future applications.  
It shows employers, collaborators, and clients that I can build **serious infrastructure**, not just demo apps.

It represents the first layer of the world I’m creating — tools that empower creators, fighters, and everyday people to take control of their craft, business, and life.

---

##  Project Structure

```
evercurrent-auth-core/
│
├── .github/workflows/ci.yml        # GitHub Actions CI
├── src/
│   ├── config/                     # Django project settings
│   ├── core/                       # Reusable API features (Resource API)
│   └── users/                      # Custom user + roles
│
├── requirements.txt
└── README.md
```

---

##  Tech Stack

- **Python 3.12+**
- **Django 5**
- **Django REST Framework**
- **SimpleJWT**
- **drf-spectacular**
- **pytest**
- **GitHub Actions**

---

##  Getting Started

### **1. Clone the repo**
```bash
git clone https://github.com/<your-username>/evercurrent-auth-core.git
cd evercurrent-auth-core
```

### **2. Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set up environment variables**
Create a `.env` file in `src/`:

```env
DEBUG=True
SECRET_KEY=dev-only-change-me
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### **5. Run migrations**
```bash
cd src
python manage.py migrate
```

### **6. Create a superuser**
```bash
python manage.py createsuperuser
```

### **7. Start the server**
```bash
python manage.py runserver
```

Visit:  
`http://127.0.0.1:8000/healthz/`  
`http://127.0.0.1:8000/docs/`

---

##  Authentication Endpoints

| Endpoint | Purpose |
|----------|----------|
| `POST /auth/token/` | Obtain access + refresh tokens |
| `POST /auth/refresh/` | Refresh an access token |
| `POST /auth/logout/` | Blacklist a refresh token |

---

## Resource API (Example CRUD)

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/resources/` | List user’s resources |
| `POST` | `/resources/` | Create a resource |
| `GET` | `/resources/<id>/` | Retrieve resource |
| `PATCH` | `/resources/<id>/` | Update resource |
| `DELETE` | `/resources/<id>/` | Delete resource |

Roles required:  
- **creator** or **admin** to create  
- **owner** or **admin** to update/delete  
- **admin** sees all resources  
- **creator** sees only their own  

---

##  Running Tests

From inside the `src/` folder:

```bash
pytest -q
```

---

##  CI Pipeline (GitHub Actions)

Every commit triggers:
1. Dependency install  
2. Django setup  
3. Full pytest execution  

View runs under the **Actions** tab in GitHub.

---

##  Author

**Justin Ternois**  
* Entrepreneur * Data Engineer/Analyst * Backend Dev  * Music Producer * MMA Athlete * 
Building tools that empower creators, brands, and everyday people.  
