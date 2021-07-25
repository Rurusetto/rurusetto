![logo](rurusetto-readme-logo.svg)

# Rūrusetto (ルールセット)

[![Netlify Status](https://api.netlify.com/api/v1/badges/94d928c5-5fde-4a3c-b7b6-549b17676dab/deploy-status)](https://app.netlify.com/sites/dev-rurusetto/deploys)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)
[![Discord Shield](https://discordapp.com/api/guilds/700619421466624050/widget.png?style=shield)](https://discord.gg/CQPNADu)

A wiki that contain all osu! rulesets

## Domain

- Dev build (Some functions in dark mode like color inversion might not work): https://dev.rulesets.info/
- Official build: https://rulesets.info/
- Directly to a ruleset page: https://[rulesetname].rulesets.info/

## Development Status

The website finish and stable now.

## A big update of Rūrusetto

Due to the old codebase of Rūrusetto cannot add a new function. We think about this long time ago since we make night mode and dark mode, auto-update rulesets version from GitHub API. This codebase cannot contain or add a new function that we think or planned to add it. That's why we decided to rewrite the entire codebase and revamp the old UI to a new UI that's design for a better user experience and a new function like wiki infobox, add a new rulesets in website editor instead of pull request, etc. If you interested in a new UI, we have [a draft repositories](https://github.com/Rurusetto/rurusetto-new-draft) and [a live website](https://rurusetto-new-design.netlify.app/). More development plan will be announced in the future.

![Rūrusetto new design](rurusetto-new-ui.png)]

## Developing Rūrusetto codebase

*If you are only interested in contributing to the wiki content, instead of the underlying backend, please skip to [contributing](#contributing).*

Please make sure you have the following prerequisites:

- [Hugo Framework](https://gohugo.io/)
- Text IDE. We recommend IDE with intelligent code completion and syntax highlighting if you work with a codebase. Our recommendation is [Visual Studio Code](https://code.visualstudio.com/)
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

### Start a development server

Run this command inside the Rūrusetto directory, this will enable a development environment in http://localhost:1313/ and this support fast render and reload:

```shell
hugo server
```

### Build this website

Run this command inside the Rūrusetto directory, complete build will be available in `public` directory inside source code directory.

```shell
hugo
```

## Build source code

About a completely build source code with API fetching that you see on https://rulesets.info/. A code is in [this repositories](https://github.com/Rurusetto/rurusetto-build). If you want to contribute a codebase that is deeper than this repositories, you can contribute that repositories too.

## Contributing

Please see [the "contributing" file](CONTRIBUTING.md) if you are interested in helping out with the project!

We have [code of conduct](code_of_conduct.md) here.

## Disclaimer

Pippi icon : [@annytf](https://twitter.com/annytf/status/991050258183434240)

Default ruleset icon : [osu-resources](https://github.com/ppy/osu-resources)

## License

The majority of content in this repository is licensed under MIT license. Please see [the license file](LICENSE) for more information. tl;dr you can do whatever you want as long as you include the original copyright and license notice in any copy of the software/source.

Each rulesets has its own license.

The licensing here does not directly apply to `osu!` and `ppy`, as it is bound to its own licensing.
