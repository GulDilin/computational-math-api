FROM python:3.8.2

WORKDIR /app

COPY requirements.txt /app
COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]