# Drive files generator

Tool to generate folders and documents on Google Drive from a JSON file.

## JSON file tree

The JSON file describes the file tree you want to create on Google Drive.

An example will help you understand the structure of it.
```json
{
  "my-drive": {
    "docs": ["My Google Docs"],
    "sheets": 3,
    "folders": {
      "ZORRO": {
        "forms": 1,
        "sites": ["Google Site #1", "Google Site #2"],
        "folders": {
          "my last folder": {}
        }   
      }
    }
  }
}
```

1. The outter object must have a single entry. The key is the ID of the folder where you want to create the file tree 
or the special value `my-drive` if you want it to be the root of your Drive. A shared drive ID can be passed too.

2. Inside a folder, you can specify the different Google Drive elements you want to create. Either documents from the
the list, or the special "folders" entry if you want to create subfolders.

3. A folder is identified by its name (= JSON key). Exception for the root element which is `my-drive` or an existing 
Google Drive ID.

4. To specify which Google Docs, Sheets, Sites (and so on) you want to create, you can either tell how many you want 
and they will have a timestamp for name (`"docs": 3` will create 3 Google Docs - not possible for folders at the moment) 
or you can specify a list of names (`"docs": ["one", "two", "three"]`).

5. If you want to create an empty folder, just add an entry with an empty dict (`"my last folder": {}`)


## Credentials
At the moment, the script is not packaged nor published as an app. So you have to create your own GCP Oauth
client ID for installed app ([this procedure][1]).  
Download the JSON file and pass it to the command line.

The script will ask for permission to write in Google Drive. After the scope authorization process is done, it
will save your refresh token + access token into a file if (and only if) you have passed `--store-creds` with a file
path to the command line.
Otherwise it will ask your permission at each run.

[1]: https://cloud.google.com/bigquery/docs/authentication/end-user-installed#client-credentials

## Run the script
```
usage: drive_files_gen.py [-h] [--store-creds STORE_CREDS] client_id_file json_file

Generate Google Drive folders and documents from a JSON file.

positional arguments:
  client_id_file        the client id JSON file, downloaded from GCP
  json_file             the Drive file tree, in JSON format

optional arguments:
  -h, --help            show this help message and exit
  --store-creds STORE_CREDS
                        if you want to store your creds (refresh + access token) on your filesystem, give it a file path
```

### Test the script
I've made a bit of unit testing with `pytest`. It requires to have both a JSON Oauth client file and 
a valid JSON credentials file (with the refresh token + access token).
You will see in `test_main.py` that I reference a `test_config` package, which is where I store the path to JSON files.

To test it, simply run `pytest`
