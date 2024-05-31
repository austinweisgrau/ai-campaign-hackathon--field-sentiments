# Build step #3: build the API with the client as static files
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy file structure after installing pip packages
# This avoids installing pip packages if changes are made to files
COPY / /app
RUN PYTHONPATH=. python3 scripts/initialize_db.py

ENV FLASK_ENV production

EXPOSE 3000
ENTRYPOINT ["/app/scripts/docker_entrypoint.sh"]
