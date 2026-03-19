""" Prueba Unitaria google acceso """

#pyright: reportUnusedVariable=false

#pylint: disable=wrong-import-position
#pylint: disable=unused-variable


import sys
from pathlib import Path

from unittest.mock import Mock, patch


sys.path.append(str(Path(__file__).resolve().parents[1]))

from villapy.cloud.google.auth import GoogleAuth

def test_drive_create_token(tmp_path: Path):
    """Doct"""

    token_file = tmp_path / "token.json"
    client_file = tmp_path / "client.json"

    fake_creds = Mock()
    fake_creds.to_json.return_value = '{"token":"fake"}'

    fake_flow = Mock()
    fake_flow.run_local_server.return_value = fake_creds

    with patch("villapy.cloud.google.auth.InstalledAppFlow") as mock_flow:

        mock_flow.from_client_secrets_file.return_value = fake_flow

        g = GoogleAuth(di_scope={"scope": {"drive" : ["scope"]}},
                   di_routes={"client": str(client_file),
                              "token": str(token_file)},
                   di_logs={"type": False, "mode_file": False, "word": ""})

        g.drive_create_token()


    assert token_file.exists()

def test_drive_check_token(tmp_path: Path):
    """DOC"""

    token_file = tmp_path / "token.json"

    fake_service = Mock()
    fake_service.about.return_value.get.return_value.execute.return_value = {
        "user": {"emailAddress": "test@gmail.com"}
    }

    with  patch("villapy.cloud.google.auth.Credentials") as mock_creds, \
          patch("villapy.cloud.google.auth.build") as mock_build:

        mock_build.return_value = fake_service

        g = GoogleAuth(di_scope={"scope": {"drive" : ["scope"]}},
                        di_routes={"client": "client.json",
                                    "token": str(token_file)},
                        di_logs={"type": False, "mode_file": False, "word": ""})

        g.drive_check_token()

    mock_build.assert_called_once()

# Finite Incantatem
