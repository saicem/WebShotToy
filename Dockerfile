FROM mcr.microsoft.com/playwright/python:v1.27.0-focal

EXPOSE 8000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "uvicorn" ,"main:app","--host", "0.0.0.0", "--port", "8000"]