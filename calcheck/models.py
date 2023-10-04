from django.db import models

# Create your models here.
class ImageUploadModel(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    target_image = models.ImageField(upload_to='target_images/')
    # source_image = models.ImageField(upload_to='source_images/')