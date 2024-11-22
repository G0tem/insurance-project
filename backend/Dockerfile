FROM python:3.12

RUN mkdir /fastapi

WORKDIR /fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
# CMD alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 8000