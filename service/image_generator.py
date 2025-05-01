"""
Image generation service for Fashion Design.
"""
import os
import base64
import requests
from datetime import datetime
from uuid import uuid4

class ImageGenerator:
    def __init__(self, webui_url="http://127.0.0.1:7860", output_dir="service/static/images", sd_model_checkpoint="chilloutmix_NiPrunedFp32Fix"):
        self.webui_url = webui_url
        self.output_dir = output_dir
        self.sd_model_checkpoint = sd_model_checkpoint
        os.makedirs(output_dir, exist_ok=True)
        
        # General prompt settings
        self.general_prompt = " ,(full-length portrait: 1.5), (8k, RAW photo, best quality, masterpiece:1.2), (realistic, photo-realistic:1.37), (male:1.3), studio light, white backgrouond, smile"
        self.default_negative_prompt = "EasyNegative, paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, ,extra fingers,fewer fingers, strange fingers, bad hand, fat ass, hole, naked, fat thigh,6 fingers, underwear, nsfw, nude,leg open, fat"

    def generate_image(self, prompt, negative_prompt=None, width=512, height=1024, steps=20):
        """
        Generate an image using the web UI.
        
        Args:
            prompt (str): The main prompt for image generation
            negative_prompt (str, optional): Negative prompt. Defaults to None.
            width (int, optional): Image width. Defaults to 512.
            height (int, optional): Image height. Defaults to 1024.
            steps (int, optional): Number of steps. Defaults to 20.
            
        Returns:
            str: Path to the generated image
        """
        final_prompt = "(" + prompt + ": 1.4)" + self.general_prompt
        # Prepare the payload
        payload = {
            "prompt": final_prompt,
            #"negative_prompt": negative_prompt or self.default_negative_prompt,
            "negative_prompt": self.default_negative_prompt,
            "steps": steps,
            "width": width,
            "height": height,
            "sampler_name": "DPM++ SDE", 
            "sampler_index": "DPM++ SDE",
            "cfg_scale": 7,
            "scheduler": "Automatic",
            #"override_settings": {
            #    "sd_model_checkpoint": self.sd_model_checkpoint
            #}
        }

        try:
            # Send request to web UI
            response = requests.post(
                f"{self.webui_url}/sdapi/v1/txt2img",
                json=payload
            )
            response.raise_for_status()
            
            # Get the image data
            image_data = response.json()['images'][0]
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uuid4()}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(image_data))
                
            return filepath
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate image: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during image generation: {str(e)}") 