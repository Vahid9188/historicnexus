from django.db import models

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('published', 'Published'),
    ]
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = models.CharField(max_length=100, blank=True)  # Tags as a comma-separated string
    image = models.ImageField(upload_to='articles/', blank=True, null=True)  #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title