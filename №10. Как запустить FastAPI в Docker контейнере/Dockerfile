FROM python:3.14

WORKDIR /app

#будет скопирован venv ТАК ДЕЛАТЬ НЕЛЬЗЯ
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]