from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, blank=True, null=True)  # ✅ MUST BE HERE
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
