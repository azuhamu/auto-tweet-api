from flask import Flask, request, jsonify
from transformers import pipeline, set_seed
import torch

app = Flask(__name__)

# --- AIモデルの準備 ---
try:
    print("🔄 Loading AI Model: rinna/japanese-gpt2-xsmall...")
    generator = pipeline(
        'text-generation',
        model='rinna/japanese-gpt2-xsmall', 
        device=-1, # CPUを使用
    )
    print("✅ AI Model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load AI model: {e}")
    generator = None

@app.route("/")
def health():
    """サーバーが正常に起動しているか確認するためのエンドポイント"""
    status = "ok" if generator else "error: model not loaded"
    return {"status": status}

@app.route("/generate", methods=["GET"])
def generate_text():
    """ツイート文を生成するメインのエンドポイント"""
    if not generator:
        return jsonify({"error": "AI model is not available"}), 503

    title = request.args.get("title", "").strip()
    excerpt = request.args.get("excerpt", "").strip()

    if not title:
        return jsonify({"error": "title is a required parameter"}), 400

    prompt = f"""
以下のブログ記事のタイトルと抜粋を元に、読者の興味を引くような魅力的なツイートを作成してください。

# 記事タイトル:
{title}

# 記事の抜粋:
{excerpt}

# 生成ツイート:
"""

    try:
        # 毎回違う結果を出すために乱数シードを設定
        set_seed(torch.randint(0, 10000, (1,)).item())
        
        # テキスト生成の実行
        generated_outputs = generator(
            prompt,
            max_length=150,
            num_return_sequences=1,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9,
            no_repeat_ngram_size=2
        )
        
        generated_text = generated_outputs[0]['generated_text']
        tweet_text = generated_text.split("# 生成ツイート:")[1].strip()

        return jsonify({"generated_text": tweet_text})

    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 500

# サーバーを起動 (Hugging Face Spacesがこの部分を呼び出す)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
