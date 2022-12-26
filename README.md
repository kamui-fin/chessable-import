# Chessable Import

Chessable is a widely used platform that combines SRS with chess concepts. This project aims to simply the process of creating a custom chessable book/course entirely from PGN files.

## Installation and Setup

1. Clone the repository

```
git clone https://github.com/kamui-fin/chessable-import.git
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
CHESSABLE_USERNAME=my_username
CHESSABLE_PASSWORD=my_password
```

## Usage

To run `chessable-import`, the command is simply:

```
python main.py [course_name] [pgn_file]
```

- `[pgn_file]` - A valid path to the input pgn file
- `[course_name]` - The title for the course that appears in chessable

### Course options customization

- `-c` - The color of the pieces for the course. Defaults to `White`. The other options are `Black` and `Both`
- `-t` - Course type. Available options include `["Opening", "Endgame", "Strategy", "Tactics"]`

## Contributing

All contributions in the form of pull requests, bug reports, etc. are gladly welcomed.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
