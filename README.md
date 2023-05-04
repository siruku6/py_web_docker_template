# py_web_docker_template
This reopository can be a template for web application repositories using python and docker

## Initial setup

```bash
$ git clone https://github.com/siruku6/py_web_docker_template.git
$ cd py_web_docker_template
$ cp .env.sample .env
$ docker compose build
```

## Launch dev server

```bash
$ docker compose up

# 別のターミナルを立ち上げて以下を実行
$ curl localhost:5000/api
> hoge  # 結果
```
