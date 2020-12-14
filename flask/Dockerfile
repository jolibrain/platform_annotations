FROM python:3-alpine
RUN python -m pip install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

ENV FLASK_APP "app"
EXPOSE 5000
CMD flask run --host=0.0.0.0
