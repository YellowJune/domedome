from flask import Flask, request, jsonify
import openai
import os

openai.api_key = "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"

app = Flask(__name__)

@app.route("/kakao_webhook", methods=["POST"])
def kakao_webhook():
    try:
        data = request.get_json()
        utterance = data.get("userRequest", {}).get("utterance", "")

        if not utterance:
            raise ValueError("utterance가 없습니다.")

        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"다음 수학 문제를 풀어줘: {utterance}"}
            ],
            temperature=0.2,
        )

        result = gpt_response.choices[0].message["content"]

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": result[:1000]
                        }
                    }
                ]
            }
        })

    except Exception as e:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"[오류] {str(e)}"
                        }
                    }
                ]
            }
        })

if __name__ == "__main__":
    app.run(port=5000)
