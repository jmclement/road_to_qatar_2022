FROM python:3.8.13-buster

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY road_to_qatar_2022 /road_to_qatar_2022
COPY Makefile /Makefile
ENV PYTHONPATH "${PYTHONPATH}:/road_to_qatar_2022"

# CMD uvicorn --app-dir=./road_to_qatar_2022/mlops api:app --host 0.0.0.0 --port $PORT
CMD make run_api
