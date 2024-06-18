# Use the official Python image as the base image
FROM python:3.12 as gv-base

# System Dependencies:
RUN apt-get update && apt-get install -y libpq-dev

COPY ./requirements /code/requirements
WORKDIR /code
RUN python manage.py collectstatic --noinput
EXPOSE 8000
# END gv-base

# BEGIN gv-deploy
FROM gv-base as gv-deploy
# install non-dev and release-only dependencies:
RUN pip3 install --no-cache-dir -r requirements/release.txt
COPY . /code/
# collect static files into a single directory:
RUN python manage.py collectstatic --noinput
# note: no CMD in gv-deploy -- depends on deployment
# END gv-deploy

# BEGIN gv-local
FROM gv-base as gv-local
# dev and non-dev dependencies:
RUN pip3 install --no-cache-dir -r requirements/dev-requirements.txt
COPY . /code/
# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# END gv-local
