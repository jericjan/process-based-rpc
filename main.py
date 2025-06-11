from pypresence import Presence
import time
import psutil 

# Dict of exe names and their app ID
names_to_ids = {
    "kamichu.exe": (1382331352543658004, "me when the 天活 hits", "kamichu")
}

connected_id = -1
RPC = Presence(-1)

while True:
    print("Loop start")
    # Iterate over all running processes
    if connected_id != -1:
        filt = filter(
            lambda x: x[1][0] == connected_id,
            names_to_ids.items()
        )
        try:
            proc_name = next(filt)[0]
            found = False
            for proc in psutil.process_iter(['name']):
                name = proc.info['name']
                if name == proc_name:
                    found = True
            if not found:
                print(f"{proc_name} was closed")
                RPC.close()
                connected_id = -1
        except StopIteration:
            pass    

    for proc in psutil.process_iter(['name']):
        try:
            # Get process information as a dictionary
            name = proc.info['name']
            if name in names_to_ids:
                app_id, desc, img_name = names_to_ids[name]
                if app_id != connected_id:
                    print(f"{name} detected")
                    connected_id = app_id
                    RPC = Presence(app_id)
                    RPC.connect()
                    RPC.update(state=desc, large_image=img_name)
                    print("Connected to RPC!")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle cases where the process might have terminated
            # or access is denied
            pass
    time.sleep(1)
