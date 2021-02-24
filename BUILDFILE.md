To create your own fork of this project, a file named .build is needed in the same folder as the appliaction. 

Follow the bellow steps for the formatting.

{
    "version": "{the version of your launcher, normally should match the version you forked}"
	"dev":{weahter the version is a devloper version or not},
    "developer": "your name",
    "crash-reports-folder":"folder for crash reports to be sent to",
    "illegal-chars": [ //a bunch of characters that cannot be in a windows file named
        "",
        "*",
        ".",
        "",
        "/",
        "\\",
        "[",
        "]",
        ":",
        ";",
        "|",
        ","
    ],
    "illegal-names": [ //dissallowed windows file names
        "ON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9"
    ],
    "log-file": "app.log", //where the log for the launcher should go
    "name": "Java miniProjects", //the name of your project
    "programing-lanauge": "Python 3.9.1", //the language you use to code the project (currently optional)
    "raw-server": "https://raw.githubusercontent.com/JeffAxe123/miniProjects/v2", //the server used to downlaod files from  (must fololw the folder struture)
    "settings": ["folders.json","options.json"], //folders.json > configeraton for folder names, options.json > other options.
    "used-server": "https://github.com/JeffAxe123/miniProjects" //the srrver used for the "Visit Homepage"
}
