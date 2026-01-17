import google.generativeai as genai
from django.conf import settings
from langdetect import detect
import numpy as np
import os 
genai.configure(api_key=settings.GEMINI_API_KEY)
from gtts import gTTS
import os
import uuid
import pdfplumber
from .models import CompanyDocument



def text_to_vector(text):
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        raise Exception(f"Embedding generation failed: {str(e)}")


def detect_language(text):
    try:
        lang_code = detect(text)
        lang_names = {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh-cn': 'Chinese',
            'ar': 'Arabic',
            'bn': 'Bengali',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean'
        }
        
        return lang_names.get(lang_code, lang_code.upper())
    except:
        return "Unknown"


def calculate_similarity(vector1, vector2):
    vec1 = np.array(vector1)
    vec2 = np.array(vector2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    similarity = dot_product / (norm1 * norm2)
    return float(similarity)

def generate_llm_response(query, context_documents, context_type="Company"):
    """Generate response using Groq with context-aware prompting"""
    import requests
    
    try:
        # Prepare context
        context = "\n\n".join([doc['text'] for doc in context_documents])
        
        # Different prompts based on context type
        if context_type == "PDF":
            system_prompt = """You are BOL7 AI Assistant. The user has uploaded a PDF document and is asking questions about it.

YOUR JOB:
1. Answer questions about the PDF document using the provided context
2. The context contains extracted text from the user's PDF
3. Be specific and detailed in your answers
4. Quote relevant parts of the PDF when appropriate
5. If the question is about the PDF content, focus ONLY on the PDF context provided

RULES:
- Provide complete, detailed answers from the PDF content
- Be accurate and specific
- If information is in the context, use it fully
- Don't make up information not in the PDF"""
        else:
            system_prompt = """You are BOL7 AI Assistant - a professional chatbot for BOL7 Technologies.

YOUR JOB:
1. Answer questions about BOL7 Technologies using the provided context
2. Be helpful, friendly, and informative
3. Give complete, detailed answers when information is available
4. If context has relevant information, USE IT fully"""

        user_prompt = f"""Context Information:
{context}

User Question: {query}

Answer based on the above context:"""
        
        # Call Groq API
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000,
                "top_p": 0.9
            }
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}"
    
    except Exception as e:
        return f"Sorry, couldn't generate response: {str(e)}"
    

def text_to_speech(text, language='en'):                #👉  Convert text to speech using gTTS
    try:
        # Create audio file name
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join('media', 'tts', filename)
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filepath)
        
        return f"/media/tts/{filename}"
    
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
    


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into chunks for vector storage
    
    Args:
        text (str): Text to split
        chunk_size (int): Characters per chunk
        overlap (int): Overlapping characters between chunks
    
    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks



def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    # Add page number for better context
                    text += f"[Page {page_num}]\n{page_text}\n\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


def process_pdf_to_database(pdf_path, filename, category='uploaded_pdf'):
    try:
        # Extract text
        full_text = extract_text_from_pdf(pdf_path)
        
        if not full_text:
            return {
                'success': False,
                'error': 'No text found in PDF'
            }
        
        # Split into chunks (500 characters each for better context)
        chunk_size = 500
        chunks = []
        
        # Split by paragraphs first
        paragraphs = full_text.split('\n\n')
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # If chunks are too large, split further
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > chunk_size:
                # Split into smaller pieces
                words = chunk.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) < chunk_size:
                        temp_chunk += word + " "
                    else:
                        final_chunks.append(temp_chunk.strip())
                        temp_chunk = word + " "
                if temp_chunk:
                    final_chunks.append(temp_chunk.strip())
            else:
                final_chunks.append(chunk)
        
        # Save to database with vectors
        saved_count = 0
        failed_count = 0
        
        # First, delete any previous PDF uploads (optional - remove if you want to keep history)
        CompanyDocument.objects.filter(metadata__category='uploaded_pdf').delete()
        
        for i, chunk_text in enumerate(final_chunks):
            try:
                # Skip very short chunks
                if len(chunk_text) < 50:
                    continue
                
                # Detect language
                language = detect_language(chunk_text)
                
                # Generate vector
                vector = text_to_vector(chunk_text)
                
                # Save to database
                CompanyDocument.objects.create(
                    text=chunk_text,
                    vector=vector,
                    metadata={
                        'category': category,
                        'filename': filename,
                        'chunk_index': i,
                        'language': language,
                        'source': 'pdf_upload'
                    }
                )
                
                saved_count += 1
                
            except Exception as e:
                print(f"Failed to save chunk {i}: {e}")
                failed_count += 1
        
        return {
            'success': True,
            'saved_chunks': saved_count,
            'failed_chunks': failed_count,
            'total_chunks': len(final_chunks),
            'filename': filename
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }