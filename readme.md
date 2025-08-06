🧠 EdTech Adaptive Learning Platform — Backend (FastAPI)
Welcome to the backend of the AI-driven EdTech Adaptive Learning Platform.
This system is designed to analyze student activity, evaluate answers, and provide AI-generated feedback, adaptive assessments, and chat-based course guidance using local Large Language Models (LLMs).

🚀 Features
📚 Manage Courses and Lessons (CRUD)

🧠 AI-Powered Feedback System (Answer Evaluation)

💬 Course-aware Chatbot (Ask about courses, topics, lessons)

🤖 Local LLM Integration via Ollama

🔐 JWT Authentication Ready

🛠️ Built with FastAPI, SQLAlchemy, SQLite, and Pydantic

⚙️ System Requirements
Tool	Version	Required For
Python	3.10+	Backend server
pip	Latest	Installing Python dependencies
Git	Any	Cloning the project
Ollama	Latest	Local LLM inference

📦 Installation & Setup
1️⃣ Clone the Repository

git clone https://github.com/your-username/edtech-backend.git
cd edtech-backend
2️⃣ Set Up a Virtual Environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3️⃣ Install Python Dependencies

pip install -r requirements.txt
4️⃣ Install & Run Ollama with Gemma
We use Ollama to run LLMs locally (such as gemma) for AI feedback and chat.

✅ Step-by-step:

# Download & install Ollama (choose your OS): https://ollama.com/download

# Pull the Gemma model
ollama pull gemma

# Run the model
ollama run gemma
By default, Ollama listens at:
http://localhost:11434

5️⃣ Start the Backend Server

uvicorn app.main:app --reload
Server will start at:
🔗 http://localhost:8000

🗂️ Project Structure

app/
├── main.py                 # FastAPI entrypoint
├── database.py             # DB setup (SQLAlchemy)
├── models.py               # ORM models
├── schemas.py              # Pydantic schemas
├── llm_engine.py           # Ollama LLM integration
├── ai_feedback.py          # AI Feedback logic
├── routes/
│   ├── courses.py
│   ├── lessons.py
│   └── chatbot.py
└── ...
🔍 API Routes Overview
Endpoint	Description
GET /courses	List all courses
POST /courses	Create a new course
GET /courses/{id}/lessons	Get all lessons in a course
POST /courses/{id}/lessons	Add a lesson
POST /lessons/{id}/submit-answer	Get AI feedback on student answer
GET /chatbot?query=	Ask AI about course/lesson info

🤖 How It Works
Chat & Feedback prompts are sent from the frontend to the FastAPI server.

FastAPI sends these prompts to Ollama (Gemma) via HTTP.

Ollama returns generated responses, which are then displayed to users.