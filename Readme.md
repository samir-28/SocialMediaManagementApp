# 🧑‍🤝‍🧑 Simple Social Media Platform - Django REST API

A simple social media platform built using Django and Django REST Framework with features like user authentication, profile management, post creation (with images), commenting, liking, and admin post control.

---

## 🚀 Features

### User Roles

- **Normal User**:
  - Register & Login (JWT Auth)
  - Create/Update/Delete Profile & Posts
  - Like/Unlike Posts
  - Add/Delete Comments

- **Admin**:
  - View All Posts
  - Delete Any User's Post

### Core Functionalities

- JWT Authentication (`djangorestframework-simplejwt`)
- CRUD operations for Users & Posts
- Image support in posts
- Likes & Comments on Posts
- Admin Panel Controls

---

## 🛠 Technology Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (via Simple JWT)
- **Database**: SQLite (default)
- **Image Handling**: `ImageField` with Pillow
- 
## 🧩 Setup Instructions

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/yourusername/socialmedia-drf.git
cd socialmedia-drf

python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

pip install -r requirements.txt

pip install django djangorestframework djangorestframework-simplejwt Pillow

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


Authentication (JWT)
Obtain Token
POST /api/login/
{
  "username": "your_username",
  "password": "your_password"
}


Register
POST /api/register/

Use the returned token in the header:
    Authorization: Bearer your_access_token



API Endpoints
Method	  Endpoint	          Description
POST	  /api/register/	    Register a new user
POST	  /api/login/	        Login and receive JWT tokens
GET    	/api/profile/{id}/	  Get user profile
PUT	    /api/profile/{id}/	    Update user profile
DELETE	/api/profile/{id}/	    Delete user profile
GET	    /api/posts/	              Get all posts
POST	  /api/posts/	              Create a new post
PUT	    /api/posts/{id}/	        Update a post
DELETE	 /api/posts/{id}/	        Delete own post
POST	  /api/posts/{id}/like/	      Like or Unlike a post
POST	  /api/posts/{id}/comment/	        Add a comment
DELETE	/api/posts/{id}/comment/{cid}/	  Delete a comment
DELETE	/api/admin/posts/{id}/	      Admin deletes any user’s post


 Image Uploading
Make sure MEDIA_URL and MEDIA_ROOT are configured in settings.py:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

Also, update urls.py to serve media in development:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
