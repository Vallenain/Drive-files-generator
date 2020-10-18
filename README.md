# Drive files generator

Tool to generate folders and documents on Google Drive from a JSON file.

##JSON file tree

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
or `my-drive` if you want it to be the root of your Drive. A shared drive ID can be passed too.

2. Inside a folder, you can specify the different Google Drive elements you want to create. Either documents from the
the list, or the special "folders" entry if you want to create subfolders.

3. A folder is identified by its name (= its key). Exception for the root element which is `my-drive` or an existing ID.

4. To specify which Google Docs, Sheets, Sites (and so on) you want to create, you can either tell how many you want 
and they will have a timestamp for name (`"docs": 3` will create 3 Google Docs) or you can specify a list of names 
(`"docs": ["one", "two", "three"]`).

5. If you want to create an empty folder, just add an entry with an empty dict (`"my last folder": {}`)

6. Reference the path of the JSON file in `config.py`: 
##Credentials
At the moment, the script is not packaged and it is not a published app either. So you have to create your own GCP Oauth
client ID for installed app ([this procedure][1]).  
Download the JSON file and reference its path into the `config.py` file: `CLIENT_SECRET_PATH`.

The script will ask for permission to write into your Google Drive. After the scope authorization process is done, it
will save your refresh token + access token into a file if (and only if) a `CREDS_PATH` is specified in `config.py`.
Otherwise it will ask your permission at each run.

[1]: https://cloud.google.com/bigquery/docs/authentication/end-user-installed#client-credentials

##Run the script
To run the script, simply run (Python 3):  
```python main.py```

There is a lot to improve, I know... ;-)