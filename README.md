# gareth

Tool to manage the developer installation of GrimoireLab.

This software is licensed under GPL3 or later.

## Requirements

 * Python >= 3.6
 * Poetry >= 1.0
 * Click >= 7.1.2
 * PyGithub >= 1.55
 * GitPython >= 3.1.15

## Installation

### Getting the source code

Clone the repository
```
$ git clone https://github.com/vchrombie/gareth/
$ cd gareth
```

### Prerequisites

#### Poetry

We use [Poetry](https://python-poetry.org/docs/) for managing the project.
You can install it following [these steps](https://python-poetry.org/docs/#installation).

We use [Bitergia/release-tools](https://github.com/Bitergia/release-tools) for managing 
the releases.

### Installation

Install the required dependencies (this will also create a virtual environment)
```
$ poetry install
```

Activate the virtual environment
```
$ poetry shell
```

## Usage

Once you install the tool, you can use it with the `gareth` command.
```
$ gareth --help
Usage: gareth [OPTIONS]

  Tool to manage the developer installation of GrimoireLab.

Options:
  -t, --token TEXT   GitHub API Token.
  -s, --source TEXT  The source folder of the dev env.  [default: sources]
  --create           Create the developer setup.
  --update           Update the developer setup.
  --help             Show this message and exit.

```

Create the developer environment setup
```
$ gareth -t xxxx -s sources --create
```

Update the developer environment setup
```
$ gareth -s sources --update
```

## Contributions

All the contributions are welcome. Please feel free to open an issue or a PR. 
If you are opening any PR for the code, please be sure to add a 
[changelog](https://github.com/Bitergia/release-tools#changelog) entry.

## License

Licensed under GNU General Public License (GPL), version 3 or later.
