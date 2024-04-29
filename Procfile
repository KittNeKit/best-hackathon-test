worker_bot: python3 bot.py
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker API.base:base_app