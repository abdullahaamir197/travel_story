# Travel Story App

A full-stack application to capture and share your travel memories.

## Project Structure

- **frontend**: React application (details in `frontend/travel-story-app/README.md`)
- **backend**: FastAPI Python application (details in `backend/walkthrough.md` or `backend/README.md`)

## Backend Setup (Python FastAPI)

1.  Navigate to `backend`:
    ```bash
    cd backend
    ```
2.  Create and activate virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Mac/Linux
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
5.  API runs at `http://localhost:8000`. Documentation at `http://localhost:8000/docs`.

## Frontend Setup (React + Vite)

1.  Navigate to `frontend/travel-story-app`:
    ```bash
    cd frontend/travel-story-app
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
