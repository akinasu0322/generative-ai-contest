FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 必要なファイルをコピー
COPY . .