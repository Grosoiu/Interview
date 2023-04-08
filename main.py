#Example usage: python3 main.py $PATH_TO_SOURCE_DIR $PATH_TO_DESTINATION_DIR $PATH_TO_LOG_FILE $Interval(int)

# I debugged this program on windows, If the cli argument uses '\', it will replace it with '/'
 


import sys
import time
from sync_folders import sync
if __name__ == "__main__":
    # Parse command line arguments
    source_path = sys.argv[1]
    source_path = str(source_path)
    source_path.replace('\\', '/')
    replica_path = sys.argv[2]
    replica_path = str(replica_path)
    replica_path.replace('\\', '/')
    log_file_path = sys.argv[3]
    log_file_path = str(log_file_path)
    log_file_path.replace('\\', '/')
    interval = int(sys.argv[4])
    while True:
        sync(source_path,replica_path,log_file_path)
        time.sleep(interval)

