FROM python:3.10

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install -U uv
RUN uv venv
RUN uv pip install --no-cache -r pyproject.toml

COPY . .

# Changed to match the port in docker-compose.yml
EXPOSE 8050

# This will always run your server using uv
CMD ["uv", "run", "server.py"]