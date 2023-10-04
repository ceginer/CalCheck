from django import forms
from .models import ImageUploadModel

# description 추가
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('target_image',)