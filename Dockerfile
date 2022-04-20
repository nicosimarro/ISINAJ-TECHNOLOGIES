FROM python:3.7

RUN mkdir /micro
WORKDIR /micro
ADD . /micro/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/app.py"]
