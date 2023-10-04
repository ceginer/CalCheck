from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import torch
import os

class CalcheckModel:
    def __init__(self):
        # Label_map
        self.food_labels = ("mango", "melon", "strawberry", "blueberry", "apple", "grapefruit",
            "plum", "peach", "grape", "cherry", "yam", "chestnuts", "pepper",
            "chicory", "Kohlrabi", "Paprika", "Tomato", "Mushroom", "Pumpkin",
            "Pimento")
        self.label_map = {k: v+1 for v, k in enumerate(self.food_labels)}
        self.label_map["background"] = 0
        self.rev_label_map = {v: k for k, v in self.label_map.items()}  # inverse mapping

        self.distinct_colors = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231', '#911eb4', '#46f0f0', '#f032e6',
                        '#d2f53c', '#fabebe', '#008080', '#000080', '#aa6e28', '#fffac8', '#800000', '#aaffc3', '#808000',
                        '#ffd8b1', '#e6beff', '#808080', '#FFFFFF']
        self.label_color_map = {k: self.distinct_colors[i] for i, k in enumerate(self.label_map.keys())}

        # Load model checkpoint
        current_directory = os.getcwd()

        # 현재 작업 디렉토리 출력
        print("현재 작업 디렉토리:", current_directory)
        import sys

        sys.path.insert(0, './ml_model')
        checkpoint = 'ml_model/checkpoint_ssd300_epoch_14.pth.tar'
        # checkpoint ='C:/Users/Son/Desktop/checkpoint_ssd300_epoch_14.pth.tar'
        self.checkpoint = torch.load(checkpoint, map_location=torch.device("cpu"))
        print("tjdrhd")
        start_epoch = self.checkpoint['epoch'] + 1
        print('\nLoaded checkpoint from epoch %d.\n' % start_epoch)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.checkpoint['model'].to(self.device)
        self.model.eval()

        # Transforms
        self.resize = transforms.Resize((300, 300))
        self.to_tensor = transforms.ToTensor()
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], # ImageNet
                                        std=[0.229, 0.224, 0.225])

    def detect(self,original_image, min_score=0.2, max_overlap=0.5, top_k=200, suppress=None):
        """
        Detect objects in an image with a trained SSD300, and visualize the results.

        :param original_image: image, a PIL Image
        :param min_score: minimum threshold for a detected box to be considered a match for a certain class
        :param max_overlap: maximum overlap two boxes can have so that the one with the lower score is not suppressed via Non-Maximum Suppression (NMS)
        :param top_k: if there are a lot of resulting detection across all classes, keep only the top 'k'
        :param suppress: classes that you know for sure cannot be in the image or you do not want in the image, a list
        :return: annotated image, a PIL Image
        """

        # Transform
        image = self.normalize(self.to_tensor(self.resize(original_image)))

        # Move to default device
        image = image.to(self.device)

        # Forward prop.
        predicted_locs, predicted_scores = self.model(image.unsqueeze(0))
        print("image.unsqueeze(0) : ", image.unsqueeze(0))

        # Detect objects in SSD output
        det_boxes, det_labels, det_scores = self.model.detect_objects(predicted_locs, predicted_scores, min_score=min_score,
                                                                max_overlap=max_overlap, top_k=top_k)

        # Move detections to the CPU
        det_boxes = det_boxes[0].to('cpu')

        # Transform to original image dimensions
        original_dims = torch.FloatTensor(
            [original_image.width, original_image.height, original_image.width, original_image.height]).unsqueeze(0)
        det_boxes = det_boxes * original_dims

        # Decode class integer labels
        det_labels = [self.rev_label_map[l] for l in det_labels[0].to('cpu').tolist()]
        # If no objects found, the detected labels will be set to ['0.'], i.e. ['background'] in SSD300.detect_objects() in model.py
        if det_labels == ['background']:
            # Just return original image
            return original_image

        annotated_image = original_image
        bbox_list=[]
        lables_list=[]

        # Suppress specific classes, if needed
        for i in range(det_boxes.size(0)):
            if suppress is not None:
                if det_labels[i] in suppress:
                    continue

            # Boxes
            box_location = det_boxes[i].tolist()
            bbox_list.append(box_location)
            lables_list.append(det_labels[i])
        
        return bbox_list,lables_list, self.label_color_map