# Educated Guess - Three-Tier Media Platform

[![Frontend CI/CD](https://github.com/your-org/educated-guess/actions/workflows/github-actions-frontend.yaml/badge.svg)](https://github.com/your-org/educated-guess/actions)
[![Backend CI/CD](https://github.com/your-org/educated-guess/actions/workflows/github-actions-backend.yaml/badge.svg)](https://github.com/your-org/educated-guess/actions)

A modern educational media platform featuring a split-screen UI, built with React, FastAPI, and MongoDB, deployed on Azure Kubernetes Service.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Cloud Platform                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │      Azure Kubernetes Service (AKS)                    │ │
│  │                                                          │ │
│  │  ┌──────────────────┐       ┌──────────────────────┐  │ │
│  │  │   Frontend Pods  │       │   Backend Pods       │  │ │
│  │  │   (React + Nginx)│◄──────┤   (FastAPI + Python) │  │ │
│  │  │   Replicas: 2    │       │   Replicas: 3        │  │ │
│  │  └────────▲─────────┘       └──────────┬───────────┘  │ │
│  │           │                             │              │ │
│  │  ┌────────┴──────────────────────────┐ │              │ │
│  │  │   Ingress Controller (NGINX)      │ │              │ │
│  │  │   • TLS Termination               │ │              │ │
│  │  │   • Path-based Routing            │ │              │ │
│  │  └───────────────────────────────────┘ │              │ │
│  └──────────────────────────────┬──────────────────────────┤
│                                 │                           │
│                                 │                           │
│  ┌──────────────────────────────▼──────────────────────────┐│
│  │         MongoDB VM (Ubuntu 22.04)                       ││
│  │  • Database: educated_guess                             ││
│  │  • Secured with UFW firewall                            ││
│  │  • Automated backups                                    ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Frontend (React)
- ✅ Split-screen layout with book-stack navigation
- ✅ Smooth animations with Framer Motion
- ✅ Responsive design for all devices
- ✅ Modern gradient-based UI
- ✅ JWT authentication
- ✅ Dynamic content loading

### Backend (FastAPI)
- ✅ RESTful API with automatic OpenAPI documentation
- ✅ JWT-based authentication
- ✅ MongoDB integration with Motor (async)
- ✅ Layered architecture (routes, services, models)
- ✅ Health check endpoints for Kubernetes

### Database (MongoDB)
- ✅ Document-based storage
- ✅ Indexed collections for performance
- ✅ Automated backups
- ✅ Secure remote access

### Infrastructure
- ✅ Containerized with Docker
- ✅ Kubernetes-ready manifests
- ✅ Horizontal Pod Autoscaling
- ✅ CI/CD with GitHub Actions
- ✅ Ingress controller for routing

## 📁 Project Structure

```
educated-guess/
├── frontend/                # React application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── hooks/          # Custom React hooks
│   ├── Dockerfile
│   └── package.json
│
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/v1/         # API routes
│   │   ├── core/           # Configuration & security
│   │   ├── models/         # Data models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── Dockerfile
│   └── requirements.txt
│
├── database/               # MongoDB setup
│   ├── schema.json
│   ├── seed_data.json
│   └── init_db.py
│
├── infrastructure/         # Kubernetes & deployment
│   ├── aks/
│   │   ├── deployment/    # K8s deployments
│   │   └── service/       # K8s services
│   ├── vm/                # MongoDB VM scripts
│   └── ci-cd/             # CI/CD pipelines
│
└── docs/                   # Documentation
    ├── ARCHITECTURE.md
    ├── LOCAL_DEVELOPMENT.md
    └── AKS_DEPLOYMENT.md
```

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Framer Motion, Axios |
| Backend | Python 3.11, FastAPI, Motor, Pydantic |
| Database | MongoDB 7.0 |
| Container | Docker, Multi-stage builds |
| Orchestration | Kubernetes (AKS) |
| Ingress | NGINX Ingress Controller |
| CI/CD | GitHub Actions |
| Cloud | Microsoft Azure |

## 🏃 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/educated-guess.git
   cd educated-guess
   ```

2. **Start MongoDB locally**
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   
   # Initialize database
   cd database
   python init_db.py
   ```

3. **Start Backend**
   ```bash
   cd backend
   pip install -r app/requirements.txt
   uvicorn app.main:app --reload
   ```
   Backend runs on: http://localhost:8000
   API docs: http://localhost:8000/api/docs

4. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs on: http://localhost:3000

### Using Docker Compose

```bash
docker-compose up -d
```

## 🌐 Deployment to Azure

See [docs/AKS_DEPLOYMENT.md](docs/AKS_DEPLOYMENT.md) for complete deployment instructions.

### Prerequisites
- Azure subscription
- Azure CLI
- kubectl
- Docker

### Quick Deploy

1. **Create AKS cluster**
   ```bash
   az aks create \
     --resource-group educated-guess-rg \
     --name educated-guess-aks \
     --node-count 3 \
     --enable-addons monitoring \
     --generate-ssh-keys
   ```

2. **Set up MongoDB VM**
   ```bash
   # Follow instructions in infrastructure/vm/readme.md
   ```

3. **Build and push Docker images**
   ```bash
   # Build images
   docker build -t educatedguessacr.azurecr.io/educated-guess-frontend:latest ./frontend
   docker build -t educatedguessacr.azurecr.io/educated-guess-backend:latest ./backend
   
   # Push to ACR
   docker push educatedguessacr.azurecr.io/educated-guess-frontend:latest
   docker push educatedguessacr.azurecr.io/educated-guess-backend:latest
   ```

4. **Deploy to AKS**
   ```bash
   kubectl apply -f infrastructure/aks/deployment/
   kubectl apply -f infrastructure/aks/service/
   ```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/content` | GET | Get all content items |
| `/api/v1/content/{id}` | GET | Get specific content item |
| `/api/v1/categories` | GET | Get all categories |
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/login` | POST | User login |

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security

- JWT-based authentication
- MongoDB authentication enabled
- UFW firewall on MongoDB VM
- TLS encryption in transit
- Azure Key Vault for secrets
- Network security groups

## 📈 Monitoring

- Azure Monitor for AKS
- Application Insights
- Kubernetes Dashboard
- Log Analytics workspace

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Team

- Product Lead: [Your Name]
- Backend Developer: [Your Name]
- Frontend Developer: [Your Name]
- DevOps Engineer: [Your Name]

## 🆘 Support

For support, email support@educatedguess.com or open an issue on GitHub.

---

**Built with ❤️ using React, FastAPI, and MongoDB**
