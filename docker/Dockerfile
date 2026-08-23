FROM alpine:3.23
WORKDIR /priviblur

# The commit hash is injected at build time instead of shipping .git/ inside
# the image. Copying the whole repository history just so version.py could run
# "git rev-list" at import time meant a bloated image, git installed at
# runtime, a recursive chown over all of it, and a "safe.directory" workaround
# for a problem the COPY itself created. See issue #16.
#
# Build with:
#   docker build --build-arg PRIVIBLUR_COMMIT=$(git rev-parse --short HEAD) .
ARG PRIVIBLUR_COMMIT=unknown
ENV PRIVIBLUR_COMMIT=$PRIVIBLUR_COMMIT

COPY ./requirements.txt ./requirements.txt
COPY ./src/ ./src/
COPY ./assets/ ./assets/
COPY ./locales/ ./locales/

# tzdata: without it Alpine cannot resolve any timezone, so TZ is silently
# ignored and every timestamp in the logs comes out as UTC with no warning.
RUN apk add --no-cache python3 py3-setuptools tini tzdata && \
    addgroup -g 1000 -S priviblur && \
    adduser -u 1000 -S priviblur -G priviblur && \
    apk add --no-cache py3-pip && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt && \
    pip3 cache purge && \
    apk del py3-pip && \
    pybabel compile -d locales -D priviblur && \
    chown -R priviblur:priviblur /priviblur

EXPOSE 8000
USER priviblur
ENTRYPOINT [ "/sbin/tini", "--"]
CMD [ "python", "-m", "src.server" ]