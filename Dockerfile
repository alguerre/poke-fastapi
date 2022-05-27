# docker build -t pokemon_image:latest .
# docker run -p 8001:8001 pokemon_image:latest
FROM ubuntu:20.04

WORKDIR /home

RUN apt update

RUN apt install -y \
    python3 \
    python3-pip

COPY requirements.txt /home/
RUN pip3 install --no-cache-dir -r /home/requirements.txt

COPY api /home/api

CMD ["uvicorn", "api.application:app", "--port", "8001", "--host", "0.0.0.0"]
