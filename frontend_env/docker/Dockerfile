FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /frontend

# 必要なファイルをコピー
COPY . /frontend

# 必要なシステムコマンドのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


# 必要なPythonライブラリをインストール
RUN pip install --no-cache-dir -r /frontend/docker/requirements.txt

