
# Cineskop

Cineskop is a Python-based cinema scraper that compiles data from all cinemas in Niš into a single, accessible database. This data is then stored in a PostgreSQL database and served to a front-end through an Express.js server, which sends the data as JSON via HTTP requests. The front-end is built with vanilla HTML, CSS, and JavaScript, and is served by NGINX—all running in Docker containers. Data is updated once daily to ensure listings and schedules are current.

## Features

- Aggregate movie listings and schedules from multiple cinemas in Niš.
- Stores data in a PostgreSQL database.
- Backend server built with Express.js to handle API requests.
- Front-end delivered through NGINX using standard web technologies (HTML, CSS, JavaScript).
- Daily updates to ensure the latest information is available.

## System Requirements

- Windows, Linux, or macOS
- Python 3.7 or later
- Docker and Docker Compose
- [migrate](https://github.com/golang-migrate/migrate) - Database migration tool for PostgreSQL
- Cron or another task scheduler for automating daily updates

## Installation

1. Clone the repository:
	```
	git clone https://github.com/jovanovicdima/cineskop.git
	cd cineskop
	```

2. Start the Docker containers:
	  ```
   docker-compose up -d
   ```

3. If you are using `pgAdmin` and encounter permission issues on Linux, adjust the ownership of the `pgAdmin` directory:
	  ```
   sudo chown -R 5050:5050 ./backend/pgadmin
   ```

4. Navigate to the scraper folder and create a Python virtual environment to manage dependencies:
	  ```
   python -m venv ./scraper/venv
   ```

5. Install Python dependencies using the virtual environment's Python executable:
	  ```
   ./scraper/venv/bin/python -m pip install -r ./scraper/requirements.txt
   ```

6. Copy the `.env.example` file to `.env` and update it with your own database credentials and pgAdmin settings:
	  ```
   cp .env.example .env
   # Now edit the .env file with your actual values
   ```

7. Apply database migrations to set up the schema using the `migrate` tool. Ensure you have the `migrate` CLI installed or use the Docker version:
	  ```
   migrate -database postgres://username:password@host:port?sslmode=disable -path ./backend/migration/ up
   ```

   Replace `username`, `password`, `host`, and `port` with your actual PostgreSQL credentials and details.

8. To populate and update the PostgreSQL database daily, schedule the Python scraper to run at midnight, which is the best time for updating movie listings:
	  ```
   # Edit your crontab file by running: crontab -e
   # Add the following line to schedule the scraper daily at midnight using the virtual environment's Python:
   0 0 * * * /path/to/project_root_folder/scraper/venv/bin/python /path/to/project_root_folder/scraper/main.py
   ```

   Ensure the database settings in the scraper script match those used in the Docker container.

## Usage

Navigate to `http://localhost:8080` in your web browser to see Cineskop in action.

## Screenshots

Here are some screenshots of the Cineskop application in action:

![Home Page](./screenshots/Home%20Page.png)

![Filter View](./screenshots/Filter%20View.png)

![Movie Page](./screenshots/Movie%20Page.png)

## License

This project is licensed under the GNU General Public License v3 (GPLv3). For more details, see the [LICENSE](./LICENSE) file in the repository or visit [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Contact

Project Link: [https://github.com/jovanovicdima/cineskop](https://github.com/jovanovicdima/cineskop)
