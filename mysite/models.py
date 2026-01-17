from django.db import models
from pgvector.django import VectorField

class CompanyDocument(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(help_text="Original company information text")
    vector = VectorField(dimensions=768, help_text="Vector embedding (768 dimensions)")
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional info like language, category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'company_documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.id}: {self.text[:50]}..."