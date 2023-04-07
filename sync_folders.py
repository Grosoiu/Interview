import os
import shutil
import time
import hashlib

#This function creates a replica of a folder to a given path.
#All of the changes that were made synce syncing will be saved in a log file
#An example usage will be provided in main
#The synchronization will work for as long as the script is running
#If the syncrhronization was supposed to be done rarely(eg: once a day), I would have personally made the function to 
#syncronize the folders once and run a cron job to automate the process

#The interval is given in seconds

#Based on the importance of the log files and whether there should be log analytics I would monitor the logs in a Grafana-Loki architecture. 

def sync(source, destination, log_file_path):
    print(source)
    print(destination)
    try:
        if not os.path.exists(destination): ## Daca nu exista fisierul il cream
            os.mkdir(destination)

        #Loop pentru sincronizare:
        for item in os.listdir(source):
            src_item_path = os.path.join(source, item)
            replica_item_path = os.path.join(destination, item)

            # Fisierele le copiem in folderul destinatie
            if os.path.isfile(src_item_path):
                if not os.path.exists(replica_item_path):
                    shutil.copy2(src_item_path, replica_item_path)
                    print(f"Copied file: {src_item_path} -> {replica_item_path}")
                    with open(log_file_path, "a") as f:
                        f.write(f"Copied file: {src_item_path} -> {replica_item_path}\n")
                else:
                    # Verificam daca fisierul s-a schimbat
                    src_file_hash = hashlib.md5(open(src_item_path, "rb").read()).hexdigest()
                    replica_file_hash = hashlib.md5(open(replica_item_path, "rb").read()).hexdigest()

                    if src_file_hash != replica_file_hash:
                        shutil.copy2(src_item_path, replica_item_path)
                        print(f"Updated file: {replica_item_path}")
                        with open(log_file_path, "a") as f:
                            f.write(f"Updated file: {replica_item_path}\n")

            # for item in os.listdir returneaza atat fisiere cat si directoare, daca e director folosim recursivitatea
            elif os.path.isdir(src_item_path):
                sync(src_item_path, replica_item_path, log_file_path)

        # Stergem fisierele sau directoarele care se afla in destinatie, dar nu se afla in sursa.
        for item in os.listdir(destination):
            replica_item_path = os.path.join(destination, item)
            src_item_path = os.path.join(source, item)

            if not os.path.exists(src_item_path):
                if os.path.isfile(replica_item_path):
                    os.remove(replica_item_path)
                    print(f"Deleted file: {replica_item_path}")
                    with open(log_file_path, "a") as f:
                        f.write(f"Deleted file: {replica_item_path}\n")
                elif os.path.isdir(replica_item_path):
                    shutil.rmtree(replica_item_path)
                    print(f"Deleted folder: {replica_item_path}")
                    with open(log_file_path, "a") as f:
                        f.write(f"Deleted folder: {replica_item_path}\n")


    except Exception as e:
        print(f"Error: {e}")