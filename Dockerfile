FROM node:alpine
WORKDIR /usr/src/app
COPY . /usr/src/app/

#
# 04/06/2019
# We don't need to do this cache clean, I guess it wastes time / saves space:
# https://github.com/yarnpkg/rfcs/pull/53
#
# 03/12/2020
# Add apk python install
#
RUN set -ex; \
  apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers make python && \
  NOYARNPOSTINSTALL=1 yarn install; \
  yarn cache clean; \
  yarn run build

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=0 /usr/src/app/build/ /usr/share/nginx/html
COPY --from=0 /usr/src/app/docs/vott-deepdetect/site/ /usr/share/nginx/html/docs

# Replace default nginx configuration to remove js caching when updating container
COPY --from=0 /usr/src/app/nginx/default.conf /etc/nginx/conf.d/
