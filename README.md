# TaoBin Sample Transaction
Database 2022 Project

## Getting Started
### Requirements
|Name  | Recommended version(s)|   
|------|-----------------------|
|Python | 3.9 or higher |

### Install Packages
1. Clone this project repository to your machine.

    ```
    git clone https://github.com/tboonma/TaoBin-Database-Project.git
    ```
2. Get into the directory of this repository.

    ```
    cd TaoBin-Database-Project
    ```
3. Create a virtual environment.

    ```
    python -m venv venv
    ```
4. Activate the virtual environment.

    - for Mac OS / Linux.   
    ```
    source venv/bin/activate
    ```
    - for Windows.   
    ```
    venv\Scripts\activate
    ```
5. Install all required packages.

    ```
    pip install -r requirements.txt
    ```
6. Create `.env` file in the top-level and write down:

   ```
   CERT_LOCATION='<PATH_TO_PEM_FILE>'
   ```
