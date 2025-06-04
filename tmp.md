PYTHONPATH=src poetry run celery -A app.builders.app_builder worker --loglevel=info --pool=solo

PYTHONPATH=src poetry run celery -A common.mq.strategies.celery_strategy worker --loglevel=info --pool=solo
