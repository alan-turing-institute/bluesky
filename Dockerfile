FROM python:3.6

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python BlueSky.py --build-caches

CMD ["python", "BlueSky.py", "--headless"]

