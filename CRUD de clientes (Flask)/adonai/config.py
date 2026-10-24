"""Configurações do sistema, lidas das variáveis de ambiente."""

import os
from datetime import timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def carregar_config():
    chave = os.environ.get("SECRET_KEY")
    if not chave:
        raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")

    return {
        "SECRET_KEY": chave,
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_SECURE": os.environ.get("COOKIE_SEGURO") == "1",
        "PERMANENT_SESSION_LIFETIME": timedelta(hours=8),
        "WTF_CSRF_TIME_LIMIT": None,  # o token vale enquanto a sessão valer
        "UPLOAD_FOLDER": Path(
            os.environ.get("UPLOAD_DIR", RAIZ / "static" / "uploads")
        ),
        "MAX_CONTENT_LENGTH": 3 * 1024 * 1024,  # limite geral: 3 MB
    }