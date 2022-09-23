# ![Proyecto integrador final](#/img/UNC.jpg)

> Proyecto integrador final - 2022

[![github release version](https://img.shields.io/github/v/release/nhn/tui.editor.svg?include_prereleases)](https://github.com/nhn/tui.editor/releases/latest) [![npm version](https://img.shields.io/npm/v/@toast-ui/editor.svg)](https://www.npmjs.com/package/@toast-ui/editor) [![license](https://img.shields.io/github/license/nhn/tui.editor.svg)](https://github.com/nhn/tui.editor/blob/master/LICENSE) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](https://github.com/nhn/tui.editor/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) [![code with hearth by NHN Cloud](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-NHN_Cloud-ff1414.svg)](https://github.com/nhn)




## 🚩 Table of Contents

  - [📌 Project introduction](#-project-introduction)
  - [🎨 Features](#-features)
  
  - [🔧 Set up](#-set-up)
       - [Pre-requisits](#pre-requisits)
       - [HTTP server](#http-server)
  - [🐾 Usage example](#-examples)
  - [💬 Contributing](#-contributing)
  - [🚀 Referencer](#-references)
  - [📜 License](#-license)


## Project introduction
COMPLETAR


## 🎨 Features

COMPLETAR

## 🐾 Examples

COMPLETAR

* [Basic](https://nhn.github.io/tui.editor/latest/tutorial-example01-editor-basic)
* [Viewer](https://nhn.github.io/tui.editor/latest/tutorial-example04-viewer)
* [Using All Plugins](https://nhn.github.io/tui.editor/latest/tutorial-example12-editor-with-all-plugins)
* [Creating the User's Plugin](https://nhn.github.io/tui.editor/latest/tutorial-example13-creating-plugin)
* [Customizing the Toobar Buttons](https://nhn.github.io/tui.editor/latest/tutorial-example15-customizing-toolbar-buttons)
* [Internationalization (i18n)](https://nhn.github.io/tui.editor/latest/tutorial-example16-i18n)

Here are more [examples](https://nhn.github.io/tui.editor/latest/tutorial-example01-editor-basic) and play with TOAST UI Editor!



## 🔧 Setup

Fork `main` branch into your personal repository. Clone it to local computer. Install node modules. Before starting development, you should check if there are any errors.

### Pre-requisits
In Linux:
- Python 3 
- pip 3
- [mongoDB](#https://www.mongodb.com/try/download/community)

### HTTP server
1. Create environment:
   
```
mkdir environments
cd environments
python3 -m venv <env-name>
source activate <env-name>
source ~/environments/<env-name>/bin/activate 

```
Disable env: inside env
```
deactivate
```


2. Install flask and pymongo:
   
```
pip3 install Flask pymongo
```
3. Export environment variable:
```
export FLASK_APP=api_server.py
```
4. To change flask port:
```
export FLASK_RUN_PORT=<PORT_NUMBER>
```
5. Activate env and run server 
```
 flask run --host=0.0.0.0
 ```

> TOAST UI Editor uses [npm workspace](https://docs.npmjs.com/cli/v7/using-npm/workspaces/), so you need to set the environment based on [npm7](https://github.blog/2021-02-02-npm-7-is-now-generally-available/). If subversion is used, dependencies must be installed by moving direct paths per package.


## 🚀 References

* [NHN Dooray! - Collaboration Service (Project, Messenger, Mail, Calendar, Drive, Wiki, Contacts)](https://dooray.com)
* [UNOTES - Visual Studio Code Extension](https://marketplace.visualstudio.com/items?itemName=ryanmcalister.Unotes)


## 📜 License

This software is licensed under the [MIT](https://github.com/nhn/tui.editor/blob/master/LICENSE) © [NHN Cloud](https://github.com/nhn).
