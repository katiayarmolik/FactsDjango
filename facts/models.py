from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Fact(models.Model):
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='facts')

    def __str__(self):
        return self.text[:50]

class UserSavedFact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_facts')
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fact')

    def __str__(self):
        return f"{self.user.username} saved: {self.fact.text[:30]}"
