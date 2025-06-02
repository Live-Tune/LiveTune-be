# LiveTune-be

## Description

**LiveTune-be** is the backend server for the [LiveTune](https://github.com/GLSO0415-Team1/LiveTune) project—an open-source, web-based music streaming app that allows users to enjoy real-time music together using YouTube links. The backend handles room creation, user sessions, and core logic for live interactions.

## Features

  
- **Room Management**: Create, update, delete, and list public or private rooms.

- **User Sessions**: Lightweight user tracking (no login required; ephemeral session).

- **Real-time Functionality**: Enables live updates and interactions within rooms.

## Technologies Used

- Python 3.x
- Flask
- Flask-SocketIO
- OpenAPI

## Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed.

### Installation


1. **Clone the repository**

```bash
git clone git@github.com:Live-Tune/LiveTune-be.git
cd LiveTune-be
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python run.py
```

## API Documentation

- The OpenAPI specification is available at `openapi.yaml`.

## Contributing

We welcome contributions! Here's how to get started:

1. Fork this repository.
2. Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes with a descriptive message:

```bash
git commit -m "feat: add <your feature>"
```

4. Push to your fork:

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request targeting the `main` or `develop` branch.