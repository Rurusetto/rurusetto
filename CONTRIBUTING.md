# Contributing Guidelines

Thank you for showing interest in the development of Rūrusetto. This guidelines below is a guidelines. There are not "official rules" or something like that, but following them will help everyone deal with things in the most efficient manner.

## Table of contents

1. [I would like to submit an issue!](#i-would-like-to-submit-an-issue)
2. [I would like to submit a pull request!](#i-would-like-to-submit-a-pull-request)

## I would like to submit an issue!

Bug reports and feature suggestion are welcomed!

* **When submitting a bug report, please try to include as much detail as possible**

  To make the bug that you found fix correctly please try to follow the bug report template and try to explain it (How to reproduce, bug behavior etc.) as much as you can.

* **Provide more information when asked to do so.**

  If the bug is complicate or hard to fix. In this case we will likely ask you for additional info. Your additional info can make us track down the problem better.

## I would like to submit a pull request!

We also welcome pull request. The [issue tracker](https://github.com/Rurusetto/rurusetto/issues) should provide an issue from the user and some function that want to implement. Before we go longer, here is some key things before getting started:

* **Make sure you are comfortable with our library and your development environment.**

  This website use Django and Python as backend and HTML, Bootstrap and JavaScript as a frontend. Please make sure that you are familiar with this library and its tool.

  If you contribute to the codebase for the first time and want to learn on the codebase. The issues that tag with [good first issues](https://github.com/Rurusetto/rurusetto/labels/good%20first%20issue) is the best way to contribute with learning the structure the codebase at the same time. 

* **Code quality is the priority for us**

  We have `CodeFactor` to analyze the code quality and the code format. If `CodeFactor` or the maintainer need you to fix the code quality please fix it. We want to make the codebase clean as mush as we can.

* **Make sure that the pull request is complete before opening it.**

  Draft are an option but please check and make sure that you are finish the bug fix or new function before make a new pull request and let the maintainer know and review it.

* **Only push code when it's ready.**

  When pushing to already-open pull request please try to only push changes you are reasonably certain of. Push evert commit will make the continuous integration build queue grow in size, slowing down work and taking time that could be spent to verifying other changes.

* **Make sure to keep the *Allow edits from maintainers* check box checked.**

  To speed up the merging process, sometimes collaborators want to push some change to your pull request. So, having the *Allow edits from maintainers* checkbox checked lets maintainers do that; without it maintainers are forced to report issues back to you and wait for you to address them.

* **Refrain from continually merging the main branch back to the pull request.**

  Please refrain from continually merging the `main` branch unless there are merge conflicts that need resolution. One of the maintainers will merge `main` branch themselves before merging the pull request itself anyway.

* **Refrain from force-pushing to the pull request.**

  Force-pushing should be avoided, as it can lead to accidentally overwriteing a maintainer's changes. The case in which force-pushing is warranted are very rare (such as accidentally leaking sensitive info in one of the files committed, adding unrelated files, or mis-merging a dependent pull request).

* **Refrain from making changes through the GitHub web interface.**

  Even GitHub provide an option to edit code or replace files in the repository using the web interface. Ee strongly discourage using it in most scenarios. Editing files this way is inefficient and likely to introduce whitespace or file encoding changes that make it more difficult to review the code.

  Code written in web interface will also very likely be questioned by the reviewer or fail the continuous integration and code quality check. We strongly encourage using an IDE like [PyCharm](https://www.jetbrains.com/pycharm/) or [Visual Studio Code](https://code.visualstudio.com/).

* **Feel free to reach us for help.**

  If you have any problem on the development process please leave the comment in your pull request or contact the maintainer in the [Discord development server](https://discord.gg/CQPNADu). We will help you as much as we can.
