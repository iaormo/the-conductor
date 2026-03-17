FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize the database
RUN python -c "from mcp_server import get_db; get_db()"

EXPOSE 8080

CMD ["python", "mcp_server.py"]
