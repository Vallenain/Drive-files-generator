import pytest

from google_auth_oauthlib.flow import InstalledAppFlow

import main
from test_config import CREDS_PATH, CLIENT_SECRET_PATH


def test_read_json_with_none():
    with pytest.raises(TypeError):
        main.read_json()
    with pytest.raises(FileNotFoundError):
        main.read_json("")


@pytest.mark.parametrize("client_id_file_path", [CLIENT_SECRET_PATH])
def test_build_drive_service(mocker, client_id_file_path):
    submethod_mocked = mocker.patch.object(InstalledAppFlow, "run_console")
    submethod_mocked.return_value = main.make_creds_from_file(CREDS_PATH)
    main.build_drive_service(client_id_file_path)

    assert main.drive_service is not None


def test_make_creds_from_file():
    with pytest.raises(TypeError):
        main.make_creds_from_file()
    with pytest.raises(FileNotFoundError):
        main.make_creds_from_file("")
    assert main.make_creds_from_file(CREDS_PATH) is not None


def test_export_cred_to_file(tmpdir):
    creds = main.make_creds_from_file(CREDS_PATH)
    creds_tmp_path = "{}/creds.json".format(tmpdir)
    with pytest.raises(FileNotFoundError):
        main.export_cred_to_file("", creds)
    with pytest.raises(AttributeError):
        main.export_cred_to_file(creds_tmp_path, None)
    main.export_cred_to_file(creds_tmp_path, creds)
    assert main.make_creds_from_file(creds_tmp_path) is not None


PROCESS_LEVEL_INPUTS = [
    ({}, None),
    ({"sblah": "nothing"}, None),
    ({"folders": {}}, None),
    ({"folders": []}, main.JSONTreeError),
    ({"folders": {"multiple": {}, "folders": {}}}, None),
    ({"folders": {"my_folder": {"docs": 1}}}, None),
]


@pytest.mark.parametrize("tree, exception", PROCESS_LEVEL_INPUTS)
def test_process_level(mocker, tree, exception):
    parent_folder_id = "A_FAKE_ONE"
    mocker.patch("main.create_file", return_value="A_FAKE_ID")

    if exception:
        with pytest.raises(exception):
            main.process_level(parent_folder_id, tree)
    else:
        main.process_level(parent_folder_id, tree)


CREATE_DRIVE_FILES_INPUT = [
    ({}, main.JSONTreeError),
    ({"sblah": {}}, None),
    ({"sblah": {}, "sblah2": {}}, main.JSONTreeError),
    ({"my_drive": {"docs": 1}}, None),
    ([], main.JSONTreeError),
    ([{"docs": 1}], main.JSONTreeError),
]


@pytest.mark.parametrize("tree, exception", CREATE_DRIVE_FILES_INPUT)
def test_create_drive_files(mocker, tree, exception):
    mocker.patch("main.create_file", return_value="A_FAKE_ID")

    if exception:
        with pytest.raises(exception):
            main.create_drive_files(tree)
    else:
        main.create_drive_files(tree)
