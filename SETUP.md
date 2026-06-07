# Architecture GPT — Setup Guide

## Prerequisites

- **Node.js** (v18+) — [Download](https://nodejs.org/)
- **Python** (3.12+) — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/)

---

## Project Structure

```
architecture-gpt/
├── frontend/          # React + TypeScript (Vite)
├── backend/           # FastAPI (Python)
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   └── example.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
└── setup.md           # This file
```

---

## Frontend Setup (React + Vite + TypeScript)

### 1. Install dependencies

```powershell
cd frontend
npm install
```

### 2. Start the dev server

```powershell
npm run dev
```

The app will be available at **http://localhost:5173**

### 3. Build for production

```powershell
npm run build
```

Output goes to `frontend/dist/`.

---

## Backend Setup (FastAPI + Python)

### 1. Create a virtual environment

```powershell
cd backend
py -m venv venv
```

### 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

> **Note:** If you get a permissions error, run this first:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the dev server

```powershell
uvicorn app.main:app --reload
```

- API available at **http://localhost:8000**
- Swagger docs at **http://localhost:8000/docs**
- ReDoc at **http://localhost:8000/redoc**

---

## Running the Full Stack

Open **two terminal windows**:

| Terminal | Commands |
|---|---|
| **Frontend** | `cd frontend` → `npm run dev` |
| **Backend** | `cd backend` → `.\venv\Scripts\Activate.ps1` → `uvicorn app.main:app --reload` |

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

The backend is configured with CORS to accept requests from the frontend's `localhost:5173`.

---

## Environment Variables

Backend settings are in `backend/.env`:

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | Architecture GPT API | Application name |
| `DEBUG` | True | Enable debug mode |
| `FRONTEND_URL` | http://localhost:5173 | Frontend URL for CORS |

---

## Troubleshooting

### `py` command not found
Ensure Python is installed and the "Add Python to PATH" option was checked during installation. You can also try `python -m venv venv` instead.

### PowerShell execution policy error
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### npm install fails
Delete `node_modules/` and `package-lock.json`, then retry:
```powershell
rm -r node_modules
rm package-lock.json
npm install
```

### pip install fails
Ensure the virtual environment is activated (you should see `(venv)` in your terminal prompt).
