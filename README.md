📊 Online Poll System (Project Nexus)
An online voting system built with Django REST Framework, PostgreSQL, and JWT authentication, containerized with Docker. Production-ready with Gunicorn server and Render deployment support.

This project allows users to:
* Create polls with multiple choices
* Vote on polls (one vote per user per poll)
* View poll results in real-time
* Manage everything via a REST API with Swagger documentation
* Access secure endpoints with JWT authentication
* Deploy easily to Render or similar platforms
🚀 Features
* JWT-based authentication (access + refresh tokens)
* Create polls with choices in one request
* Filter polls by active/inactive status
* Vote on polls (validated: one vote per user)
* Results endpoint with live vote counts
* Swagger UI auto-generated API docs
🛠️ Tech Stack
* Backend: Django 5.2.6, Django REST Framework 3.16.1
* Auth: JWT (SimpleJWT 5.5.1)
* Database: PostgreSQL 15
* Server: Gunicorn 23.0.0
* Docs: Swagger (drf-yasg 1.21.11)
* Deployment: Docker & Docker Compose
* CI/CD: Render deployment ready
📦 Local Development Setup
1. Clone the repository
```bash
git clone https://github.com/collins987/online-poll-system.git
cd online-poll-system
```

2. Create environment variables
Create a `.env` file at the project root:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
POSTGRES_DB=onlinepolls
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

👉 Generate your own SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Run with Docker
```bash
docker-compose up --build
```

Your services will be available at:
* API → http://127.0.0.1:8000/api/
* Swagger UI → http://127.0.0.1:8000/api/docs/
* Django Admin → http://127.0.0.1:8000/admin/

4. Create superuser
In another terminal:
```bash
docker-compose exec web python manage.py createsuperuser
```

🚀 Deploying to Render
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:
   * Build Command: `./build.sh`
   * Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
   * Environment Variables:
     ```
     SECRET_KEY=your-secure-secret-key
     DEBUG=False
     DATABASE_URL=postgres://your-render-postgres-url
     ALLOWED_HOSTS=.onrender.com,your-custom-domain
     CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://*.your-custom-domain
     ```

4. Create a PostgreSQL database service on Render
   * Link it to your web service
   * The DATABASE_URL will be automatically added to your environment

5. Deploy! Render will automatically:
   * Install dependencies from requirements.txt
   * Run migrations
   * Collect static files
   * Start the Gunicorn server
🔑 Authentication
Before accessing protected endpoints, obtain a JWT:
curl -X POST http://127.0.0.1:8000/api/auth/token/ \ -H "Content-Type: application/json" \ -d '{"username": "admin", "password": "yourpassword"}' 
Response:
{ "refresh": "eyJ0eXAiOiJKV1Qi...", "access": "eyJ0eXAiOiJKV1Qi..." } 
Use the access token in headers:
Authorization: Bearer <access-token> 
📖 Usage Examples
1. Create a poll with choices
curl -X POST http://127.0.0.1:8000/api/polls/ \ -H "Authorization: Bearer <token>" \ -H "Content-Type: application/json" \ -d '{ "title": "Best programming language?", "description": "Vote your favorite", "choices": ["Python", "JavaScript", "Go"], "is_active": true }' 
✅ Response:
{ "id": 1, "title": "Best programming language?", "choices": [ {"id": 1, "text": "Python", "votes": 0}, {"id": 2, "text": "JavaScript", "votes": 0}, {"id": 3, "text": "Go", "votes": 0} ] } 
2. List all polls
curl -X GET http://127.0.0.1:8000/api/polls/ 
3. Vote on a poll
curl -X POST http://127.0.0.1:8000/api/vote/ \ -H "Authorization: Bearer <token>" \ -H "Content-Type: application/json" \ -d '{"poll": 1, "choice": 2}' 
4. Get poll results
curl -X GET http://127.0.0.1:8000/api/polls/1/results/ 
✅ Response:
{ "poll": "Best programming language?", "results": [ {"id": 1, "choice": "Python", "votes": 0}, {"id": 2, "choice": "JavaScript", "votes": 1}, {"id": 3, "choice": "Go", "votes": 0} ] } 
📚 API Docs
Interactive API docs (Swagger UI) available at:
http://127.0.0.1:8000/api/docs/ 


Project Nexus – Online Polls System
Built as part of a Django Backend Pro Dev Capstone Project.