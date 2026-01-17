from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CompanyDocument
from .utils import text_to_vector, detect_language
from .utils import calculate_similarity, generate_llm_response
from django.shortcuts import render
from .utils import text_to_speech
from django.core.files.storage import default_storage
from .utils import process_pdf_to_database




def chatbot_page(request):
    return render(request, 'chatbot.html')

@csrf_exempt
def chatbot_query(request):
    """Chatbot endpoint - Search database and generate response using RAG"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            top_k = int(data.get('top_k', 5))
            
            if not query:
                return JsonResponse({'success': False, 'error': 'Query is required'}, status=400)
            
            if len(query) < 3:
                return JsonResponse({'success': False, 'error': 'Query too short'}, status=400)
            
            query_language = detect_language(query)
            query_vector = text_to_vector(query)
            
            # Check if there's recent PDF data
            pdf_documents = CompanyDocument.objects.filter(
                metadata__category='uploaded_pdf'
            ).order_by('-created_at')[:50]  # Get recent PDF chunks
            
            # Get all documents
            all_documents = CompanyDocument.objects.all()
            
            if not all_documents.exists():
                return JsonResponse({
                    'success': False,
                    'error': 'No data in database'
                }, status=404)
            
            # Calculate similarities
            pdf_results = []
            company_results = []
            
            for doc in all_documents:
                similarity = calculate_similarity(query_vector, doc.vector)
                similarity_percent = round(float(similarity) * 100, 2)
                
                if similarity_percent > 15:
                    result_item = {
                        'id': doc.id,
                        'text': doc.text,
                        'similarity': similarity_percent,
                        'language': doc.metadata.get('language', 'Unknown'),
                        'category': doc.metadata.get('category', 'company_info')
                    }
                    
                    # Separate PDF results from company info
                    if doc.metadata.get('category') == 'uploaded_pdf':
                        pdf_results.append(result_item)
                    else:
                        company_results.append(result_item)
            
            # Sort by similarity
            pdf_results = sorted(pdf_results, key=lambda x: x['similarity'], reverse=True)
            company_results = sorted(company_results, key=lambda x: x['similarity'], reverse=True)
            
            # Prioritize PDF results if available
            if pdf_results:
                # Use mostly PDF content
                results = pdf_results[:4] + company_results[:1]  # 4 PDF + 1 company
                context_type = "PDF"
            else:
                # Use company info
                results = company_results[:top_k]
                context_type = "Company"
            
            results = results[:top_k]
            
            # Debug logging
            print(f"\n=== QUERY: {query} ===")
            print(f"Context Type: {context_type}")
            print(f"PDF results: {len(pdf_results)}, Company results: {len(company_results)}")
            print(f"Using {len(results)} results:")
            for r in results[:3]:
                print(f"- [{r['similarity']}%] [{r['category']}] {r['text'][:80]}...")
            
            if not results:
                llm_response = "I couldn't find relevant information. Please try rephrasing your question."
            else:
                llm_response = generate_llm_response(query, results, context_type)
            
            return JsonResponse({
                'success': True,
                'query': query,
                'query_language': query_language,
                'llm_response': llm_response,
                'context_type': context_type,
                'results': results,
                'total_matches': len(results)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'POST method required'}, status=405)




@csrf_exempt
def add_document(request):
    if request.method == 'POST':
        try:
            # Parse request
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            
            # Validate
            if not text:
                return JsonResponse({
                    'success': False,
                    'error': 'Text is required'
                }, status=400)
            
            if len(text) < 10:
                return JsonResponse({
                    'success': False,
                    'error': 'Text too short. Minimum 10 characters required.'
                }, status=400)
            
            # Detect language
            language = detect_language(text)
            
            # Generate vector embedding
            vector = text_to_vector(text)
            
            # Save to database
            document = CompanyDocument.objects.create(
                text=text,
                vector=vector,
                metadata={'language': language}
            )
            
            # Return success response
            return JsonResponse({
                'success': True,
                'message': 'Document added successfully!',
                'data': {
                    'id': document.id,
                    'text': document.text,
                    'language': language,
                    'vector_dimensions': len(vector),
                    'created_at': document.created_at.isoformat()
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON format'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST method allowed'
    }, status=405)





@csrf_exempt
def bulk_add_documents(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            documents = data.get('documents', [])
            
            if not documents or not isinstance(documents, list):
                return JsonResponse({
                    'success': False,
                    'error': 'documents array is required'
                }, status=400)
            
            added_count = 0
            failed_count = 0
            results = []
            
            for text in documents:
                try:
                    text = text.strip()
                    if len(text) < 10:
                        failed_count += 1
                        continue
                    
                    language = detect_language(text)
                    vector = text_to_vector(text)
                    
                    document = CompanyDocument.objects.create(
                        text=text,
                        vector=vector,
                        metadata={'language': language}
                    )
                    
                    added_count += 1
                    results.append({
                        'id': document.id,
                        'text': text[:50] + '...' if len(text) > 50 else text,
                        'language': language
                    })
                    
                except Exception as e:
                    failed_count += 1
                    continue
            
            return JsonResponse({
                'success': True,
                'message': f'Added {added_count} documents, {failed_count} failed',
                'added_count': added_count,
                'failed_count': failed_count,
                'results': results
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST method allowed'
    }, status=405)


def list_documents(request):
    try:
        documents = CompanyDocument.objects.all()
        
        data = []
        for doc in documents:
            data.append({
                'id': doc.id,
                'text': doc.text,
                'language': doc.metadata.get('language', 'Unknown'),
                'created_at': doc.created_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'documents': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    


@csrf_exempt
def generate_tts(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            language = data.get('language', 'en')
            
            if not text:
                return JsonResponse({
                    'success': False,
                    'error': 'Text is required'
                }, status=400)
            
            # Generate audio
            audio_url = text_to_speech(text, language)
            
            if audio_url:
                return JsonResponse({
                    'success': True,
                    'audio_url': audio_url
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'TTS generation failed'
                }, status=500)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'POST method required'
    }, status=405)






@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        try:
            if 'pdf_file' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'No file uploaded'
                }, status=400)
            
            pdf_file = request.FILES['pdf_file']
            
            # Validate file type
            if not pdf_file.name.endswith('.pdf'):
                return JsonResponse({
                    'success': False,
                    'error': 'Only PDF files are allowed'
                }, status=400)
            
            # Validate file size (max 10MB)
            if pdf_file.size > 10 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'File too large. Maximum size is 10MB'
                }, status=400)
            
            # Save file temporarily
            file_path = default_storage.save(f'temp/{pdf_file.name}', pdf_file)
            full_path = default_storage.path(file_path)
            
            # Process PDF
            result = process_pdf_to_database(
                full_path, 
                pdf_file.name,
                category='uploaded_pdf'
            )
            
            # Delete temporary file
            default_storage.delete(file_path)
            
            if result['success']:
                return JsonResponse({
                    'success': True,
                    'message': f'PDF processed successfully! Added {result["saved_chunks"]} entries to database.',
                    'data': result
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result.get('error', 'Processing failed')
                }, status=500)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'POST method required'
    }, status=405)