from abc import ABC, abstractmethod

class CVService(ABC):
    @abstractmethod
    def analyze_plant_image(self, image_path: str):
        """Analyze plant image for disease and drought stress"""
        pass
