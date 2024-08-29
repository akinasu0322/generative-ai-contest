FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なシステムコマンドのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 必要なライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 必要なファイルをコピー
COPY . .