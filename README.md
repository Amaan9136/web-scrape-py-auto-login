# Common Code Folder

This folder contains various Python scripts designed to interact with user credentials, databases, and HTML references for checking balances and verifying credentials.

## Files Overview

### 1. `attribute-checker.py`
- **Function:** Verify the correctness of credentials
- **Usage:** Use this for a new type of app to extract HTML references from a website
- **Note:** Less efficient as it requires assignment of details from HTML

### 2. `main-checkbalancewith2details.py`
- **Function:** Check balance directly from the database by pasting the table from `user-credentials-from-database.txt`
- **Usage:** Check details in the format: mobile password and known login details of HTML
- **Format:** 
    ```
    mobile   password
    7353346164   7353346164s
    ```
- **Note:** Best speed only if you have login details prior

### 3. `main-checkbalancewith2details.py`
- **Function:** Check balances for previously verified details from `main-checkbalancewith2details.py`
- **Usage:** Check details in the format: mobile password balance to check the balance of successful details
- **Format:** 
    ```
    mobile   password   balance
    7353346164   7353346164s   100.00
    ```
- **Note:** Best speed only if you have login details prior

## Usage Notes
- Each file serves specific purposes depending on the available details and prior verification.
- Efficiency varies based on the availability of login details and the method of credential verification.

### Note for Optimization
- For best performance, use `main-checkbalancewith2details.py` after successful verification with `attribute-checker.py` or with known login details.

+++++++
