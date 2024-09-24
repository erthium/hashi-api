# Hashiwokakero API

RestAPI with Python's FastAPI, for the Hashiwokakero logic puzzle, to generate, solve and get puzzles from the database.

The main hashiwokakero repository is [here](https://github.com/erthium/hashiwokakero).

You can also check the playground of hashiwokakero [here](https://erthium.tech/hashi).

## License

This project is licensed under the [GNU GPL-3.0](https://github.com/erthium/hashi-api/blob/main/LICENSE) license.

Although everything is free to use, modify and distribute, credit is always appreciated.

## Setup

### Dependencies

The project is written in Python 3.12.4. Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/bin/activate
```

To install the dependencies, run:

```bash
pip install -r requirements.txt
## or
make init
```

### Database

The backend solely relies on the PostgreSQL database, this part will assume we will be running the database on the local machine.

Install PostgreSQL to your machine, and make sure that the server/service is running.

Create a database and preferably a user for the database. After all successfully created, update the `DATABASE_URL` in the `.env` file.

To create the tables, run the following command on the project root:

```bash
alembic upgrade head
```

### Running the server

To run the server, execute the following command:

```bash
# development/auto-reload mode
uvicorn app.main:app --reload
## or
make dev
```

The server will be running on `http://127.0.0.1:8000` or in the port that you specified in the `.env` file.

Go to the `/docs` endpoint to see the API documentation.
