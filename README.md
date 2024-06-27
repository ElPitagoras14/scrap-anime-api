# Anime Scraper API

## Description

Anime Scraper API is a project built with FastAPI to scrape anime data and download links.

## Requirements

- Python 3.7+
- pip
- Docker (Only for Docker use)
- Redis Database

## Getting Started

### Redis Installation

1. Create a Redis Database with the following command:

   ```bash
   docker-compose up -d redis-stack
   ```

### Docker Use

1. Clone the repository:

   ```bash
   git clone https://github.com/ElPitagoras14/scrap-anime-api.git
   cd scrap-anime-api
   ```

2. Rename the file `docker-compose-example.yaml` to `docker-compose.yaml`.

3. Fill the following environment variables in `docker-compose.yaml`.

   ```env
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   APP_NAME=main:app
   IN_DOCKER=True
   ANIME_HOST=
   REDIS_HOST=redis-stack
   REDIS_PORT=6379
   ```
4. Create a `.env` file with the following variable:

   ```env
   COMPOSE_PROJECT_NAME=back-scraper
   ```

5. Build the image:

   ```bash
   docker-compose up -d
   ```

The server should be running at `http://127.0.0.1:8000`.

### Development Use

1. Clone the repository:

   ```bash
   git clone https://github.com/ElPitagoras14/scrap-anime-api.git
   cd scrap-anime-api
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Run the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. Create an .env file in the root of the project and add the following environment variables:

   ```env
   HOST=127.0.0.1
   PORT=8000
   DEBUG=True
   APP_NAME=main:app
   ANIME_HOST=
   REDIS_HOST=127.0.0.1
   REDIS_PORT=6379
   ```

5. Make sure your virtual environment is activated (if you created one).

6. Navigate to the src folder and run the script:

   ```bash
   python main.py
   ```

7. If you use VSCode, you can use task to run the project.

The server should be running at `http://127.0.0.1:8000`.

## Usage

You can access the automatically generated FastAPI documentation at `http://127.0.0.1:8000/docs`.

## Author

- [Jonathan García](https://github.com/ElPitagoras14) - Computer Science Engineer
