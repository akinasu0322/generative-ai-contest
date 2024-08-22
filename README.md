# generative-ai-contest
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
