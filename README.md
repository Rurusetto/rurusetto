![Rūrusetto logo](rurusetto-readme-logo.svg)

# Rūrusetto (ルールセット)

[![Continuous Integration](https://github.com/Rurusetto/rurusetto/actions/workflows/django.yml/badge.svg)](https://github.com/Rurusetto/rurusetto/actions/workflows/django.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/rurusetto/rurusetto/badge)](https://www.codefactor.io/repository/github/rurusetto/rurusetto)
[![Website](https://img.shields.io/website?down_color=red&down_message=offline&up_color=dark%20green&up_message=online&url=https%3A%2F%2Fbeta.rulesets.info%2F)](https://beta.rulesets.info)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)
[![Discord Shield](https://discordapp.com/api/guilds/700619421466624050/widget.png?style=shield)](https://discord.gg/CQPNADu)

A wiki that contains all **osu!** rulesets

A new era of Rūrusetto is beginning!

## About the new website

The new website is targeted to revamp all UI of the website and make Rūrusetto not a static website anymore, with a lot of new functions, that cannot be added in the old website source code.

You can test the new website [here](https://beta.rulesets.info) and you can check on the changelog in website or GitHub release.

## Old website source code

An old source code of the website is in [the other branch](https://github.com/Rurusetto/rurusetto/tree/main)

The main website will use the old source code until I am sure that the new code can be used now.

If you have questions on the new website, you can checkout the already written explanation [here] (https://github.com/Rurusetto/rurusetto/tree/main#a-big-update-of-r%C5%ABrusetto).

## Developing Rūrusetto

Please make sure you have the following prerequisites:

-  [Python 3.7 or better](https://www.python.org/)
- During development of codebase, we recommend an IDE with intelligent code completion and syntax highlighting, if you work with a codebase. Our recommendation are [PyCharm](https://www.jetbrains.com/pycharm/) or [Visual Studio Code](https://code.visualstudio.com/)
-  [Git](https://git-scm.com/)

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

During the development progress, we recommend using the virtual environment (venv) during the development process.

First, create a folder to contain the virtual environment in Rūrusetto directory. Then build the virtual environment.

```shell
cd rurusetto
mkdir venv
python3 -m venv rurusettovenv
```

When you want to access the virtual environment just use `source` command and link to `activate` file to activate the virtual environment file in Rūrusetto directory.

```shell
source rurusettovenv/bin/activate
```

And when you want to get off from the virtual environment, use the `deactivate` command.

```shell
deactivate
```

Note : If you use PyCharm, you can click on the python interpreter and you can add the new interpreter to create a new virtual environment and when you run the command in PyCharm terminal, all commands will stay isolated in the virtual environment.

### Install the requirement library in the virtual environment

When you start the virtual environment, you need to install the requirements that are listed in `requirements.txt` file. Run this command in Rūrusetto directory:

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

Rūrusetto use `python-decouple` library to separate the configuration value and secret key. This library will read the configuration value from `.env` file. Let's create the `.env` file in `rurusetto` folder and below is the template for this file.

```env
SECRET_KEY = awesome_key_here
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1
OSU_OAUTH_CLIENT_ID = idgohere
OSU_OAUTH_CLIENT_SECRET = keygohere
OSU_API_V1_KEY = keygohere
```

Note : The `OSU_OAUTH_CLIENT_ID`  `OSU_OAUTH_CLIENT_SECRET` and `OSU_API_V1_KEY` are required when you want to development with osu! OAuth system or some program part that required the osu! API you must fill the osu! API key and OAuth app number in `settings.py` to start development on this function. But if you are not testing on this function it's okay to leave the key blank. (The development OAuth server callback is http://127.0.0.1:8000/accounts/osu/login/callback/.)

### Start the development server

Run the `runserver` command in Rūrusetto directory

```shell
cd rurusetto # get in the Rūrusetto project config folder
python manage.py runserver
```

## Contributing

When it comes to contributing to the project, the two main things you can do to help out are reporting the issues and submitting pull requests. We have prepared a [list of contributing guidelines](CONTRIBUTING.md) that should hopefully ease you into our collaboration process.

Note that the contributing guidelines is not all. Nothing is set in stone. If you have an issue with the way code is structure, with any libraries we are using, or with any processes involved with contributing, please bring up and ask us! We welcome all feedback, so we can make the contributing to this project as painless as possible.

We use [code of conduct](code_of_conduct.md) from `Contributor Covenant`.

## License

The code in this repository is licensed under MIT license. Please see [the license file](LICENSE) for more information. tl;dr you can do whatever you want as long as you include the original copyright and license notice in any copy of the software/source.

The image in this website and the content that upload by user and community is cover on DMCA. If you are the work and owner and want to request to remove your work please email the team at [contact@rulesets.info](mailto:contact@rulesets.info) or contact HelloYeew (project leader) at [me@helloyeew.dev](mailto:me@helloyeew.dev).

Each rulesets has its own license.

The licensing here does not directly apply to `osu!` and `ppy`, as it is bound to its own licensing.