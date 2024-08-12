import os
import subprocess
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration parameters
basepath = config.get('Paths', 'handShakefiles')
wordlists = config.get('Paths', 'wordlists').split(',')
hashcat_path = config.get('Executables', 'hashcat_path', fallback='hashcat')  # Use system default if not specified

def main():
    """
    Main function to orchestrate the WPA cracking process.
    """
    for cap_file in find_cap_files(basepath):
        print(f"Processing: {cap_file}")
        converted_cap = convert_to_22000(cap_file)
        if converted_cap:
            crack_wpa(converted_cap)

def find_cap_files(path):
    """
    Finds all .cap files within a given directory.

    Args:
        path (str): The directory to search.

    Yields:
        str: The path to each .cap file found.
    """
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".cap"):
                yield os.path.join(root, file)

def convert_to_22000(cap_file):
    """
    Converts a .cap file to the 22000 hash format using hcxpcapngtool.

    Args:
        cap_file (str): The path to the .cap file.

    Returns:
        str: The path to the converted .22000 file, or None if conversion fails.
    """
    output_file = f"{cap_file}.22000"
    try:
        subprocess.run(
            ["hcxpcapngtool", "-o", output_file, "-E", f"{cap_file}_L", cap_file],
            check=True,  # Raise an error if the command fails
            stdout=subprocess.DEVNULL,  # Suppress output
            stderr=subprocess.DEVNULL,
        )
        return output_file
    except subprocess.CalledProcessError:
        print(f"Error converting {cap_file}")
        return None

def crack_wpa(hash_file):
    """
    Cracks a WPA hash file using hashcat.

    Args:
        hash_file (str): The path to the .22000 hash file.
    """
    output_file = f"{hash_file}_CRACKED.txt"
    command = [
        hashcat_path, 
        "-a", "0", 
        "-m", "22000", 
        hash_file, 
        "-D", "2", 
        *wordlists,  # Expand the wordlist paths
        "--status", 
        "--status-timer", "2", 
        "--outfile",
        output_file
    ]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline().decode('utf-8').strip()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output)
    except Exception as e:
        print(f"Error during cracking: {e}")

if __name__ == "__main__":
    main()

