AutoAssist Agent
Multi-Tool AI Agent with RAG, Redis Memory & ReAct Reasoning

Python  |  FastAPI  |  LangChain  |  ChromaDB  |  Redis  |  React  |  Docker

Overview
AutoAssist Agent is an autonomous AI agent system that independently plans and executes multi-step tasks using the ReAct (Reason, Act, Observe) reasoning loop. The agent uses Claude API to decide which tools to invoke, executes them, and synthesizes results into a final answer without human instruction between steps.

Features
-	ReAct Agent Loop: Claude API autonomously selects tools using stop_reason detection
-	RAG Pipeline: Upload documents and ask questions; ChromaDB retrieves relevant context via vector similarity
-	Redis Memory: Persistent conversation history across sessions with 1-hour TTL
-	3 Built-in Tools: Document search, data analysis, web search
-	REST API: FastAPI backend with full CORS support
-	React Frontend: Clean chat UI showing tool-use steps transparently
-	Docker Ready: One-command deployment with docker-compose

Architecture
User Input
    |
React Frontend (localhost:5173)
    | axios POST /chat
FastAPI Backend (localhost:8000)
    |
Redis  <--  load/save conversation history
    |
run_agent()  --  ReAct Loop
    |
Claude API (claude-opus-4-5)
    | tool_use
execute_tool()
    |-- search_documents  -->  ChromaDB (RAG)
    |-- analyze_data      -->  Data analysis
    |-- web_search        -->  Web results
    |
Final Answer  -->  Frontend

Tech Stack
Layer	Technology
AI Agent	Anthropic Claude API (claude-opus-4-5)
RAG	LangChain + ChromaDB
Memory	Redis (1-hour TTL)
Backend	FastAPI + Uvicorn
Frontend	React + Vite + Axios
Deployment	Docker + Docker Compose

Project Structure
autoassist-agent/
    backend/
        main.py          FastAPI app and endpoints
        agent.py         ReAct agent loop
        tools.py         Tool definitions and execution
        rag.py           ChromaDB RAG pipeline
        memory.py        Redis conversation memory
        requirements.txt
    frontend/
        src/
            App.jsx      React chat UI
    docker-compose.yml
    README.md

Quick Start
1. Clone the repo
git clone https://github.com/liqzheng/autoassist-agent.git
cd autoassist-agent

2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env file in backend/:
ANTHROPIC_API_KEY=your_api_key_here
REDIS_URL=redis://localhost:6379

Start backend:
python -m uvicorn main:app --reload

3. Frontend setup
cd frontend
npm install
npm run dev

4. Or run with Docker
docker-compose up --build

5. Start everything (manual)
Open two terminal windows:

Terminal 1 - Start backend:
cd ~/Desktop/autoassist-agent/backend
source venv/bin/activate
./venv/bin/python -m uvicorn main:app --reload

Terminal 2 - Start frontend:
cd ~/Desktop/autoassist-agent/frontend
npm run dev

Then open your browser and go to: http://localhost:5173

API Endpoints
Method	Endpoint	Description
GET	/	Health check
POST	/chat	Send message to agent
POST	/upload	Upload document to RAG
DELETE	/session/{id}	Clear conversation history

Key Implementation Details
ReAct Loop (agent.py)
Iteratively calls Claude API and checks stop_reason to determine whether to execute tools or return a final answer. Maximum 5 iterations to prevent infinite loops. Tool results are appended to message history so Claude can reason over them in the next iteration.

RAG Pipeline (rag.py)
Documents are chunked into 500-character segments, embedded via ChromaDB's default embedding function (all-MiniLM-L6-v2), and retrieved by cosine similarity at query time. Supports multiple documents with metadata tagging.

Redis Memory (memory.py)
Conversation history is serialized as JSON and stored in Redis with a 1-hour TTL. This enables persistent multi-turn context without relying on in-memory state, allowing the backend to scale horizontally.

Author
Liqiong (Ella) Zheng
MS Computer Science @ Northeastern University
GitHub: github.com/liqzheng
LinkedIn: linkedin.com/in/ella-z
