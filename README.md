🛒 E-Commerce Micro-services Platform (Dockerized)
📌 Project Overview
This project implements a fully containerized e-commerce micro-services platform using Docker and Docker Compose.
The goal is to demonstrate best practices for building, orchestrating, securing, and running a multi-container application with persistent data, service communication, caching, and health monitoring.
All services start and run with a single command:
docker-compose up -d

🎯 Learning Objectives Achieved
This project demonstrates:
    • Custom Dockerfiles for all services
    • Multi-stage Docker builds to reduce image size
    • Docker Compose orchestration
    • Inter-container communication via a custom bridge network
    • Persistent storage using named volumes
    • Redis caching for improved performance
    • Health checks and service monitoring
    • Secure containers using non-root users
    • Environment-based configuration using .env
    • Resource limits (CPU & memory)
    • Proper startup ordering with depends_on and health conditions





🏗️ Project Architecture
                ┌──────────────┐
                │   Frontend   │
                │  (HTML/JS)   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ API Gateway  │
                │ (Flask/Node) │
                └──────┬───────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────┐              ┌──────────────┐
│ Product API  │◀───────────▶     Redis      |
│ (Node/Python)│   Cache      │    (Cache)   | 
└──────┬───────┘              └──────────────┘
       │
       ▼
┌──────────────┐
│ PostgreSQL   │
│  Database    │
└──────────────┘
Key Design Decisions
    • API Gateway acts as the single entry point for security and routing
    • Redis caches product queries to reduce database load
    • PostgreSQL stores all product and order data with persistent volumes
    • Custom Docker Network ensures isolated and secure service communication
    • Health checks ensure services start only when dependencies are ready


📂 Project Structure
ecommerce-docker/
├── README.md
├── .env
├── .gitignore
├── docker-compose.yml
├── database/
│   ├── Dockerfile
│   └── init.sql
├── product-service/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json / requirements.txt
│   └── src/
├── api-gateway/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt / package.json
│   └── src/
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── public/
└── scripts/
    └── test-endpoints.sh

⚙️ Step-by-Step Execution Guide
1️⃣ Clone the Repository
git clone <your-repo-url>
cd ecommerce-docker

2️⃣ Environment Configuration
Create a .env file in the root directory:
POSTGRES_DB=ecommerce
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123

DB_HOST=postgres
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

PRODUCT_SERVICE_URL=http://product-service:5000
API_GATEWAY_PORT=8080
FRONTEND_PORT=3000

3️⃣ Database Setup (PostgreSQL)
    • PostgreSQL is built using a custom Dockerfile
    • Database initialized using init.sql
    • Includes at least 10 sample products
    • Uses a named volume for persistence
Verification:
docker volume ls

4️⃣ Product Service
    • RESTful API built with N’ode.js or Python
    • Uses multi-stage Docker build
    • Runs as a non-root user
    • Connects to PostgreSQL
    • Implements Redis caching for GET requests
Available Endpoints
GET    /api/products
GET    /api/products/:id
GET    /api/products/category/:category
POST   /api/products

5️⃣ Redis Cache
    • Used to cache product queries
    • Persistent storage via named volume
    • Cache hit/miss logged in application logs

6️⃣ API Gateway
    • Single entry point for all external requests
    • Routes requests to Product Service
    • Implements:
        ◦ Request logging
        ◦ (Optional) rate limiting
    • Prevents direct access to internal services

7️⃣ Frontend
    • Simple HTML/CSS/JS interface
    • Displays:
        ◦ Product list
        ◦ Product details
    • Communicates only with API Gateway
    • Served via containerized web server

8️⃣ Build & Run the Application
docker-compose up -d --build

🧪 Testing & Validation
Check Running Containers
docker-compose ps
Check Networks
docker network ls
Check Volumes
docker volume ls

API Testing (Using curl)
curl http://localhost:8080/api/products
curl http://localhost:8080/api/products/1
curl http://localhost:8080/api/products/category/electronics

Verify Redis Caching
docker logs product-service
docker logs redis
Look for cache HIT / MISS messages.

Verify Data Persistence
docker-compose down
docker-compose up -d
Products should still exist after restart.

Monitor Resource Limits
docker stats

🔐 Security Best Practices
    • Containers run as non-root users
    • Internal services not exposed externally
    • Environment variables used instead of hardcoding secrets
    • Minimal base images used in multi-stage builds

📸 Proof of Functionality
Include screenshots or video showing:
    • docker-compose ps (all healthy)
    • API responses working
    • Frontend displaying products
    • Redis caching logs
    • Data persistence after restart

✅ Deliverables Checklist
    • Custom Dockerfiles
    • Multi-stage builds
    • Docker Compose orchestration
    • Health checks
    • Persistent volumes
    • Custom network
    • API Gateway routing
    • Redis caching
    • Frontend integration
    • Complete documentation
