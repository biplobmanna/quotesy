from django.db import models
from django.db.models import functions

# Create your models here.

class Quote(models.Model):
    quote = models.TextField()
    author = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    @property
    def complete_quote(self):
        return f"{self.quote} -- {self.author}"

    def __str__(self):
        return self.quote

    class Meta:
        ordering = ["-updated_at", "author"]
        db_table = "quote"
