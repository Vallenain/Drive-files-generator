from datetime import datetime
import logging
import json
from timeit import default_timer as timer
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from config import CONFIG
from drive_mime_types import DRIVE_MIME_TYPES

logging.getLogger().setLevel(logging.INFO)


drive_service = None


class JSONTreeError(TypeError):
    pass


def make_creds_from_file(creds_path):
    with open(creds_path, "r") as file:
        json_creds = json.load(file)
        return Credentials(
            token=json_creds.get("token"),
            refresh_token=json_creds.get("refresh_token"),
            scopes=json_creds.get("scopes"),
            token_uri=json_creds.get("token_uri"),
            client_id=json_creds.get("client_id"),
            client_secret=json_creds.get("client_secret"),
        )


def export_cred_to_file(creds_path, creds):
    json_creds = creds.to_json()
    with open(creds_path, "w") as file:
        file.write(json_creds)


def build_drive_service():
    global drive_service
    if os.path.isfile(CONFIG.get('CREDS_PATH', '')):
        creds = make_creds_from_file(CONFIG['CREDS_PATH'])
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CONFIG["CLIENT_SECRET_PATH"], scopes=CONFIG["SCOPES"]
        )
        creds = flow.run_console()
    if CONFIG.get('CREDS_PATH'):
        export_cred_to_file(CONFIG["CREDS_PATH"], creds)
    drive_service = build("drive", "v3", credentials=creds, cache_discovery=False)


def read_json(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def create_file(parent_id, mime_type, name=None):
    if not name:
        name = str(datetime.now())
    body = {
        "name": name,
        "mimeType": mime_type,
        "description": "File auto created by Drive files generator tool"
    }
    if parent_id != "my-drive":
        body['parents'] = [parent_id]
    logging.info(
        "About to create a {} called {} in folder {}".format(mime_type, name, parent_id)
    )
    response = (
        drive_service.files().create(enforceSingleParent=True, body=body).execute()
    )
    logging.info("Successfully created!")
    return response.get("id")


def process_level(parent_folder_id, json_file_tree_level):
    drive_file_types = DRIVE_MIME_TYPES.keys()
    folders = json_file_tree_level.get("folders")

    for key in json_file_tree_level:
        logging.info("Processing {} under {}".format(key, parent_folder_id))

        if key in drive_file_types:
            value = json_file_tree_level.get(key)

            if isinstance(value, str):
                logging.warning(
                    "Integer or list of string expected for property {} under {}. Skipping it.".format(
                        key, parent_folder_id
                    )
                )
                continue

            # In case it's an integer
            elif isinstance(value, int):
                logging.info("There are {} unnamed {} to create".format(value, key))
                for i in range(value):
                    create_file(parent_folder_id, DRIVE_MIME_TYPES.get(key))
                    logging.info("{} created: {}/{}".format(key, i + 1, value))

            # In case it's a list
            elif isinstance(value, list):
                logging.info("There are {} named {} to create".format(len(value), key))
                for idx, file_name in enumerate(value):
                    if not isinstance(file_name, int) and not isinstance(
                        file_name, str
                    ):
                        logging.warning(
                            "Only strings and integers can be accepted as valid filenames in array of {} "
                            "under {}. Skipping it.".format(key, parent_folder_id)
                        )
                        continue

                    create_file(
                        parent_folder_id, DRIVE_MIME_TYPES.get(key), str(file_name)
                    )

                    logging.info("{} created: {}/{}".format(key, idx + 1, len(value)))

            # Unexpected type
            else:
                logging.warning(
                    "Expected strings or list of strings/integers for {} under {}. Skipping it.".format(
                        key, parent_folder_id
                    )
                )
        elif key == "folders":
            pass
        else:
            logging.info("Unexpected mime type: {}. Skipping it.".format(key))

    if folders is not None:
        if isinstance(folders, dict):
            for folder in folders:
                logging.info(
                    "{} folders to be created under {}".format(
                        len(folders), parent_folder_id
                    )
                )
                logging.info(
                    "Creating folder {} under {}".format(folder, parent_folder_id)
                )
                folder_id = create_file(
                    parent_folder_id, "application/vnd.google-apps.folder", folder
                )
                logging.info(
                    "Folder {} has been created under {} with id {}".format(
                        folder, parent_folder_id, folder_id
                    )
                )
                process_level(folder_id, folders.get(folder))
        else:
            raise JSONTreeError("Dict expected for folders")


def create_drive_files(json_file_tree):
    if not isinstance(json_file_tree, dict):
        raise JSONTreeError("Dict / map expected as container of the whole tree")
    if len(json_file_tree) != 1:
        raise JSONTreeError(
            "One and only one key expected at first level of the tree: the parent folder ID"
        )
    parent_folder_id = list(json_file_tree.keys())[0]
    process_level(parent_folder_id, json_file_tree.get(parent_folder_id))


if __name__ == "__main__":
    logging.info("Launching the tool!")
    build_drive_service()
    logging.info("Scopes have been authorized")
    json_object = read_json(CONFIG["JSON_FILE_TREE_PATH"])
    logging.info("Json file has been read")
    logging.info("Recording time")
    start = timer()
    create_drive_files(json_object)
    end = timer()
    logging.info("It's all good! Elapsed time: {}s".format(end - start))
