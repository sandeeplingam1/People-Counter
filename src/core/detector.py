import cv2
import mediapipe as mp

class PersonDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initializes the MediaPipe Pose model for person detection.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def detect_people(self, image):
        """
        Detects people (poses) in the given image.
        Returns:
            processed_image: Image with detection overlays.
            num_people: Number of people detected.
        """
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and find poses
        results = self.pose.process(image_rgb)
        
        num_people = 0
        if results.pose_landmarks:
            # MediaPipe Pose detects ONE person by default in the 'Pose' solution.
            # However, for multiple people, we should ideally use 'Holistic' or 
            # a different Object Detection model. 
            # Given MediaPipe's single-person Pose limitation, I will use 
            # MediaPipe Object Detection (EfficientDet) for multi-person counting 
            # if Pose isn't sufficient, but for this remaster, I will implement 
            # Object Detection which is better for "People Counting".
            pass
            
        # Refactoring to Object Detection for multi-person support
        return image, num_people

    def __del__(self):
        self.pose.close()

# Let's actually use Object Detection for reliable multi-person counting
class MultiPersonDetector:
    def __init__(self, min_detection_confidence=0.4):
        self.mp_object_detection = mp.solutions.object_detection
        self.detector = self.mp_object_detection.ObjectDetection(
            min_detection_confidence=min_detection_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.detector.process(image_rgb)
        
        count = 0
        if results.detections:
            for detection in results.detections:
                # Check if the detected object is a person (Label ID 0 in COCO/MediaPipe)
                if detection.label[0] == "person":
                    count += 1
                    self.mp_drawing.draw_detection(image, detection)
        
        return image, count

    def __del__(self):
        self.detector.close()
