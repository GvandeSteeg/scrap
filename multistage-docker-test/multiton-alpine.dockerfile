#############
## Stage 1 ##
#############
FROM python:3.9 AS compile-image
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


#############
## Stage 2 ##
#############
FROM python:3.9-alpine AS build-image
COPY --from=compile-image /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY api.py /opt/api.py

CMD ["python", "/opt/api.py"]
