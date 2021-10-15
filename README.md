![Rūrusetto logo](rurusetto-readme-logo.svg)

# Rūrusetto (ルールセット)

[![Continuous Integration](https://github.com/Rurusetto/rurusetto/actions/workflows/django.yml/badge.svg)](https://github.com/Rurusetto/rurusetto/actions/workflows/django.yml)
[![Deploy Changes to Server](https://github.com/Rurusetto/rurusetto/actions/workflows/deploy.yml/badge.svg)](https://github.com/Rurusetto/rurusetto/actions/workflows/deploy.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/rurusetto/rurusetto/badge)](https://www.codefactor.io/repository/github/rurusetto/rurusetto)
[![Website](https://img.shields.io/website?down_color=red&down_message=offline&up_color=dark%20green&up_message=online&url=https%3A%2F%2Frulesets.info%2F)](https://rulesets.info)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)
[![Discord Shield](https://discordapp.com/api/guilds/700619421466624050/widget.png?style=shield)](https://discord.gg/CQPNADu)

A wiki that contains all osu! rulesets

The new era of Rūrusetto is beginning!

## About the new website

The new website is targeted to revamp all the UI of the old website and make Rūrusetto a dynamic website with a lot more of new functions that cannot be added to the old website's source code.

## Old website source code

The old source code of the website is in [the other branch](https://github.com/Rurusetto/rurusetto/tree/main)

## Developing Rūrusetto

Please make sure you have the following prerequisites:

- [Python 3.7 or newer](https://www.python.org/)
- During development on the codebase, we recommend an IDE with intelligent code completion and syntax highlighting. Our recommendation is [PyCharm](https://www.jetbrains.com/pycharm/) or [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

### Downloading the source code

Clone the repository:

```shell
git clone https://github.com/Rurusetto/rurusetto/
cd rurusetto
```

To update the source code to the latest commit, run the following command inside the Rūrusetto directory:

```shell
git pull
```

### Make the virtual environment

During the development progress, we recommend using a virtual environment.

First, make a folder to contain the virtual environment in Rūrusetto directory. Then build the virtual environment.

```shell
cd rurusetto
mkdir venv
python3 -m venv rurusettovenv
```

When you want to access the virtual environment just use `source` command and link it to the `activate` file to activate the virtual environment file in Rūrusetto directory.

```shell
source rurusettovenv/bin/activate
```

And when you want to get out of from the virtual environment, use the `deactivate` command.

```shell
deactivate
```

**Note** : If you use PyCharm, you can click on the python interpreter and you can add the new interpreter to create a new virtual environment. Then when you run the commands in PyCharm terminal, all commands will persist in the virtual environment.

### Install the requirement library in the virtual environment

When you start the virtual environment, you need to install the requirements that are listed in `requirements.txt` file. Run this command in Rūrusetto directory to do so automatically:

```shell
pip install -r requirements.txt
```

### Make the database

Before we can start the server, we must make a database for the website by migrating the database from the code. Run this command in Rūrusetto directory to make the database.

```shell
cd rurusetto # get in the Rūrusetto project config folder
python manage.py migrate
```

### Fill the configuration value and secret key

Rūrusetto uses `python-decouple` library to separate the configuration value and secret key. This library will read the configuration value from the `.env` file. Create the `.env` file in `rurusetto` folder. Below is the template for this file.

```env
SECRET_KEY = awesome_key_here
DEBUG = True
TEST_SERVER = True
ALLOWED_HOSTS = 127.0.0.1
OSU_OAUTH_CLIENT_ID = idgohere
OSU_OAUTH_CLIENT_SECRET = keygohere
OSU_API_V1_KEY = keygohere
GITHUB_TOKEN = githubtokengohere
```

**Note** : The `OSU_OAUTH_CLIENT_ID` `OSU_OAUTH_CLIENT_SECRET` and `OSU_API_V1_KEY` are required when you want to development with osu! OAuth system or some program parts that require the osu! API you must fill the osu! API key and OAuth app number in `settings.py` to start development on this function. But if you are not testing this function it's okay to leave the key blank. (The development OAuth server callback is http://127.0.0.1:8000/accounts/osu/login/callback/.)

### Start the development server

Run the `runserver` command in Rūrusetto directory

```shell
cd rurusetto # get in the Rūrusetto project config folder
python manage.py runserver
```

## Contributing

When it comes to contributing to the project, the two main things you can do to help out are reporting issues and submitting pull requests. We have prepared a [list of contributing guidelines](CONTRIBUTING.md) that should hopefully ease you into our collaboration process.

Note that the contributing guidelines are not exhaustive. Nothing is set in stone. If you have an issue with the way the code is structured, with any libraries we are using, or with any processes involved with contributing, please bring it up and ask us! We welcome all feedback, so we can make contributions to this project as hassle-free as possible.

We use [code of conduct](code_of_conduct.md) from `Contributor Covenant`.

## License

The code in this repository is licensed under the MIT license. Please see [the license file](LICENSE) for more information. 

**TL;DR** you can do whatever you want as long as you include the original copyright and license notice in any copy of the software/source.

The images in this website and the content that is upload by the users and community are covered by DMCA. If you are the work's original owner and want to request to remove your work, please email the team at [contact@rulesets.info](mailto:contact@rulesets.info) or contact HelloYeew (project leader) at [me@helloyeew.dev](mailto:me@helloyeew.dev).

Each ruleset has its own license.

The licensing here does not directly apply to `osu!` and `ppy`, as it is bound to its own licensing.
