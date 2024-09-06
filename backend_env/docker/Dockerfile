FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /backend

# 必要なファイルをコピー
COPY . /backend

# 必要なシステムコマンドのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    wget \
    expect \
    && rm -rf /var/lib/apt/lists/*

# MySQLのインストール
RUN /backend/docker/_install_mysql.sh

# 必要なPythonライブラリをインストール
RUN pip install --no-cache-dir -r /backend/docker/requirements.txt
