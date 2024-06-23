# Gmail API HappyFox Task

## How to use it
```bash
git clone https://github.com/taha20181/happyfox-task.git
cd happyfox-task

# Virtualenv modules installation (Unix based systems)
python3 -m venv myvenv
source myvenv/bin/activate

# Install python modules
pip install -r requirements.txt
```

## Configuration

1. **Place your `credentials.json` file**:
        - Place the `credentials.json` file you downloaded from the Google Cloud Console in the root directory of the project.

2. **Setup database connection** :
        - Make sure you have the below variables set in the environment.
        - Run `database.py` to create a table named Email.
    ```
    export DB_HOST=0.0.0.0
    export DB_PORT=1234
    export DB_USER=XXXX
    export DB_PASSWORD=XXXX
    export DB_NAME=XXXX
    ```

## Steps to run the project

1. **Run `fetch_emails.py`** : 
        - Fetches emails from your gmail account using Gmail API and store in the DB.
2. If not already authenticated, it will open the consent page, please allow and continue to proceed with fetching emails.
3. **Review `rules.json`** : 
        - Rules to filter emails and actions to perform on the filtered set of emails. Kindly follow similar nomenclature.
    ```
    {
        "rule_1" : {
            "apply_type" : "all",
            "cohorts" : [
                {
                    "field" : "FROM",
                    "condition" : "CONTAINS",
                    "value" : "swiggy.in"
                },
                {
                    "field" : "TO",
                    "condition" : "EQUALS",
                    "value" : "example@gmail.com"
                },
                {
                    "field" : "DATE",
                    "condition" : "IS_LESS_THAN",
                    "value" : 3
                }
            ],
            "actions" : [
                {
                    "type" : "MARK_READ",
                    "label" : "UNREAD"
                },
                {
                    "type" : "MOVE",
                    "label" : "STARRED"
                }
            ]
        }
    }
    ```
    - `apply_type` can either be `all` or `any`.
    - `condition` can have values `CONTAINS`, `NOT_CONTAINS`, `EQUALS` and `NOT_EQUALS` for string types, `IS_LESS_THAN` and `IS_GREATER_THAN` for date type.
    - `actions` can have types `MARK_READ`, `MARK_UNREAD` with label as `UNREAD` and `MOVE` with label like `INBOX` or `STARRED` etc.
    
4. **Run `process_emails.py`** : 
        - Read stored emails and process them as per rules mentioned in the `rules.json` file and perform a set of actions.