FROM python:3.10.13-slim-bookworm

ENV PLAYWRIGHT_BROWSERS_PATH="/ms-playwright"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir playwright && \
    playwright install chromium && \
    playwright install-deps chromium

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "8002"]
