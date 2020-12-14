# Annotation Tool Flask proxy

In order to manipulate files on DeepDetect Platform from VoTT client, this
Flask app define HTTP routes.

## Testing

```
python -m pytest tests
```

## Installation

### Platform docker

Add a new container inside socker-compose.yml :

```
platform_annotations_backend:
  image: jolibrain/platform_annotations_backend
  restart: always
  volumes:
    - /opt/platform:/opt/platform
```

Container is not available on a docker registry, so we use the Dockerfile to
build the container.

### Platform nginx

Add this rule to Platform nginx config file *config/nginx/nginx.conf* :

```
upstream platform_annotations_backend {
  least_conn;
  server platform_annotations_backend:5000 fail_timeout=0;
}

server {

  ...

  location ^~ /annotations/tasks/ {
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://platform_annotations_backend/;
  }
```
