import os
import logging
import argparse
import shutil
import time


# Setting up the logging configuration (checks if the log file exists. If not, it creates one. If it exists, it will append the new info.)
def setup_logging(log_file):
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if os.path.isdir(log_file):
        log_file = os.path.join(log_file, "sync.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


# Setting up the function that syncs the files between the source and replica folders
def sync_folders(source_folder, replica_folder):
    logging.info(f"Syncing {source_folder} to {replica_folder}...")
    # Sync counter
    synced_files = 0
    for root, dirs, files in os.walk(source_folder):
        # create directories in replica_folder that don't exist
        relative_path = os.path.relpath(root, source_folder)
        replica_root = os.path.join(replica_folder, relative_path)
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)
            logging.info(f"Created directory {replica_root}")
            synced_files += 1

        # sync files in the directories
        for file in files:
            source_path = os.path.join(root, file)
            replica_path = os.path.join(replica_root, file)
            if not os.path.exists(replica_path) or os.stat(source_path).st_mtime - os.stat(replica_path).st_mtime > 1:
                shutil.copy2(source_path, replica_path)
                logging.info(f"Copied {source_path} to {replica_path}")
                synced_files += 1

        # remove files and directories from replica that don't exist in source
        for item in os.listdir(replica_root):
            replica_item_path = os.path.join(replica_root, item)
            source_item_path = os.path.join(root, item)
            if not os.path.exists(source_item_path):
                if os.path.isdir(replica_item_path):
                    shutil.rmtree(replica_item_path)
                    logging.info(f"Removed directory {replica_item_path}")
                else:
                    os.remove(replica_item_path)
                    logging.info(f"Removed file {replica_item_path}")
                synced_files += 1

    if synced_files == 0:
        logging.info(
            "No changes were made during sync.\n --------------------")
    else:
        logging.info(
            f"{synced_files} changes were made during sync.\n --------------------")


# Define main function to extract the arguments from the command
def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source", type=str, help="Source folder path")
    parser.add_argument("replica", type=str, help="Replica folder path")
    parser.add_argument("interval", type=int, help="Sync interval in seconds")
    parser.add_argument("log_file", type=str, help="Log file path")
    args = parser.parse_args()

    setup_logging(args.log_file)

    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
