# Strawberry Disease Classifier

A Django-based project that hosts a strawberry classification system. This README is written from the repository structure observed in the project root and provides concrete, safe instructions to get the project running, inspect the code, and use the classifier components.

---

Table of contents
- [Project overview](#project-overview)
- [Repository layout](#repository-layout)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Local development (Django)](#local-development-django)
- [Running the classifier / inference](#running-the-classifier--inference)
- [Dataset, training and model files](#dataset-training-and-model-files)
- [Configuration notes](#configuration-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Project overview

This project hosts a strawberry disease classifier inside a Django web application. The classifier app likely includes model loading, preprocessing, and inference logic usable through a web UI, an admin interface, or programmatic endpoints. Use this README to install, run, and begin inspecting/integrating the classifier.

---

## Repository layout

Top-level files/folders observed:
- manage.py — Django management entrypoint
- requirements.txt — Python dependencies (install with pip)
- classifier/ — application responsible for classification functionality (models, views, forms, utilities)
- strawberry_disease_classifier/ — Django project package (settings, urls, asgi/wsgi)
- media/ — uploaded images and/or saved model artifacts
- db.sqlite3 — placeholder SQLite DB (size 0 in observed snapshot)
- .gitgnore — local ignore rules
- .idea/ — local IDE config (can be ignored)

Recommended additional files to check inside the repo (not listed here but commonly present):
- README.md (this file)
- classifier/management/commands/ — for custom CLI tasks (training, export)
- classifier/static/ and classifier/templates/ — for web UI
- classifier/models.py — Django Models (DB-backed entities)
- classifier/serializers.py & classifier/views.py — for API endpoints
- scripts/ or notebooks/ — for training or evaluation

---

## Prerequisites

- Python 3.8+ (use the version required by the project)
- pip
- virtual environment tool (venv, virtualenv, pyenv)
- (Optional) GPU + CUDA if model training/inference requires GPU acceleration

Verify installed Python:
```bash
python --version
```

Check required libraries:
- Open requirements.txt to see exact packages and versions:
```bash
cat requirements.txt
```

---

## Installation

1. Clone the repository (if not already):
```bash
git clone https://github.com/renz-garcia/strawberry_disease_classifier.git
cd strawberry_disease_classifier
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows PowerShell
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
If any dependency fails, inspect `requirements.txt` and install the problematic package manually or use the recommended system packages for compiled dependencies.

---

## Local development (Django)

Basic Django commands to get the project running locally:

1. Apply database migrations:
```bash
python manage.py migrate
```

2. Create an admin superuser (to upload images, inspect models, or use the admin UI):
```bash
python manage.py createsuperuser
```

3. Collect static files (if the project uses static files):
```bash
python manage.py collectstatic
```

4. Run the development server:
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser and navigate to the UI or admin interface (commonly /admin). Inspect the `classifier` app to find upload pages, REST endpoints, or the inference UI.

Note: Because db.sqlite3 in the repository snapshot appears empty, the first run may create a fresh local database.

---

## Running the classifier / inference

The repository contains a `classifier` application. Typical integration points you should look for inside `classifier/`:

- views.py — web views for file upload and inference
- urls.py — the route(s) where inference endpoints are mounted
- utils.py or inference.py — image preprocessing and model loading functions
- management/commands — custom CLI commands such as `train`, `predict`, or `export_model`
- media/ — location where uploaded images and saved outputs are stored

General instructions to run inference (these are broad steps—adapt to actual code you find in `classifier/`):

1. Start Django server:
```bash
python manage.py runserver
```

2. Visit the UI or API endpoint for prediction. Common endpoints:
- Web upload form: http://127.0.0.1:8000/classifier/ or /
- Admin upload: http://127.0.0.1:8000/admin/

3. If a CLI prediction exists, run a management command:
```bash
python manage.py predict --image path/to/image.jpg
```
(Replace with the actual command name after inspecting `classifier/management/commands/`.)

4. Check `media/` for saved inference results and thumbnails.

---

## Dataset, training and model files

- This repository snapshot doesn’t include an obvious dataset directory or trained model artifact inside the top-level listing, but `media/` may hold such files if added.
- If training scripts are present (commonly in `classifier/` or a `scripts/` folder), inspect them for dataset format, required preprocessing, and supported model architectures.
- Typical training steps:
  - Prepare dataset (train/val/test folders with class subfolders)
  - Configure model/hyperparameters (in settings or a config file)
  - Run training script or management command
  - Save the best model into `media/models/` or a configured folder
- If you plan to train, ensure you have the required compute (GPU recommended) and dependencies (check `requirements.txt`).

---

## Configuration notes

- Project settings are likely under `strawberry_disease_classifier/settings.py`. Key items to review:
  - DEBUG, ALLOWED_HOSTS
  - DATABASES (default uses SQLite in this snapshot)
  - MEDIA_ROOT and MEDIA_URL (where images/models are saved)
  - STATIC_ROOT / STATICFILES_DIRS
  - Any third-party ML library configuration (Torch, TensorFlow, etc.)

- Environment variables:
  - Use a .env or environment variables for secrets (SECRET_KEY, DB credentials if using other DB, etc.)
  - Do not commit credentials to source control.

---

## Troubleshooting

- Missing dependencies or compilation errors: install system-level build tools (e.g., build-essential on Linux) and the appropriate libraries (CUDA toolkit if using GPU builds).
- Port conflicts for runserver: change port with `--port` argument.
- Static files not found: run `collectstatic` and ensure STATIC_ROOT is configured.
- Model load errors: confirm the model weights file path and matching model architecture.

---

## Contributing

Guidelines:
1. Fork the repository and create a descriptive branch (e.g., `feat/add-rest-endpoint`).
2. Make small, focused commits with clear messages.
3. Add or update documentation when adding features.
4. Run linters and tests (if present) before opening a pull request.

Please include notes in PR descriptions about any changes to data formats, model artifacts, or environment variables.

---

