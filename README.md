# Dealership Review Platform - Full-Stack Capstone

A full-stack web application for a national car dealership network. Visitors can browse dealerships across the US, filter them by state and read customer reviews. Registered users can log in and post their own reviews, and every review is tagged with a sentiment (positive, neutral or negative) by a dedicated microservice.

Built as the capstone project for the IBM Full-Stack Software Developer program.

## Features

- Browse all dealerships or filter them by state
- View a dealer's details and its customer reviews
- Sentiment analysis on every review (positive / neutral / negative)
- User registration, login and logout
- Post a review with car make, model and purchase date (logged-in users)
- Django admin for managing car makes and models
- Containerized with Docker and deployed to Kubernetes
- CI linting for Python and JavaScript with GitHub Actions

## Architecture

| Component | Technology | Port | Location |
|---|---|---|---|
| Frontend | React | served by Django | `server/frontend` |
| Web app and API proxy | Django 5, Gunicorn | 8000 | `server/djangoapp`, `server/djangoproj` |
| Dealers and reviews API | Node.js, Express, MongoDB | 3030 | `server/database` |
| Sentiment analyzer | Python, Flask, NLTK VADER | 5000 (5050 locally) | `server/djangoapp/microservices` |

The React app calls the Django endpoints under `/djangoapp/`. Django proxies dealer and review requests to the Express/MongoDB service, enriches each review with a sentiment from the Flask microservice, and stores users and car models in SQLite.

## Django API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/djangoapp/login` | Log in |
| GET | `/djangoapp/logout` | Log out |
| POST | `/djangoapp/register` | Register a new user |
| GET | `/djangoapp/get_dealers` | All dealerships |
| GET | `/djangoapp/get_dealers/<state>` | Dealerships in a state |
| GET | `/djangoapp/dealer/<id>` | Details of one dealer |
| GET | `/djangoapp/reviews/dealer/<id>` | Reviews of a dealer, with sentiment |
| POST | `/djangoapp/add_review` | Add a review (logged-in users only) |
| GET | `/djangoapp/get_cars` | Car makes and models |

## Project structure

```
server/
  database/          Express + MongoDB service (docker-compose)
  djangoapp/         Django app: views, models, restapis, microservices/
  djangoproj/        Django project settings and URLs
  frontend/          React frontend
  Dockerfile         Image for the Django app
  entrypoint.sh      Runs migrations and collectstatic on start
  deployment.yaml    Kubernetes deployment
.github/workflows/   Lint workflow
```

## Running locally

1. Start the dealers and reviews API (port 3030):

   ```bash
   cd server/database
   docker build . -t nodeapp
   docker-compose up
   ```

2. Start the sentiment analyzer (port 5050):

   ```bash
   cd server/djangoapp/microservices
   docker build -t sentianalyzer .
   docker run -d -p 5050:5000 sentianalyzer
   ```

3. Set the service URLs in `server/djangoapp/.env`:

   ```
   backend_url=http://localhost:3030
   sentiment_analyzer_url=http://localhost:5050/
   ```

4. Build the frontend:

   ```bash
   cd server/frontend
   npm install
   npm run build
   ```

5. Run Django:

   ```bash
   cd server
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

   Open http://localhost:8000.

## Deploying to Kubernetes

Build the image and push it to a container registry (the example uses IBM Cloud Container Registry):

```bash
cd server
MY_NAMESPACE=$(ibmcloud cr namespaces | grep sn-labs-)
docker build -t us.icr.io/$MY_NAMESPACE/dealership .
docker push us.icr.io/$MY_NAMESPACE/dealership
```

Set your namespace in the `image` field of `deployment.yaml`, then deploy and forward the port:

```bash
kubectl apply -f deployment.yaml
kubectl port-forward deployment.apps/dealership 8000:8000
```

The container runs `entrypoint.sh` (migrations and static files) and then serves the app with Gunicorn on port 8000. The pod must be able to reach the URLs set in `djangoapp/.env`.

## Continuous integration

The GitHub Actions workflow in `.github/workflows` runs `flake8` on all Python files and JSHint on the Express service on every push and pull request to `main`.

## Author

**Farhad Rahmani** - [GitHub](https://github.com/farhadrahmanii) - [LinkedIn](https://www.linkedin.com/in/farhadrahmanii)
