## **Q2: HOW IS IT WORKING? (SHORT)**
```
USER TYPES: "Where is BOL7?"
     ↓
1. Text → Vector (Gemini API)
   "Where is BOL7?" → [0.123, -0.456, ...]
     ↓
2. pgvector + HNSW searches database
   Compares query vector with saved vectors
   SUPER FAST search!
     ↓
3. Finds Top-2 similar vectors
   "BOL7 is in Delhi" → 95% match ✅
   "BOL7 office in Noida" → 88% match ✅
     ↓
4. Retrieves matching TEXT from database
     ↓
5. Passes to Groq LLM (RAG)
   Context + Query → Natural response
     ↓
6. Bot replies: "BOL7 is located in New Delhi, India..."
```  







---


## **TECHNICAL FLOW:**
```
Database has:
├─ Text: "BOL7 is in Delhi"
├─ Vector: [0.234, -0.567, ...] (768 numbers)
└─ Saved with pgvector

User query:
├─ "Where is BOL7?" 
└─ Converts to: [0.240, -0.560, ...]

HNSW Algorithm:
├─ Compares query vector with ALL database vectors
├─ Uses cosine similarity
├─ ULTRA FAST (milliseconds!)
└─ Returns Top-2 most similar

Retrieved:
├─ Match 1: "BOL7 is in Delhi" (95%)
└─ Match 2: "Office in Noida" (88%)

Groq LLM:
├─ Takes retrieved text as context
├─ Generates natural answer
└─ Returns: "BOL7 Technologies is located..."













inside Browser These Feature Are Prebuilt Already => FOR  TTS AND  STT    

FOR STT ->  WE ARE USING OF BROWSER STT (Javascript)  Prebuilt Feature. 
FOR TTS ->  WE ARE USING OF gTTS. BUT WE COULD HAVE USED  PRE-BUILT FEATURE OF  BROWSER FOR TTS BUT WE USED OF  Gtts. 






