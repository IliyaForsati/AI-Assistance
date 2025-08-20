FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# for when running -it
RUN apt-get install -y vim

WORKDIR /home/app

COPY ./requirements.txt /home/app/
RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]

# you can say "dokcer run -p (port):8000 -it <image> /bin/bash" 
# to run command CMD [ "/bin/bash" ]
# or any ubuntu command