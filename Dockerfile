FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]