FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

WORKDIR /root

COPY ./ /root/
RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["fastapi", "dev", "main.py"]
# CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]