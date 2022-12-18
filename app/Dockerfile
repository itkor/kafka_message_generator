FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9092
ENTRYPOINT ["python"]
CMD ["generator_dockerized.py"]