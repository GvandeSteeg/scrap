FROM python:3.9
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api.py /opt/api.py

CMD ["python", "/opt/api.py"]
