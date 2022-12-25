# Chessable Import

Chessable is a widely used platform that combines SRS with chess concepts. This project aims to simply the process of creating a custom chessable book/course entirely from PGN files.

## Installation and Setup

1. Clone the repository

```
git clone git@github.com:kamui-fin/chessable-import.git
cd chessable-import
```

2. Install python dependencies

```
pip install -r requirements.txt
```

3. Create a `.env` file to store credentials

```
touch .env
```

4. Open the newly created `.env` and type out your chessable.com credentials in this format (replacing the `my_username` and `my_password` text)

```
USERNAME=my_username
PASSWORD=my_password
```

## Usage

To run `chessable-import`, the command is simply:

```
python src/main.py [course_name] [pgn_file]
```

- `[pgn_file]` - A valid path to the input pgn file
- `[course_name]` - The title for the course that appears in chessable

## Contributing

All contributions in the form of pull requests, bug reports, etc. are gladly welcomed.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
