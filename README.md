# generative-ai-contest
### アプリケーションサーバーとパソコンを繋げる
```bash
# sshキーの作成
# サーバー側で
ssh-keygen -t ed25519 -C "your_email@example.com"
```
### アプリケーションサーバーとgitを繋げる
### gitクローンの仕方
```bash
# 
```
### Dockerの立ち上げ方
#### DockerfileからDockerイメージを作成
```bash
# dockerファイルのあるディレクトリで
docker build -t gen-ai-contest-image:1.0 .
```
#### Dockerイメージからコンテナの作成
```bash
docker run -v .:/app -it gen-ai-contest-image:1.0 /bin/bash
```
