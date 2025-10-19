# 🛠️ End of Life Tracker

**End of Life Tracker** is an application designed to track and display information about products reaching their end of life (EOL). This tool is particularly useful for DevOps teams and IT managers who need to plan for the replacement of obsolete technologies.

## 🚀 Technologies Used
- **Python 3.10**
- **FastAPI**: Web framework for building APIs.
- **httpx**: Asynchronous HTTP client for Python.
- **Cachetools**: In-memory caching for optimizing API calls.
- **Python Dotenv**: Environment variable management.
- **Uvicorn**: ASGI server for running the application.
- **Pydantic**: Data validation and settings management.
- **Docker**: Containerization for development and deployment.

## 📦 Project Structure
  
```
endoflife/
├── src/
│   ├── app/
│   │   ├── models/
│   │   ├── views/
│   │   ├── controllers/
│   │   ├── utils/
│   │   ├── health/
│   │   ├── main.py
├── test/
├── requirements.txt
├── Dockerfile
├── mypy.ini
├── .env.example
└── README.md
```

## 🛠️ Prerequisites

- [Python 3.10](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)

## ⚙️ Setting Up the Environment

### 1. Clone the Repository
```bash
git clone https://github.com/technologicum-auxilium/endoflife.git
cd endoflife

2. Create a Virtual Environment and Install Dependencies

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

3. Configure Environment Variables

Create a .env file from the .env.example:

cp .env.example .env

Edit the .env file with your configuration:

API_BASE_URL=https://example.com/api/
CACHE_MAXSIZE=100
CACHE_TTL=3600

🐳 Running with Docker
1. Build the Docker Image

docker build -t endoflife-app .

2. Run the Docker Container

docker run -p 8000:8000 --env-file .env endoflife-app

3. Access the Application

Visit http://localhost:8000/docs to view the auto-generated API documentation using FastAPI.
🚀 Running the Application Locally
1. Run the Application

After installing dependencies and configuring the .env file, start the server:

uvicorn src.app.main:app --reload

2. Access the API Documentation

Go to http://localhost:8000/docs to explore the API.
🛠️ Running Type Checks with MyPy

To ensure the code is properly type-checked, run:

mypy --cache-dir=/dev/null src/app

📋 Main Endpoints
GET /health

Checks the health status of the application.
GET /products/{product}

Fetches EOL status for a specific product.
GET /products/specific/{endpoint}

Fetches detailed data for a specific endpoint.
GET /products/summarized

Returns a summarized view of all monitored products.
📊 Example Usage
Example Request

curl -X GET "http://localhost:8000/products/myproduct"

Expected Response

{
  "name": "myproduct",
  "eol_date": "2024-12-31",
  "status": "active"
}

🛠️ Troubleshooting
Common Issues

    Positional-only parameters: Make sure you're using Python 3.10+.
    Missing library stubs: Run:

    mypy --install-types

🐳 Docker Multi-Stage Build (Dockerfile)

Here's a sample Dockerfile using a multi-stage build:

# Stage 1: Build
FROM python:3.10-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Run
FROM python:3.10-slim
WORKDIR /app
COPY --from=build /root/.local /root/.local
COPY src/ /app/src
ENV PATH="/root/.local/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

Build and run with:

docker build -t endoflife-app .
docker run -p 8000:8000 --env-file .env endoflife-app

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
👥 Contributors
Technologicum Auxilium
