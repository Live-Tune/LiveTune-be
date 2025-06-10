# 📝 Contributing to LiveTune Back-end

Thank you for your interest in contributing! We're excited to collaborate and improve the LiveTune platform together. Please take a few moments to review this guide before you begin.
[한글 CONTRIBUTING 바로가기](./docs/CONTRIBUTING_ko.md) 

> [!IMPORTANT]
> For developers interested in contributing to this project, please read the following carefully.

## 📚 Table of Contents

- [⚙️ Prerequisites](#️-prerequisites)
- [🔧 Project Setup](#-project-setup)
- [📝 Contributing Guidelines](#-contributing-guidelines)
- [📁 Folder Structure](#-folder-structure)

---

## ⚙️ Prerequisites

Before contributing, ensure you have:

- [Python](https://www.python.org/) (v3.9 or higher recommended) with pip installed
- Familiarity with [Flask](https://flask.palletsprojects.com/) and [Flask-SocketIO](https://flask-socketio.readthedocs.io/) 

---

## 🔧 Project Setup

Before starting, please read the following carefully to set up your development environment.

Clone our repository.

```bash
git clone git@github.com:Live-Tune/LiveTune-be.git
cd LiveTune-be
```

Create a virtual environment and activate it (Recommended).

```bash
python -m venv venv
# On Windows
# venv\Scripts\activate
# On macOS/Linux
# source venv/bin/activate
```

Install required libraries and dependencies.

```bash
pip install -r requirements.txt
```

In the root folder, you need to add an `env.py` file that contains your [YouTube Data API key](https://developers.google.com/youtube/v3/getting-started).

```python
YOUTUBE_API_KEY = "YOUR-API-KEY-HERE"
```

> [!important] 
> **Do not commit your `env.py` or API keys to version control.** Ensure it's listed in `.gitignore`.

Run the development server to check if everything is working. 

```bash
python run.py
```

If you want to test along with the front-end, as discussed in [#27](https://github.com/Live-Tune/LiveTune-be/issues/27), you can download the front-end repository and follow the [instructions](https://github.com/Live-Tune/LiveTune-fe/blob/main/CONTRIBUTING.md#-project-setup) to run the FE development server. 

And you're ready to go!

## 📝 Contributing Guidelines

### Naming

#### File

- Python (`.py`) filenames should be `snake_case` e.g., `user_utils.py`, `room_models.py`.

#### Functions, Variables, and Methods

- Functions, variables, and methods should be `snake_case` e.g., `get_user_data`, `max_connections`.
- Class names should be `PascalCase` e.g., `UserSession`, `RoomManager`.

### Using Git

- When committing, please use `git commit` without the `-m` option and adhere to the template format (if a `.gitmessage` template is configured).

### Develop

1. Fork this repository.
2. Create a separate branch from `main` called `${YourGithubID}/feature-name` or `${YourGithubID}/issue-number`. For example: `john-doe/add-room-capacity-feature` or `jane-doe/fix-123-login-bug`.
3. Work on that branch.
4. Ensure your code is well-formatted and **commented**.
5. Request a Pull Request (PR) with a clear explanation. Include the following:
    - What did you do? (A concise summary of changes)
    - Why is this needed for our project? (Link to an issue if applicable, or explain the motivation)
    - How can it be tested?

## 📁 Folder Structure

A general overview of the backend project structure:

```
LiveTune-be
├── app/                # Main application package
│   ├── __init__.py     # Application factory, blueprint registration
│   ├── routes.py         # API endpoint definitions 
│   ├── sockets.py      # WebSocket event handlers
│   └── utils.py        # Utility functions
├── docker/
│   ├── Dockerfile
│   ├── dockerBuild.bat
│   ├── dockerImageLoad.bat
│   ├── dockerImageSave.bat
│   └── dockerRun.bat
├── docs/
│   ├── CONTRIBUTING_ko.md
│   └── openapi.yaml # API documentation
├── .gitignore
├── env.py              # Environment variables (should be in .gitignore)
├── requirements.txt    # Python package dependencies
├── run.py              # Script to run the development 
└── README.md           # Project README
```