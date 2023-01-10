import secrets
from typing import Any
from varname import nameof
from cryptography import fernet

from app.api import exceptions
from app import config
from app.services.database.mongodb import collections
from app.api.routes.projects import schemas


def process(
    request: schemas.CreateOrUpdateProject
) -> Any:
    if collections.projects.is_project_name_taken(name=request.name):
        raise exceptions.NameTakenException(field=nameof(request.name))

    private_key, encrypted_private_key = _generate_private_key()

    project_id = collections.projects.create_project(
        name=request.name,
        private_key=encrypted_private_key
    )
    project = collections.projects.get_project(project_id=project_id)
    return schemas.ProjectWithPrivateKey(
        **project,
        private_key=private_key
    )


def _generate_private_key() -> tuple[str, str]:
    private_key = secrets.token_hex()
    f = fernet.Fernet(config.SECRET_KEY.encode())
    encrypted_private_key = f.encrypt(private_key.encode()).decode()
    return private_key, encrypted_private_key
