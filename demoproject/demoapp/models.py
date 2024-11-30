from django.db import models
from django.utils import timezone

# Create your models here.
class DemoGallery(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    date_added = models.DateTimeField(default=timezone.now)
    img_Description = models.TextField(max_length=200,default='')
    img_Info = models.TextField(max_length=500,default='')

    def __str__(self):
        return self.name
    
class ImageReview(models.Model):
    image = models.ForeignKey(DemoGallery, on_delete=models.CASCADE, related_name='image_reviews')
    user = models.ForeignKey(DemoGallery, on_delete=models.CASCADE, related_name='users')
    comment = models.TextField()

    def __str__(self):
        return self.user.name
