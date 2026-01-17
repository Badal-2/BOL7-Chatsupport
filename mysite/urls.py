from django.contrib import admin
from django.urls import path
from .import views 



urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),                              # Get API
    path('api/add-document/', views.add_document, name='add_document'),             # Post API
    path('api/bulk-add-documents/', views.bulk_add_documents, name='bulk_add_documents'),   # Post API
    path('api/list-documents/', views.list_documents, name='list_documents'),     # Get API
    path('api/chatbot/', views.chatbot_query, name='chatbot_query'),              # Post API
    path('api/tts/', views.generate_tts, name='generate_tts'),                    # Post API
    path('api/upload-pdf/', views.upload_pdf, name='upload_pdf')                  # Post API   
]