FROM python:3.11.4-slim
WORKDIR /app
COPY . ./
RUN pip3 install -r /app/requirements.txt --no-cache-dir
CMD python main.py
