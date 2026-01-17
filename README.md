# 🚀 BOL7 Technologies AI Assistant - RAG System

A production-ready **Retrieval Augmented Generation (RAG)** system built with Django, PostgreSQL, pgvector, and Google Gemini AI. This system enables semantic search over company documents and generates natural language responses using vector embeddings and large language models.

## 🎯 Project Overview

This AI-powered assistant allows users to ask questions about BOL7 Technologies and receive accurate, context-aware responses by:
1. Converting queries to vector embeddings
2. Searching a PostgreSQL database using semantic similarity (HNSW algorithm)
3. Retrieving the most relevant documents
4. Generating natural language responses using Google Gemini LLM

## ✨ Features

- **Vector Embeddings**: Text converted to 768-dimensional vectors using Google Gemini
- **Semantic Search**: Find relevant information based on meaning, not just keywords
- **HNSW Indexing**: Fast approximate nearest neighbor search
- **Multilingual Support**: Automatic language detection (English, Hindi, Spanish, Chinese, Russian, etc.)
- **RAG Architecture**: Combines retrieval and generation for accurate responses
- **Docker Support**: PostgreSQL + pgvector running in containers
- **Clean UI**: Simple, functional interface for querying

## 🛠️ Tech Stack

- **Backend**: Django 5.x, Python 3.x
- **Database**: PostgreSQL 17 + pgvector extension
- **AI/ML**: Google Gemini API (Embeddings + LLM)
- **Vector Search**: HNSW algorithm, Cosine similarity
- **Infrastructure**: Docker, Docker Compose
- **Frontend**: HTML5, JavaScript (Vanilla)

## 📋 Prerequisites

- Python 3.8+
- Docker Desktop
- Google Gemini API Key (free tier available)
- Git















## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/bol7-rag-system.git
cd bol7-rag-system
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL with Docker
```bash
docker run -d \
  --name my-postgres \
  -e POSTGRES_USER=badal \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=Vector_Embedding \
  -p 5433:5432 \
  pgvector/pgvector:pg17
```

### 5. Create HNSW Index
```bash
docker exec -it my-postgres psql -U badal -d Vector_Embedding
```
```sql
CREATE EXTENSION vector;
CREATE INDEX company_documents_vector_idx 
ON company_documents 
USING hnsw (vector vector_cosine_ops);
\q
```

### 6. Configure Environment Variables

Create `.env` file in project root:
```
GEMINI_API_KEY=your_api_key_here
```

Get your free API key: https://makersuite.google.com/app/apikey

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Start Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## 📊 Project Structure
```
bol7-rag-system/
├── mysite/
│   ├── models.py           # Database models (CompanyDocument)
│   ├── views.py            # API endpoints (search, add_document)
│   ├── utils.py            # Helper functions (embeddings, LLM)
│   ├── urls.py             # URL routing
│   └── templates/
│       └── index.html      # Frontend UI
├── manage.py
├── requirements.txt
├── .env                    # API keys (not in git)
├── README.md
└── .gitignore
```

## 🔧 How It Works

### System Architecture
```
User Query → Gemini Embedding → Vector Search (HNSW) 
→ Top-K Retrieval → Context + Query → Gemini LLM 
→ Natural Language Response
```

### Detailed Flow

1. **Data Ingestion** (Admin)
   - Company information stored in database
   - Text converted to 768-dim vectors
   - Saved with metadata (language, timestamp)

2. **User Query**
   - User asks question (e.g., "Where is BOL7 located?")
   - Query converted to vector using Gemini
   - Language automatically detected

3. **Vector Search**
   - HNSW algorithm finds similar vectors
   - Cosine similarity calculated
   - Top-2 most relevant documents retrieved

4. **RAG Generation**
   - Retrieved context + user query sent to LLM
   - Gemini generates natural language response
   - Response returned to user

5. **Output Display**
   - AI-generated answer
   - Query details (text, language, vector)
   - Retrieved context with similarity scores




## 📝 Example Usage

**Query:** "Who are the founders of BOL7?"

**AI Response:** "BOL7 Technologies was founded by Hemant Gupta and Pramod Saggar in September 2010."

**Retrieved Context:**
- Match 1: "BOL7 founders are Hemant Gupta and Pramod Saggar" (95% similarity)
- Match 2: "BOL7 was founded on September 29, 2010" (87% similarity)


## 🔑 Key Components

### Vector Embeddings
- Model: `text-embedding-004` (Google Gemini)
- Dimensions: 768
- Speed: ~400-500ms per embedding

### Search Algorithm
- **HNSW**: Hierarchical Navigable Small World graphs
- **Similarity**: Cosine similarity
- **Threshold**: 30% minimum match

### LLM
- Model: `gemini-2.0-flash`
- Task: Context-aware response generation
- Approach: RAG (Retrieval Augmented Generation)

## 📦 requirements.txt
```
Django==5.2
psycopg2-binary==2.9.9
pgvector==0.3.6
google-generativeai==0.8.3
langdetect==1.0.9
numpy==1.26.4
python-dotenv==1.0.1
```

## 🐳 Docker Commands
```bash
# Start database
docker start my-postgres

# Stop database
docker stop my-postgres

# View logs
docker logs my-postgres

# Access PostgreSQL shell
docker exec -it my-postgres psql -U badal -d Vector_Embedding
```

## 🎓 Learning Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Google Gemini API](https://ai.google.dev/)
- [RAG Systems Explained](https://www.promptingguide.ai/research/rag)
- [HNSW Algorithm](https://arxiv.org/abs/1603.09320)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Badal Chauhan**
- Python & AI Developer
- GitHub: [Badal-2]([https://github.com/Badal-2]) 
