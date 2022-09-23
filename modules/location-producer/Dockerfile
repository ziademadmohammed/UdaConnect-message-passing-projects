FROM python:3.7-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5555

COPY . .
CMD ["python","app/main.py"]