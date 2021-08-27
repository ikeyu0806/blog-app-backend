FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY ./app /app
RUN pip install -r requirements.txt
