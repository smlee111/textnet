from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    데이터 1차 카테고리 모델
    """
    subject = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.subject
    
class CategoryDepth(models.Model):
    """
    데이터 2차 카테고리 모델
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.subject

class Entity(models.Model):
    """
    엔티티 모델
    """
    CategoryDepth = models.ForeignKey(CategoryDepth, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.subject


class Synonym(models.Model):
    """
    엔티티-동의어 모델
    """
    CategoryDepth = models.ForeignKey(CategoryDepth, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.entry
    
class Intent(models.Model):
    """
    인텐트 모델
    """
    CategoryDepth = models.ForeignKey(CategoryDepth, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.subject
    
class Sentence(models.Model):
    """
    인텐트-학습문장 모델
    """
    CategoryDepth = models.ForeignKey(CategoryDepth, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    phrase = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    
    def __str__(self):
        return self.phrase