# Anime Scraper API

## Description

Anime Scraper API is a project built with FastAPI to scrape anime data and download links.

## Requirements

- Python 3.7+
- pip
- Docker (Only for Docker use)
- Redis Database

## Getting Started

### Docker Use

1. Clone the repository:

   ```bash
   git clone https://github.com/ElPitagoras14/scrap-anime-api.git
   cd scrap-anime-api
   ```

2. Build the image:

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
   source env/bin/activate # For Linux based
   env\Scripts\activate # For Windows
   ```

3. Run the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. Make sure your virtual environment is activated (if you created one).

5. Navigate to the src folder and run the script:

   ```bash
   python main.py
   ```

6. If you use VSCode, you can use task `Run with Python` with `Ctrl+Shift+P` to run the project.

The server should be running at `http://127.0.0.1:8000`.

### Redis Installation (For Development)

1. Create a Redis Database with the following command:

   ```bash
   docker-compose up -d redis-stack
   ```

## Usage

You can access the automatically generated FastAPI documentation at `http://127.0.0.1:8000/docs`.

## Author

- [Jonathan García](https://github.com/ElPitagoras14) - Computer Science Engineer
