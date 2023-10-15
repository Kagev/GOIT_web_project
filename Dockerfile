FROM python:3.10
LABEL authors="PyCrafters"

# set the environment variable
ENV APP_HOME /app

# set the working directory inside the container
WORKDIR $APP_HOME

# Installing dependencies for accessing services
COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

RUN pip install poetry && poetry config virtualenvs.create false && poetry install -- only main


# Copying your application to a container
COPY . .

# Set the port app
EXPOSE 8000

# run app
CMD ["python", "python_web_project/main.py", "runserver", "0.0.0.0:8000"]

