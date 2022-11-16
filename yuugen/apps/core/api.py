import json
import os

from pathlib import Path
from yuugen.apps.core import config

from django.core.exceptions import ImproperlyConfigured






def get_secret(setting):
    """Get the secret variable or return explicit exception."""
    with open(os.path.join(os.path.dirname(__file__), "secrets.json"), "r") as f:
        secrets = json.loads(f.read())
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f"Set the {setting} secret variable"
        raise ImproperlyConfigured(error_msg)




