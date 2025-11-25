# Real-Time Analytics Dashboard

A high-throughput real-time analytics system built with **Flask**, **Redis**, **WebSockets**, and a **React dashboard**.  
Designed to stream live business metrics with **under 100ms latency**, featuring dynamic visualizations, caching logic, and scalable architecture for monitoring multiple data sources.

---

## 📌 Project Overview

### Backend (Flask + Flask-SocketIO)

The backend handles:
- Real-time WebSocket communication using Socket.IO
- Redis Pub/Sub event consumption
- Broadcasting live metrics to clients
- REST API for recent and aggregated metrics
- Simulated high-throughput metric generation

**Key Backend Components**
- `backend/app.py`  
  - WebSocket server  
  - Redis listener  
  - REST endpoints:  
    - `GET /api/health`  
    - `GET /api/metrics/recent`  
    - `GET /api/metrics/aggregate?window=60`
- `backend/generator.py`  
  - Simulates high-speed event generation  
  - Publishes metrics to Redis Pub/Sub  
- `backend/requirements.txt`
- `backend/.env`
- `backend/tests/test_api.py`
- `backend/Dockerfile`

---

### Frontend (React + Chart.js)

The frontend provides:
- Real-time metric visualization
- Interactive charts using `react-chartjs-2`
- Live counters for various metrics
- Real-time event logs (last 200 events)

**Key Frontend Components**
- `frontend/src/App.js`
- `frontend/src/components/Dashboard.js`
- `frontend/src/components/MetricChart.js`
- `frontend/src/index.js`
- `frontend/package.json`
- `frontend/Dockerfile`

---

### Dev & Infrastructure

Included for easy development and automation:
- `docker-compose.yml`  
  - Starts Redis, Backend, and Frontend together
- `.github/workflows/ci.yml`  
  - GitHub Actions pipeline for backend tests
- Top-level project files:  
  - `README.md`  
  - `LICENSE`  
  - `.gitignore`

---

## 🚀 Quick Start

### 1. Requirements
- Docker  
- Docker Compose  
- Node.js (only needed for manual frontend run)  
- Python 3.11 (only needed for manual backend run)

### 2. Start Entire Stack
```bash
docker-compose up --build
```

### 3. Access the Application
| Service | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:5000 |
| WebSocket | ws://localhost:5000 |

---

## ⚙️ Architecture Summary

### Real-Time Data Flow

1. `generator.py` produces random metrics at high speed.
2. Metrics are published to a Redis Pub/Sub channel.
3. Backend (`app.py`):
   - Listens to Redis  
   - Stores recent metrics in Redis cache  
   - Broadcasts events to WebSocket clients
4. Frontend receives WebSocket data and:
   - Updates charts instantly  
   - Shows counters  
   - Displays live logs  

**Target latency:** < **100ms** end-to-end.

---

## 🔧 Optional Enhancements

Possible improvements for future expansion:

### Production Hardening
- JWT authentication / API keys  
- HTTPS + reverse proxy  
- Redis ACL / TLS  
- Rate limiting and throttling  

### Persistent Storage
- DynamoDB  
- PostgreSQL  
- Long-term materialized aggregates  

### Real Data Stream Integration
- AWS Kinesis  
- Apache Kafka  
- EventBridge  

### DevOps Additions
- Docker Compose overrides  
- Kubernetes manifests  
- GitHub Actions CI/CD to AWS ECS, Fargate, or EKS  

---

If you want an **architecture diagram**, **API documentation section**, or **installation steps for AWS deployment**, I can generate that too.
