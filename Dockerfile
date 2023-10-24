FROM python:3.10
LABEL authors="PyCrafters"

# set the environment variable
ENV APP_HOME /app
ENV PORT 8000


# set the working directory inside the container
WORKDIR $APP_HOME

# Installing dependencies
COPY requirements.txt $APP_HOME/
RUN pip install --no-cache-dir -r requirements.txt

# Copying your application to the container
COPY . .

# Set the port app
EXPOSE $PORT

# Run alembic migrations
#RUN alembic revision --autogenerate -m 'koyeb_initial' && alembic upgrade head

# Run the application
CMD ["python", "main.py"]
