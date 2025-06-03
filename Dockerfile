FROM python:3.13-slim

LABEL maintainer="asarekings"
LABEL version="3.0.0"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "src.api.main"]
