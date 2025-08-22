# Python 3.9の公式イメージをベースとして使用
FROM python:3.9

# コンテナ（サーバー）内での作業ディレクトリを指定
WORKDIR /code

# 最初にライブラリ一覧だけをコピーしてインストール
# （コードの変更時に毎回ライブラリを入れ直さないようにするための高速化テクニック）
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ライブラリインストール後に、プロジェクトの全ファイル（app.pyなど）をコピー
COPY . .

# このアプリケーションはポート8000番で通信します、という宣言
EXPOSE 8000

# コンテナが起動したときに実行するメインのコマンド
# 「flask run --host=0.0.0.0 --port=8000」というコマンドを実行する
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
