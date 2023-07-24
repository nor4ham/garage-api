from importlib import import_module

APP_MODELS = [
    "app.api.users.models",
]

for model in APP_MODELS:
    import_module(model)
