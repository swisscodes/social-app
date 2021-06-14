# Pull base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /social-docker

# Install dependencies
COPY Pipfile Pipfile.lock requirements.txt /social-docker/
RUN pip install -r requirements.txt
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /social-docker/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]