"""Extensões do Flask, criadas sem o app (o app as liga depois, com init_app)."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
limiter = Limiter(get_remote_address, storage_uri="memory://")