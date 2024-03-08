
from flask import Flask, request, render_template, send_file 
import openai 
import requests 
from io import BytesIO 


# Set your OpenAI API Key her 
openai.api_key = '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'

app = Flask(__name__)

def generate_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response 
    except Exception as e:
        print(f"Error Generaing image: {e}")
        return None


def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None 


@app.route("/", methods=["GET", "POST"])

def main():
    if request.method=='POST':
        prompt = request.form['prompt']
        if prompt:
            response = generate_image(prompt)
            if response and 'data' in response and len(response['data']) > 0:
                image_url = response['data'][0]['url']

                # download functionality
                image_buffer = download_image(image_url)
                if image_buffer:
                    return send_file(image_buffer, attachment_filename="generated_image.png")
                else:
                    return "Failed to download image.", 400
            else:
                return 'Failed to generate image. Please try again.', 400
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)