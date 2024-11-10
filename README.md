# Anime Scraper API

## Description

Anime Scraper API is a project built with FastAPI to scrape anime data and download links.

## Requirements

- Python 3.7+
- pip
- Docker (Only for Docker use)
- MySQL Database

## Getting Started

### Docker Use

1. Clone the repository:

   ```bash
   git clone https://github.com/ElPitagoras14/scrap-anime-api.git
   cd scrap-anime-api
   ```

2. Rename `docker-compose.yaml.example` to `docker-compose.yaml`.

3. Fill the environment variables in `docker-compose.yaml` according to [Environment Variables](#environment-variables) section.

4. Build the image:

   ```bash
   docker-compose up -d
   ```

The server should be running at `http://localhost:8000`.

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

### MySQL (For Development)

> [!NOTE]
> You can use your own database with the `init.sql` file at `src/databases/mysql/init.sql`.

1. Fill the environment variables for `scraper-db` service in `docker-compose.yaml` according to Environment Variables section.

2. Create a MySQL Database with the following command:

   ```bash
   docker-compose up -d scraper-db
   ```

## Usage

You can access the automatically generated FastAPI documentation at `http://127.0.0.1:8000/docs`.

## RoadMap

- [ ] Write the Roadmap

## Environment Variables

### FastAPI service

- `HOST` - Domain where the application will be hosted. Recommended: `0.0.0.0` in Docker or `localhost` for development.
- `PORT` - Application port. Default: `8000`.
- `APP_NAME` - Name of the FastAPI application. Default: `main:app`.
- `APP_ADMIN_USER` - Default admin username for the app. Default: `administrator`.
- `APP_ADMIN_PASS` - Default admin password for the app. Default: `scraper`.
- `AUTH_SECRET_KEY` - Secret key for JWT encryption.
- `AUTH_ALGORITHM` - Algorithm used for JWT encryption.
- `AUTH_EXPIRE_MINUTES` - JWT token expiration time in minutes.
- `LOG_APP_PATH` - Path where application logs will be saved. Recommended for Docker: /var/log/scraper-anime/app.log.
- `LOG_ERROR_PATH` - Path where error logs will be saved. Recommended for Docker: /var/log/scraper-anime/error.log.
- `MYSQL_HOST` - MySQL database host, corresponding to the database service name in Docker.
- `MYSQL_USER` - Username for connecting to the MySQL database. Default: `root`.
- `MYSQL_PASS` - Password for connecting to the MySQL database. It must match the password used to create the database.
- `MYSQL_PORT` - Port where the MySQL database is hosted. Default: `3306`.
- `MYSQL_DATABASE` - Name of the database to connect to. Must match the database used during setup.

### MySQL service

- `MYSQL_ROOT_PASSWORD` - Password for the `root` user to be created in the MySQL database.
- `MYSQL_DATABASE` - Name of the database to be created in the MySQL service.

## Author

- [Jonathan García](https://github.com/ElPitagoras14) - Computer Science Engineer
