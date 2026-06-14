# 🚀 ATS Score Checker

An AI-powered Resume ATS (Applicant Tracking System) Score Checker built using **RAG (Retrieval-Augmented Generation)** architecture.

Upload a resume PDF and receive a detailed ATS compatibility report including:

* ATS Score
* Keyword Analysis
* Resume Strengths
* Improvement Suggestions
* Category-wise Evaluation
* Semantic Similarity Matching

---

## 📌 Features

✅ Resume PDF Upload

✅ ATS Compatibility Scoring

✅ Gemini-Powered Resume Analysis

✅ RAG-based Retrieval Pipeline

✅ Vector Search using Qdrant

✅ Semantic Similarity Matching

✅ Category-wise Feedback

✅ FastAPI Backend

✅ React Frontend

---

## 🏗️ System Architecture

```text
Resume PDF
    │
    ▼
PyPDF Text Extraction
    │
    ▼
LangChain Chunking
    │
    ▼
Gemini Embeddings
    │
    ▼
Qdrant Vector Database
    │
    ▼
Cosine Similarity Retrieval
    │
    ▼
Gemini LLM Analysis
    │
    ▼
ATS Score + Recommendations
```

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* CSS

### Backend

* FastAPI
* Python

### AI / RAG

* Gemini 2.0 Flash
* Gemini Embeddings
* LangChain
* Qdrant

### Data Processing

* PyPDF
* NumPy

---

## 📂 Project Structure

```text
ATS-Checker/
│
├── backend/
│   ├── app.py
│   ├── ats_engine.py
│   ├── rag_pipeline.py
│   ├── prompts.py
│   ├── requirements.txt
│   ├── uploads/
│   └── vectorstore/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── App.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/rushi-3333/ATS-Score-Checker.git

cd ATS-Score-Checker
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Run the backend:

```bash
python app.py
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 📊 ATS Analysis Workflow

### Step 1

User uploads a resume PDF.

### Step 2

PDF text is extracted using PyPDF.

### Step 3

Resume content is chunked using LangChain.

### Step 4

Chunks are converted into embeddings using Gemini Embeddings.

### Step 5

Vectors are stored inside Qdrant.

### Step 6

Relevant ATS criteria are retrieved using semantic search.

### Step 7

Cosine similarity scores are calculated.

### Step 8

Gemini generates ATS feedback and scoring.

---

## 📡 API Endpoint

### Analyze Resume

```http
POST /api/analyze
```

Request:

```text
multipart/form-data
```

Field:

```text
file → PDF Resume
```

Sample Response:

```json
{
  "success": true,
  "data": {
    "overall_score": 82,
    "strengths": [],
    "improvements": [],
    "summary": ""
  }
}
```

---

## 📈 Future Improvements

* Job Description Matching
* Resume Ranking
* Multiple Resume Comparison
* Interview Question Generation
* Resume Rewriting Suggestions
* Docker Deployment
* Cloud Vector Database Support

---

## 🧠 Skills Demonstrated

* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)
* Vector Databases
* Semantic Search
* FastAPI Development
* React Development
* Prompt Engineering
* Embedding Models
* Cosine Similarity Search

---

## 🤝 Contributing

Pull requests and suggestions are welcome.

For major changes, please open an issue first.

---

⭐ If you found this project useful, consider giving it a star.
