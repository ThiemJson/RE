FROM python:3-alpine AS setup-image

WORKDIR /usr/src/treqs

COPY pyproject.toml .
COPY setup.py .
COPY treqs ./treqs

RUN pip install --no-cache-dir -e .

ENTRYPOINT [ "treqs" ]
