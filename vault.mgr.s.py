import tarfile
import subprocess
import shutil
import os
import getpass
from pathlib import Path
from datetime import datetime


#path
path_check = Path.home()

#stat
stat = shutil.disk_usage(path_check) 

#conversion
BYTES_PER_GB = 1024**3

if stat.free <= 5*1024**3 :
    print("[!] Not Enough Disk Space: Terminating session.")
    exit(1)


# --- Environment Mapping ---
HOME = Path.home()
VAULT_SOURCE = HOME / "notes"
RESTORE_DIR = HOME / "temp_rest"
TEMP_DIR = HOME / "TMP"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")


   
def display_splash():
    """Renders the sanroku-36's Vault Manager Splash Screen"""
    crow_ascii = r"""
             _____
          /  ____  \      [ SYSTEM: SECURE ]
         /  /    \  \     [ NODE:   SANROKU-36  ]
        |  | (0)(0) |  |   
         \  \  __  /  /   
          \__\____/__/    
             /    \       
     Wal    /      \    la
    ------------------------
    SANROKU-36'S VAULT MANAGER v1.3 S
    Intended for Self Destructive decryption only...
    (DO NOT USE THIS TO DECRYPT FILES OVER 5GB...)
    
    ------------------------
    """
    print(crow_ascii)

def run_sync():
    """Option 1: System -> Vault"""
    print(f"[*] Current User Home: {HOME}")
    target_input = input("Path to encrypt (relative to home): ")
    
    source_path = Path(target_input).expanduser()
    if not source_path.is_absolute():
        source_path = HOME / target_input

    if not source_path.exists():
        print(f"[!] Path invalid: {source_path}")
        return

    passphrase = getpass.getpass("Set Vault Passphrase: ")
    VAULT_SOURCE.mkdir(parents=True, exist_ok=True)
    
    safe_name = source_path.name if source_path.name else "root_backup"
    temp_tar = VAULT_SOURCE / f"{safe_name}_{TIMESTAMP}.tar.gz"
    final_gpg = VAULT_SOURCE / f"{safe_name}_{TIMESTAMP}.tar.gz.gpg"

    print(f"[>] Compressing {source_path}...")
    try:
        with tarfile.open(temp_tar, "w:gz") as tar:
            tar.add(source_path, arcname=source_path.name)
        
        subprocess.run([
            "gpg", "--symmetric", "--batch", "--passphrase", passphrase,
            "--cipher-algo", "AES256", "-o", str(final_gpg), str(temp_tar)
        ], check=True, capture_output=True)
        os.remove(temp_tar)
        print(f"[+] Secure: {final_gpg.name}")
    except Exception as e:
        print(f"[!] Failure: {e}")

def run_breaker():
    """Option 2: Restricted Vault -> Restore (VOLATILE RAM MODE)"""
    temp_tar = None
    RAM_MOUNT = Path("/mnt/ram_vault")
    # RESTORE_DIR is already defined as HOME / "temp_rest"
    
    # --- PHASE 1: Detection ---
    vault_files = list(VAULT_SOURCE.glob("*.gpg"))
    if not vault_files:
        print("[!] No vaults detected.")
        return

    for i, f in enumerate(vault_files):
        print(f"{i+1}. {f.name}")
    
    try:
        choice = int(input("\nSelect index: ")) - 1
        gpg_file = vault_files[choice]
    except (ValueError, IndexError):
        print("[!] Invalid selection.")
        return
def run_breaker():
    """Option 2: Restricted Vault -> Restore (VOLATILE RAM MODE)"""
    RAM_MOUNT = Path("/mnt/ram_vault")
    temp_tar = RAM_MOUNT / "temp_restore.tar.gz"
    # RESTORE_DIR is already defined as HOME / "temp_rest"
    
    # --- PHASE 1: Detection ---
    vault_files = list(VAULT_SOURCE.glob("*.gpg"))
    if not vault_files:
        print("[!] No vaults detected.")
        return

    for i, f in enumerate(vault_files):
        print(f"{i+1}. {f.name}")
    
    try:
        choice = int(input("\nSelect index: ")) - 1
        gpg_file = vault_files[choice]
    except (ValueError, IndexError):
        print("[!] Invalid selection.")
        return

    passphrase = getpass.getpass("Enter Passphrase: ")

    # --- PHASE 2: Ghost Drive Setup ---
    try:
        print("[*] Initializing Volatile RAM Shield...")
        # Create mount point and mount tmpfs
        subprocess.run(["sudo", "mkdir", "-p", str(RAM_MOUNT)], check=True)
        subprocess.run(["sudo", "mount", "-t", "tmpfs", "-o", "size=5000M", "tmpfs", str(RAM_MOUNT)], check=True)
        # Give your user ownership of the RAM
        subprocess.run(["sudo", "chown", f"{os.getlogin()}:{os.getlogin()}", str(RAM_MOUNT)], check=True)

        # Handle the Symlink logic
        if RESTORE_DIR.exists() or RESTORE_DIR.is_symlink():
            shutil.rmtree(RESTORE_DIR) if RESTORE_DIR.is_dir() and not RESTORE_DIR.is_symlink() else RESTORE_DIR.unlink()
        
        os.symlink(RAM_MOUNT, RESTORE_DIR)
        
        # --- PHASE 3: Decryption ---
        # Ensure we are using absolute strings for GPG
        input_vault = str(gpg_file.absolute())
        output_tar = str((RAM_MOUNT / "temp_restore.tar.gz").absolute())

        print(f"[#] Decrypting: {gpg_file.name} -> RAM")
        
        result = subprocess.run([
            "gpg", "--decrypt", "--batch", "--passphrase", passphrase,
            "--pinentry-mode", "loopback", # Forces GPG to use the provided passphrase
            "-o", output_tar, input_vault
        ], capture_output=True, text=True)
        
        # ... (Decryption and Extraction Logic) ...
        
        print(f"[+] Extraction complete. Data is live in RAM.")
        
        # --- THE ANCHOR ---
        print("\n" + "="*40)
        print("VAULT IS OPEN: Files are in ~/temp_rest (Check the @HOME folder(your user's home folder)")
        print("You already know where that is if you managed to configure this program...")
        print("WARNING: Closing this script or pressing Enter will SHRED the data.")
        print("="*40)
        
        input("\nPress [ENTER] to secure the vault and exit...") 
        # The script stays HERE until you hit Enter.
        
    except Exception as e:
        print(f"[!] Failure: {e}")

        if result.returncode != 0:
            print(f"[!] GPG Error: {result.stderr}")
            return

    except Exception as e:
        print(f"[!] Critical Failure: {e}")
    

    
    finally:
        print("[*] Initiating Deep Shred of temporary artifacts...")
        
        # 1. Shred the temp tarball (overwrite 3 times + final delete)
        if temp_tar and temp_tar.exists():
            try:
                # -u removes the file after overwriting
                # -n 3 performs 3 passes of random data
                subprocess.run(["shred", "-u", "-n", "3", str(temp_tar)], check=True)
                print("[+] Temp archive shredded.")
            except Exception as e:
                print(f"[!] Shred failed, falling back to standard delete: {e}")
                temp_tar.unlink(missing_ok=True)

        # 2. Sever the Link
        if RESTORE_DIR.is_symlink():
            RESTORE_DIR.unlink()
            print("[+] Symlink severed.")

        # 3. Unmount the RAM
        # Using -l (lazy) ensures it closes even if a file explorer is open
        subprocess.run(["sudo", "umount", "-l", str(RAM_MOUNT)], stderr=subprocess.DEVNULL)
        print("[+] Ghost Drive dismantled. RAM cleared.")

if __name__ == "__main__":
    os.system('clear') # Keep the terminal focused
    display_splash()
    
    print(f"USER: {os.getlogin()} | DATE: {datetime.now().strftime('%Y-%m-%d')}")
    print("1. Sync (Backup to Vault)")
    print("2. Breaker (Restore from Vault)")
    
    cmd = input("\nExecute command: ")
    if cmd == "1":
        run_sync()
    elif cmd == "2":
        run_breaker()
    else:
        print("[!] Terminating session.")
