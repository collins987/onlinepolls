📊 Online Poll System (Project Nexus)
An online voting system built with Django REST Framework, PostgreSQL, and JWT authentication, containerized with Docker.
This project allows users to:
* Create polls with multiple choices
* Vote on polls (one vote per user per poll)
* View poll results in real-time
* Manage everything via a REST API with Swagger documentation
🚀 Features
* JWT-based authentication (access + refresh tokens)
* Create polls with choices in one request
* Filter polls by active/inactive status
* Vote on polls (validated: one vote per user)
* Results endpoint with live vote counts
* Swagger UI auto-generated API docs
🛠️ Tech Stack
* Backend: Django, Django REST Framework
* Auth: JWT (SimpleJWT)
* Database: PostgreSQL
* Docs: Swagger (drf-yasg)
* Deployment: Docker & Docker Compose
📦 Setup Instructions
1. Clone the repository
git clone https://github.com/your-username/online-poll-system.git cd online-poll-system 
2. Create environment variables
Create a .env file at the project root:
SECRET_KEY=your_django_secret_key DEBUG=True POSTGRES_DB=onlinepolls POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_HOST=db POSTGRES_PORT=5432 
👉 You must generate your own SECRET_KEY (use python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())").
3. Run with Docker
docker-compose up --build 
* API → http://127.0.0.1:8000/api/
* Swagger UI → http://127.0.0.1:8000/api/docs/
* Django Admin → http://127.0.0.1:8000/admin/
4. Create superuser
In another terminal:
docker-compose exec web python manage.py createsuperuser 
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
✅ To Do / Improvements
* Add pagination for polls
* Enable poll closing after expires_at
* Add unit tests with Pytest/Django TestCase
👨‍💻 Author
Project Nexus – Online Polls System
Built as part of a Django Backend Pro Dev Capstone Project.
Would you like me to also include a "Testing with Pytest" section in this README so that running one command (pytest) checks all endpoints automatically? That way you won’t rely only on curl/manual tests.