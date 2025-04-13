FROM ubuntu 

WORKDIR /app 

COPY requirements.txt /app/ 
COPY . /app/

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install --no-cache-dir -r requirements.txt


EXPOSE 8000 

ENTRYPOINT [ "python3", "manage.py" ]

CMD ["runserver", "0.0.0.0:8000"]