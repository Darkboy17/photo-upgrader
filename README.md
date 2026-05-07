# 🚀 Photo Upgrader — AI-Powered Studio Shot Generator

<p align="center">
  Transform low-quality product images into clean, studio-quality visuals using AI.
</p>

---

## 🌐 Live Demo
👉 Live link: https://photo-upgrader-three.vercel.app  
👉 Backend API: https://photo-upgrader-api.duckdns.org/docs

---

## ✨ Features

- 📤 Drag & drop image upload
- 🎨 AI-powered relighting (studio-quality outputs)
- 🔄 Before / After interactive viewer (hold-to-compare)
- 🔍 Fullscreen image preview
- ⚡ Async job processing with polling
- 🧠 Modular AI provider architecture
- 🎯 Semi-production-grade UI

---

## 🧠 Tech Stack

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Vercel (Deployment)

### Backend
- FastAPI
- Bria AI (Relighting API)
- Python Async Pipeline

### Infrastructure
- Docker
- Oracle Cloud VM
- Nginx (Reverse Proxy + SSL)

---

## 🏗️ Architecture

```
Frontend (Next.js)
      ↓
Next.js API Routes (Proxy)
      ↓
FastAPI Backend
      ↓
Bria AI (Relighting)
      ↓
Storage + Response
```

---

## ⚙️ Local Setup

### 1. Clone Repo

```bash
git clone https://github.com/Darkboy17/photo-upgrader.git
cd photo-upgrader
```

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

 Create a .env file and place it in the root directory (backend). Add the following:

 ```bash
APP_NAME=Photo Upgrader API
APP_ENV=development
APP_DEBUG=true

BACKEND_BASE_URL=http://localhost:8000

CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

MAX_UPLOAD_MB=12
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/webp

STORAGE_INPUT_DIR=storage/inputs
STORAGE_OUTPUT_DIR=storage/outputs


BRIA_API_KEY=get_your_bria_api_key
DEFAULT_PROVIDER=bria_relight

BRIA_LIGHT_TYPE=soft overcast daylight lighting
BRIA_LIGHT_DIRECTION=front
 ```

Then run the backend:
```bash
.\run.ps1
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create a .env.local file in the root directory (fronted). Add the following:

```bash
BACKEND_API_URL=http://localhost:8000
```

Then run the frontend:
```bash
npm run dev
```

---

## 🔐 Environment Variables

### Backend (`.env`)

```
BRIA_API_KEY=
BACKEND_BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
DEFAULT_PROVIDER=bria_relight
```

### Frontend (`.env.local`)

```
BACKEND_API_URL=http://localhost:8000
```

---

## 🎯 Key Learnings

- Designing scalable AI pipelines
- Handling async processing with polling
- Managing image transformations efficiently
- Deploying full-stack apps with Docker + cloud VM
- Building modular provider-based architecture

---

## 🔮 Future Improvements

- 🧠 Local GPU pipeline (Stable Diffusion / Real-ESRGAN)
- 🎨 Advanced background generation
- 📊 Usage analytics dashboard
- ⚡ Batch processing support

---

## 🧑‍💻 Author

**Kordor Pyrbot**

---

## ⭐ If you like this project
Give it a star on GitHub ⭐
