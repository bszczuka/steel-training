FROM python:3.10-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk add pango libffi fontconfig ttf-freefont
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
