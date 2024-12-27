from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import re

# Create your models here.


# 이미지 저장 경로
def product_image_path(instance, filename):
    return f"product_images/{instance.user.username}/{filename}"

# 해시태그 유효성 검사 함수
def validation_hashtag(value):
    if not re.match(r'^[0-9a-zA-Z]+$', value):
        raise ValidationError("해시태그는 알파벳, 숫자, 언더스코어만 가능합니다!")

# Hashtag 모델 정의
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validation_hashtag])
    
    def __str__(self):
        return f'#{self.name}'
    
# Product 모델 정의
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_products", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="products", blank=True)
    views = models.PositiveIntegerField(default=0)
    
    
    


    @property
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title