## Setup and Running

### Create Virtual Environment
```bash
python3 -m venv venv
```

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Run the Application
```bash
python -m uvicorn app.main:app --reload
```
Invoice of cancelled gig is automatically deleted 
if you wish to reset the database, at the project root, run in the terminal: 
```bash
cd /pathToYourFile/projectName
source venv/bin/activate
python -m app.reset_db
```