FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp
RUN apt update && apt install nano tree -y
RUN pip install -r /tmp/requirements.txt
RUN ls


RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN mkdir /back
WORKDIR /back
EXPOSE 27017
EXPOSE 22
EXPOSE 2222

COPY . /back
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
