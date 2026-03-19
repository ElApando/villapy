""" Prueba Unitaria google creación """

#pylint: disable=wrong-import-position

import sys
from pathlib import Path

from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from villapy.cloud.google.drive import GoogleTools

class TestGoogleDrive:
    """ Prueba Uniatria de registro """

    def test_drive_replace_file(self):
        """ Prueba Unitaria remplazo de archivo"""

        fake_service = Mock()

        fake_service.files.return_value.list.return_value.execute.return_value = {
            "files": [{"id": "123"}]
        }

        fake_service.files.return_value.update.return_value.execute.return_value = {
            "id": "123"
        }

        with patch("villapy.cloud.google.drive.Credentials"), \
            patch("villapy.cloud.google.drive.build", return_value=fake_service), \
            patch("villapy.cloud.google.drive.MediaFileUpload"):

            g = GoogleTools(di_scope={"scope": {"drive" : ["scope"]},
                                    "folder_id": {"prd": "token"}},
                            di_routes={"client": "client.json",
                                        "token": "token",
                                        "file_prd": "prove_file.csv",
                                        "name_file": "prove_file.csv"},
                            di_logs={"type": False, "mode_file": False, "word": ""})

            result = g.drive_upload_or_replace()

        assert result["id"] == "123"

    def test_drive_create_file(self):
        """ Prueba Unitaria creación de archivo"""

        fake_service = Mock()

        fake_service.files.return_value.list.return_value.execute.return_value = {
            "files": []
        }

        fake_service.files.return_value.create.return_value.execute.return_value = {
            "id": "999",
            "name": "test.csv"
        }

        with patch("villapy.cloud.google.drive.Credentials"), \
            patch("villapy.cloud.google.drive.build", return_value=fake_service), \
            patch("villapy.cloud.google.drive.MediaFileUpload"):

            g = GoogleTools(di_scope={"scope": {"drive" : ["scope"]},
                                    "folder_id": {"prd": "token"}},
                            di_routes={"client": "client.json",
                                        "token": "token",
                                        "file_prd": "prove_file.csv",
                                        "name_file": "prove_file.csv"},
                            di_logs={"type": False, "mode_file": False, "word": ""})

            result = g.drive_upload_or_replace()

        assert result["id"] == "999"

# Finite Incantatem
