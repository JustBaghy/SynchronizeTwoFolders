This is a Python script to sync two folders. The sync is one way, between a Source folder and a Replica folder. The sync is performed at a fix interval (calculated in seconds). File creation/copying/removal operations are logged to a file and to the console output.
Before running the script, please make sure you have the latest Python installed (to avoid any compatibility issues)

In order to run the script please use the following steps: 
1. Open Command Prompt aka CMD (preferred to "Run as Administrator" to avoid any permission errors when creating and/or deleting files/folders)
2. Change the path to the folder where you've downloaded the .py file (you can use the command "cd path_to_the_file)
3. Use the following command: "python SyncronizeTwoFolders.py path_to _source path_to_replica sync_interval path_to_log"
The sync_interval is in seconds. As an example, if you want the sync to be performed every minute, set the sync_interval to 60.

In order to stop the script, press CTRL+C keys.
