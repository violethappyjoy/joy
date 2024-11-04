FROM python:3.11-slim
WORKDIR /mqtt
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "pymqtt.py"]
