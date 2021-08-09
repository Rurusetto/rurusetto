# Rūrusetto (ルールセット)

A wiki that contain all osu! rulesets

## About the new website

The new website is target to revamp all UI of the website and make Rūrusetto not a static website anymore with a lot of new function that cannot add in old website source code.

You can test on the new website [here](https://beta.rulesets.info) and you can see changelog in website or GitHub release.

## Old website source code

An old source code of the website is in [the other branch](https://github.com/Rurusetto/rurusetto/tree/main)

The main website will use the old source code until I am sure that the new code can be used now.

About question on new website I already write an explanation on [this](https://github.com/Rurusetto/rurusetto/tree/main#a-big-update-of-r%C5%ABrusetto).

## Developing Rūrusetto

Please make sure you have the following prerequisites:

- [Python](https://www.python.org/)
- During development on codebase, we recommend IDE with intelligent code completion and syntax highlighting if you work with a codebase. Our recommendation is [PyCharm Professional](https://www.jetbrains.com/pycharm/) or [Visual Studio Code](https://code.visualstudio.com/)
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

During the development progress, we recommend using the virtual environment during development progress.

First, make the folder to contain the virtual environment in Rūrusetto directory. Then build the virtual environment.

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

Note : If you use PyCharm, you can click on the python interpreter and you can add the new interpreter to create a new virtual environment and when you run the command in PyCharm terminal all command will stay in virtual environment.

### Install the requirement library in the virtual environment

When you start the virtual environment, you need to install the requirement that listing in `requirements.txt` file. Run this command in Rūrusetto directory:

```shell
pip install -r requirements.txt
```

And install the [rurusetto-django-allauth](https://github.com/Rurusetto/rurusetto-django-allauth), the library that require to use with website login system.

```shell
pip install git+https://github.com/Rurusetto/rurusetto-django-allauth.git
```

### Make the database

Before we can start the server, we must make a database for the website by migrate the database from the code. Run this command in Rūrusetto directory to make the database.

```shell
cd rurusetto # get in the Rūrusetto project config folder
python manage.py migrate
```

### Start the development server

Run the `runserver` command in Rūrusetto directory

```shell
cd rurusetto # get in the Rūrusetto project config folder
python manage.py runserver
```

Note : Before you can start the development server you must fill the API key to enable osu! OAuth system in `settings.py` file and the callback URL of the OAuth on the development server is http://127.0.0.1:8000/accounts/osu/login/callback/.

## License

The majority of content in this repository is licensed under MIT license. Please see [the license file](LICENSE) for more information. tl;dr you can do whatever you want as long as you include the original copyright and license notice in any copy of the software/source.

Each rulesets has its own license.

The licensing here does not directly apply to `osu!` and `ppy`, as it is bound to its own licensing.