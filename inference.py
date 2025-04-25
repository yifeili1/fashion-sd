import requests
import base64

# Define the URL and the payload to send.
url = "http://127.0.0.1:7861"
general_prompt = " ,(full-length portrait: 1.5), (8k, RAW photo, best quality, masterpiece:1.2), (realistic, photo-realistic:1.37), (male:1.3), studio light, white backgrouond, smile"



prompt = "male, 1man, pure color sleeveless top garment, denim medium short pants, tall"
payload = {
    "negative_prompt": "EasyNegative, paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, ,extra fingers,fewer fingers, strange fingers, bad hand, fat ass, hole, naked, fat thigh,6 fingers, underwear, nsfw, nude,leg open, fat",
    "steps": 20,
    "width": 512,
    "height": 1024
}

payload['prompt'] = '(' + prompt + ':1.4)' + general_prompt

# Send said payload to said URL through the API.
response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
r = response.json()

# Decode and save the image.
with open("output.png", 'wb') as f:
    f.write(base64.b64decode(r['images'][0]))