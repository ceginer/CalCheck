from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
from .models import ImageUploadModel
from .forms import ImageUploadForm
from .utils import calories_per_100g, check_image
import logging
from django.http import HttpResponse

# Create your views here.
class ImageUpload(APIView):
    def get(self, request):
        form = ImageUploadForm()  # GET reuest
        return render(request, 'calcheck/img_upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        # if form.is_valid():
        target_image = request.FILES['source_image']
        upload_image_model = ImageUploadModel.objects.create(
                                                            target_image=target_image
                                                            )

        if upload_image_model:
            return redirect(reverse('calcheck:check_calories', kwargs={'id': upload_image_model.id}))
        else:
            return HttpResponse("Upload failed or form is not valid.")

class CheckCalories(APIView):
    def get(self, request, id):
        upload_image_model = ImageUploadModel.objects.get(id=id)
        target_image = upload_image_model.target_image

        #객체 bbox
        target_bbox_list_json,lables_list, label_color_map = check_image(target_image)
        
        # 중복 제거한 라벨 = 검출된 객체
        detected_furits = list(set(lables_list))
        calories_map = calories_per_100g()
        calories_list= []
        for fruit in detected_furits:
            calories_list.append(calories_map[fruit])
            

        print(label_color_map)
        print(calories_map)
        print(detected_furits)
        print(calories_list)

        result_list= zip(detected_furits,calories_list)

        context = {
            'label_color_map' : label_color_map,
            'calories_map' : calories_map,
            'target_bbox_json': target_bbox_list_json,
            'lables_list' : lables_list,
            'result_list' : result_list,
            'img_model': upload_image_model,
            'detected_furits' : detected_furits
            }

        return render(request, 'calcheck/check.html', context)
    
    def post(self, request, id):
        return

