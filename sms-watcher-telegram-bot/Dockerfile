FROM python:3.12-alpine as builder

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.12-alpine

ENV APP_DIR=/home/app

RUN mkdir -p $APP_DIR

RUN addgroup -S app && adduser -S app -G app

WORKDIR $APP_DIR

COPY --from=builder /usr/src/app/wheels /wheels

RUN pip install --no-cache /wheels/*

COPY . .

RUN sed -i 's/\r$//g' entrypoint.sh

RUN chmod +x entrypoint.sh

RUN chown -R app:app $APP_DIR

USER app

ENTRYPOINT ["/home/app/entrypoint.sh"]