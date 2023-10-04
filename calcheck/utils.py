from PIL import Image
from .apps import CalcheckConfig
import json

def check_image(target_image):
    original_image = Image.open(target_image, mode='r')
    original_image = original_image.convert('RGB')
    bbox_list,lables_list, label_color_map = CalcheckConfig.model.detect(original_image, min_score=0.2, max_overlap=0.5, top_k=200)

    # bbox 는 json 직렬화
    bbox_list = json.dumps(bbox_list)



    return bbox_list, lables_list, label_color_map

def calories_per_100g():
    calories_per_100g = {
    "mango": 57,
    "melon": 38,
    "strawberry": 27,
    "blueberry": 57.14,
    "apple": 57,
    "grapefruit": 30,
    "plum": 25,
    "peach": 42,
    "grape": 47,
    "cherry": 60,
    "yam": 124,
    "chestnuts": 160,
    "pepper": 19,
    "chicory": 22.86,
    "Kohlrabi": 28,
    "Paprika": 16.67,
    "Tomato": 14,
    "Mushroom": 38,
    "Pumpkin": 57,
    "Pimento": 20
    }
    return calories_per_100g