FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY . .
RUN python3 -m pip install -r requirments_proph.txt
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r requirments.txt

CMD ["python3", "api/app.py"]
