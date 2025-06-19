import os
import openai
import pytesseract
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import requests

openai.api_key = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)

def solve_math_problem(problem_text):
    prompt = f"""
    다음 수학 문제를 자세히 풀이하고 정답을 알려줘. 고등학생 수준에 맞게 설명해줘.

    문제:
    {problem_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message["content"]

def extract_text_from_image(url):
    image_data = requests.get(url).content
    image = Image.open(BytesIO(image_data))
    return pytesseract.image_to_string(image, lang="kor+eng")

@app.route("/kakao_webhook", methods=["POST"])
def kakao_webhook():
    body = request.json
    utterance = body['userRequest']['utterance']

    problem_text = utterance

    if "imageUrl" in body['userRequest']:
        image_url = body['userRequest']['imageUrl']
        try:
            problem_text = extract_text_from_image(image_url)
        except Exception as e:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"이미지 인식 실패: {str(e)}"}}]
                }
            })

    answer = solve_math_problem(problem_text)

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": answer[:1000]}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
