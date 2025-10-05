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

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Create environment variables
Create a `.env` file at the project root:
```env
SECRET_KEY=your secret key
DEBUG=True
POSTGRES_DB=onlinepolls
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

👉 Generate your own SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4. Run with Docker
```bash
docker-compose up --build
```

Your services will be available at:
* API → http://127.0.0.1:8000/api/
* Swagger UI → http://127.0.0.1:8000/api/docs/
* Django Admin → http://127.0.0.1:8000/admin/

5. Create superuser
In another terminal:
```bash
docker-compose exec web python manage.py createsuperuser
```
You'll be prompted to enter:
* Username (e.g., "admin")
* Email address (optional, can be left blank)
* Password (create a strong password with at least 8 characters)

Note: Make sure to remember these credentials as you'll need them to:
* Access the Django admin interface
* Generate JWT tokens for API authentication
* Create and manage polls

You can verify the superuser was created by checking again:
docker-compose exec web python manage.py shell -c "from django.contrib.auth.models import User; print('Superusers:', [user.username for user in User.objects.filter(is_superuser=True)])"


🚀 Deploying to Render
1. Create a new Web Service on Render:
   * Click "New +" button
   * Select "Web Service" (important: not Static Site)
   * Connect your GitHub repository if not already connected
   * Select your repository from the list

2. On the "Create Web Service" page:
   * Enter a name for your service (e.g., "project-nexus")
   * Under "Environment" section:
     - Look for Environment selection (radio buttons/dropdown)
     - Choose "Python" (NOT "Docker" or other options)
   * Select Branch: `master`
   * Leave Root Directory empty

3. Build & Deploy settings:
   * Build Command: `./build.sh`  # Will appear after selecting Python environment
   * Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
   * Set Auto-Deploy to On

4. Configure Environment Variables:
   ```
   SECRET_KEY=oo+cyo392vt5(k4*oz(gc8f!^x6eih_q%j9hmn%$+04tm_$h*&
   DEBUG=False
   DATABASE_URL=postgres://your-render-postgres-url
   ALLOWED_HOSTS=.onrender.com,your-custom-domain
   CSRF_TRUSTED_ORIGINS=https://*.onrender.com,http://127.0.0.1:8000
   ```

   Note: Replace `your-custom-domain` with your actual domain if you have one.
   The DATABASE_URL will be automatically added when you create and link a PostgreSQL service.

4. Create a PostgreSQL database service on Render
   * Link it to your web service
   * The DATABASE_URL will be automatically added to your environment

5. Deploy! Render will automatically:
   * Install dependencies from requirements.txt
   * Run migrations
   * Collect static files
   * Start the Gunicorn server
🔑 Authentication and API Usage
Note: Replace the base URL in these examples:
- Local testing: use `http://127.0.0.1:8000`
- Render deployment: use `https://my-app-name.onrender.com`

1. First, obtain a JWT token using your superuser credentials:
```bash
# Use the superuser credentials you created earlier
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "my_superuser_password"}'
```
✅ Response:
```json
{
    "refresh": "eyJ0eXAiOiJKV1Qi...",
    "access": "eyJ0eXAiOiJKV1Qi..."
}
```
Save the `access` token for subsequent requests.

📖 Usage Examples

2. Create a poll with choices (requires authentication)
```bash
curl -X POST http://127.0.0.1:8000/api/polls/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Best programming language?",
    "description": "Vote your favorite",
    "choices": ["Python", "JavaScript", "Go"],
    "is_active": true
  }'
```

3. List all polls (public endpoint, no authentication required)
```bash
curl -X GET http://127.0.0.1:8000/api/polls/
```

4. Vote on a poll (requires authentication)
```bash
curl -X POST http://127.0.0.1:8000/api/vote/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"poll": 1, "choice": 2}'
```

5. Get poll results (public endpoint, no authentication required)
```bash
curl -X GET http://127.0.0.1:8000/api/polls/1/results/
``` 
✅ Response:
{ "poll": "Best programming language?", "results": [ {"id": 1, "choice": "Python", "votes": 0}, {"id": 2, "choice": "JavaScript", "votes": 1}, {"id": 3, "choice": "Go", "votes": 0} ] } 
📚 API Docs
Interactive API docs (Swagger UI) available at:
http://127.0.0.1:8000/api/docs/ 


Project Nexus – Online Polls System
Built as part of a Django Backend Pro Dev Capstone Project.