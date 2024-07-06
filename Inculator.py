print("Hagg4r 👺")
import os
import subprocess
import requests
from requests.exceptions import RequestException, SSLError
from datetime import datetime
import pymysql
import urllib3
import time
import sys

urllib3.disable_warnings()

file_count = 1  # Initialize file_count globally

def run_command(command):
    """Run a command and return its output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def run_sudo_command(command):
    """Run a command with sudo and return its output."""
    result = subprocess.run(['sudo'] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def save_to_file(filepath, data):
    """Save data to a file."""
    with open(filepath, 'a') as file:
        file.write(data + '\n')

def install_tools():
    """Install necessary tools if not already installed."""
    tools = {
        "uniscan": ["sudo", "apt-get", "install", "-y", "uniscan"],
        "nmap": ["sudo", "apt-get", "install", "-y", "nmap"],
        "sqlmap": ["sudo", "apt-get", "install", "-y", "sqlmap"],
        "whois": ["sudo", "apt-get", "install", "-y", "whois"],
        "subfinder": ["sudo", "apt-get", "install", "-y", "subfinder"]
    }
    
    for tool, install_command in tools.items():
        print(f"Checking if {tool} is installed...")
        if not is_tool_installed(tool):
            print(f"{tool} not found. Installing {tool}...")
            stdout, stderr = run_sudo_command(install_command)
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
        else:
            print(f"{tool} is already installed.")

def is_tool_installed(tool_name):
    """Check if a tool is installed."""
    return subprocess.call(["which", tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the animated header 'hagg4rscan'."""
    colors = ['\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[95m', '\033[96m']
    header = """
    ,:'/¯/`:,       .·/¯/`:,'                ,.-:~:-.                             __'                              __'                          ,.-:~:-.                .:'/*/'`:,·:~·–:.,           
  /:/_/::::/';    /:/_/::::';             /':::::::::'`,                    ,.·:'´::::::::`'·-.                ,.·:'´::::::::`'·-.                 /':::::::::'`,             /::/:/:::/:::;::::::/`':.,'     
 /:'     '`:/::;  /·´    `·,::';          /;:-·~·-:;':::',                 '/::::::::::::::::::';             '/::::::::::::::::::';              /;:-·~·-:;':::',          /·*'`·´¯'`^·-~·:–-'::;:::'`;    
 ;         ';:';  ;         ';:;        ,'´          '`:;::`,              /;:· '´ ¯¯  `' ·-:::/'            /;:· '´ ¯¯  `' ·-:::/'            ,'´          '`:;::`,        '\                       '`;::'i‘  
 |         'i::i  i         'i:';°      /                `;::\           /.'´      _         '`;/' ‘         /.'´      _         ';/' ‘          /                `;::\         i       i':/:::';       ,:'        
 'i        i':/_/:';        ;:';°   i'       ,';´'`;         '\:::', ‘  /     /':::::/;::::_::::::::;‘    /     /':::::/;::::_::::::::;‘     i'       ,';´'`;         '\:::', ‘     i       i/:·'´       ,:'      
  ;       i·´   '`·;       ;:/°  ,'        ;' /´:`';         ';:::'i‘,'     ;':::::'/·´¯     ¯'`·;:::¦‘ ,'     ;':::::'/·´¯`·;:::¦‘`;   ,'        ,;::/'`·.,_'     
   'i     i         i';   ,'´             ,:/'¯/'`·:':::';'      \::'·´,'::':,'        ;:::::/´  ;          ;:::::/´   i'::':/´  ;            ;:::::/´    ;::::/´'`·,'´':,
   """

    for color in colors:
        print(color + header)
        time.sleep(0.5)

def get_ip_info(ip):
    """Get IP information using an external service."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", verify=False)
        response.raise_for_status()
        return response.json()
    except (RequestException, SSLError) as e:
        return str(e)

def scan_with_uniscan(target):
    """Run Uniscan on the target."""
    command = ["uniscan", "-u", target, "-qweds"]
    stdout, stderr = run_command(command)
    save_to_file("uniscan_results.txt", stdout)
    if stderr:
        save_to_file("uniscan_errors.txt", stderr)
    return stdout, stderr

def scan_with_nmap(target):
    """Run Nmap on the target."""
    command = ["nmap", "-sV", target]
    stdout, stderr = run_command(command)
    save_to_file("nmap_results.txt", stdout)
    if stderr:
        save_to_file("nmap_errors.txt", stderr)
    return stdout, stderr

def scan_with_sqlmap(target):
    """Run SQLMap on the target."""
    command = ["sqlmap", "-u", target, "--batch"]
    stdout, stderr = run_command(command)
    save_to_file("sqlmap_results.txt", stdout)
    if stderr:
        save_to_file("sqlmap_errors.txt", stderr)
    return stdout, stderr

def extract_files_from_db(target):
    """Extract files from a database using SQLMap."""
    # Adjust the command to specify the file extraction options
    command = [
        "sqlmap", "-u", target, "--batch", "--dump", "--output-dir=output",
        "--technique=BEUSTQ", "--files"  # Modify options based on what you need
    ]
    stdout, stderr = run_command(command)
    save_to_file("sqlmap_file_extraction_results.txt", stdout)
    if stderr:
        save_to_file("sqlmap_file_extraction_errors.txt", stderr)
    return stdout, stderr

def run_whois(domain):
    """Run Whois on the domain."""
    command = ["whois", domain]
    stdout, stderr = run_command(command)
    save_to_file("whois_results.txt", stdout)
    if stderr:
        save_to_file("whois_errors.txt", stderr)
    return stdout, stderr

def run_subfinder(domain):
    """Run Subfinder on the domain."""
    command = ["subfinder", "-d", domain]
    stdout, stderr = run_command(command)
    save_to_file("subfinder_results.txt", stdout)
    if stderr:
        save_to_file("subfinder_errors.txt", stderr)
    return stdout, stderr

def log_to_database(host, user, password, db, data):
    """Log data to a MySQL database."""
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=db)
        cursor = connection.cursor()
        sql = "INSERT INTO scan_results (scan_data, timestamp) VALUES (%s, %s)"
        cursor.execute(sql, (data, datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error logging to database: {e}")

def main():
    """
    Main function to orchestrate the scans.
    - Installs required tools.
    - Runs Uniscan, Nmap, SQLMap, Whois, and Subfinder on the target.
    - Extracts files from a database and logs the results to a file and database.
    """
    clear_screen()
    print_header()
    
    install_tools()
    
    target = input("Enter the domain: ")
    print(f"Target: {target}")
    
    # Run scans
print("\n[1] Running Uniscan...")
uniscan_stdout, uniscan_stderr = scan_with_uniscan(target)
print(uniscan_stdout)
if uniscan_stderr:
    print(f"Uniscan errors:\n{uniscan_stderr}")
    print("\n[2] Running Nmap...")
    nmap_stdout, nmap_stderr = scan_with_nmap(target)
    print(nmap_stdout)
    
    print("\n[3] Running SQLMap...")
    sqlmap_stdout, sqlmap_stderr = scan_with_sqlmap(target)
    print(sqlmap_stdout)
    
    print("\n[4] Extracting files from database with SQLMap...")
    file_extraction_stdout, file_extraction_stderr = extract_files_from_db(target)
    print(file_extraction_stdout)
    
    print("\n[5] Running Whois...")
    whois_stdout, whois_stderr = run_whois(target)
    print(whois_stdout)
    
    print("\n[6] Running Subfinder...")
    subfinder_stdout, subfinder_stderr = run_subfinder(target)
    print(subfinder_stdout)
    
    # Define database connection parameters
    db_host = "localhost"
    db_user = "root"
    db_password = "password"
    db_name = "scan_results_db"
    
    # Log results to the database
    try:
        log_to_database(db_host, db_user, db_password, db_name, uniscan_stdout)
        log_to_database(db_host, db_user, db_password, db_name, nmap_stdout)
        log_to_database(db_host, db_user, db_password, db_name, sqlmap_stdout)
        log_to_database(db_host, db_user, db_password, db_name, file_extraction_stdout)
        log_to_database(db_host, db_user, db_password, db_name, whois_stdout)
        log_to_database(db_host, db_user, db_password, db_name, subfinder_stdout)
    except Exception as e:
        print(f"An error occurred while logging to the database: {e}")

if __name__ == "__main__":
    main()