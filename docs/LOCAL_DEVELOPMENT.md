# Local Development Guide

## Overview
This guide covers setting up the Educated Guess platform on your local machine for development.

## Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Node.js | 18+ | `node --version` |
| Python | 3.11+ | `python --version` |
| MongoDB | 7.0+ | `mongod --version` |
| Docker | 20+ | `docker --version` |
| Git | Latest | `git --version` |

## Quick Start (Docker Compose)

The fastest way to get started is using Docker Compose:

```bash
# Clone repository
git clone https://github.com/your-org/educated-guess.git
cd educated-guess

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- MongoDB: localhost:27017

## Manual Setup

### 1. MongoDB Setup

#### Option A: Docker
```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:7.0
```

#### Option B: Local Installation
```bash
# Ubuntu/Debian
sudo apt-get install -y mongodb-org

# macOS
brew install mongodb-community@7.0

# Windows
# Download from https://www.mongodb.com/try/download/community

# Start MongoDB
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

### 2. Initialize Database

```bash
cd database

# Install Python MongoDB driver
pip install pymongo motor

# Initialize database with seed data
python init_db.py
```

Expected output:
```
🔗 Connected to MongoDB: educated_guess
📁 Setting up categories...
  ✓ Inserted 4 categories
👤 Setting up authors...
  ✓ Inserted 3 authors
📝 Setting up content items...
  ✓ Inserted 12 content items
✅ Database initialization complete!
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt

# Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env file with your settings
# Update MongoDB URL if needed

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will start on: http://localhost:8000

**Test the backend:**
```bash
curl http://localhost:8000/
curl http://localhost:8000/api/health
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Start development server
npm run dev
```

Frontend will start on: http://localhost:3000

**Note:**  Vite may use port 5173 if 3000 is occupied.

## Development Workflow

### Backend Development

#### Project Structure
```
backend/app/
├── api/v1/           # API routes
│   ├── content_routes.py
│   └── auth_routes.py
├── core/             # Core functionality
│   ├── config.py     # Configuration
│   ├── database.py   # DB connection
│   └── security.py   # Auth & security
├── schemas/          # Pydantic schemas
├── services/         # Business logic
└── main.py           # Entry point
```

#### Making Changes
1. Edit files in `backend/app/`
2. FastAPI auto-reloads on file changes
3. Test endpoints at http://localhost:8000/api/docs
4. Check logs in terminal

#### Adding New Endpoints
```python
# In api/v1/your_routes.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/your-endpoint")
async def your_function():
    return {"message": "Hello"}

# In main.py
from app.api.v1 import your_routes
app.include_router(your_routes.router, prefix="/api/v1")
```

### Frontend Development

#### Project Structure
```
frontend/src/
├── components/       # Reusable components
│   ├── LeftNavigation/
│   ├── ContentGrid/
│   └── HeroSection/
├── pages/            # Page components
│   ├── NetworkPage.jsx
│   ├── LibraryPage.jsx
│   └── JoinPage.jsx
├── services/         # API integration
│   ├── api.js
│   └── axios-config.js
├── hooks/            # Custom hooks
└── App.jsx           # Main app
```

#### Making Changes
1. Edit files in `frontend/src/`
2. Vite auto-reloads on file changes
3. View changes at http://localhost:3000
4. Check browser console for errors

#### Adding New Pages
```jsx
// 1. Create page in src/pages/YourPage.jsx
import React from 'react';

const YourPage = () => {
  return <div>Your Content</div>;
};

export default YourPage;

// 2. Add route in App.jsx
import YourPage from './pages/YourPage';

// In Routes:
<Route path="/your-route" element={<YourPage />} />
```

## Common Tasks

### Adding New Content
```bash
# Using MongoDB CLI
mongosh

use educated_guess

db.content_items.insertOne({
  title: "Your Title",
  description: "Your description",
  category_id: "category_id_here",
  author_id: "author_id_here",
  image_url: "https://example.com/image.jpg",
  tags: ["tag1", "tag2"],
  created_at: new Date()
})
```

### Creating New User
```bash
# Via API
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Testing API Endpoints
```bash
# Using curl
curl http://localhost:8000/api/v1/content
curl http://localhost:8000/api/v1/categories

# With authentication
TOKEN="your-jwt-token"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/content
```

### Viewing Logs
```bash
# Backend logs (FastAPI)
# Check terminal where uvicorn is running

# Frontend logs
# Check browser console (F12)

# MongoDB logs
mongosh
db.adminCommand({ getLog: "global" })
```

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=educated_guess
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

## Troubleshooting

### Backend Won't Start
```bash
# Check MongoDB is running
mongosh

# Check port 8000 is free
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Reinstall dependencies
pip install --force-reinstall -r app/requirements.txt
```

### Frontend Won't Start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check port 3000 is free
# Windows:
netstat -ano | findstr :3000
# macOS/Linux:
lsof -i :3000
```

### Database Connection Issues
```bash
# Test MongoDB connection
mongosh mongodb://localhost:27017/educated_guess

# Check MongoDB service
# Linux:
sudo systemctl status mongod
# macOS:
brew services list
# Windows:
# Check Services app
```

### CORS Errors
- Ensure backend `ALLOWED_ORIGINS` includes frontend URL
- Restart backend after changing `.env`
- Check browser console for exact error

## Development Tips

### Hot Reload
- Both frontend and backend support hot reload
- Backend: FastAPI `--reload` flag
- Frontend: Vite HMR (Hot Module Replacement)

### API Testing
- Use Swagger UI: http://localhost:8000/api/docs
- Use Postman or Insomnia for complex requests
- Browser DevTools Network tab for debugging

### Database GUI Tools
- MongoDB Compass (Official GUI)
- Studio 3T
- Robo 3T

### VS Code Extensions
- Python (Microsoft)
- Pylance
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- ESLint

## Performance Optimization

### Backend
```python
# Use async/await for all DB operations
async def get_content():
    items = await db.content_items.find().to_list(100)
    return items

# Add indexes to frequently queried fields
await db.content_items.create_index([("title", "text")])
```

### Frontend
```javascript
// Lazy load components
const LazyComponent = React.lazy(() => import('./Component'));

// Memoize expensive computations
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);

// Debounce search input
const debouncedSearch = useDebounce(searchQuery, 500);
```

## Next Steps

Once comfortable with local development:
1. Review [AKS_DEPLOYMENT.md](AKS_DEPLOYMENT.md) for production deployment
2. Set up CI/CD pipelines
3. Configure monitoring and logging
4. Implement additional features

## Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Documentation](https://react.dev/learn)
- [MongoDB University](https://university.mongodb.com/)
- [Vite Guide](https://vitejs.dev/guide/)
