FROM python:alpine3.7
COPY . /app
WORKDIR /app
# Fix for Pip Dependencies Issue
RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc && pip3 install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]