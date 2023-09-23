1. clone the repository
```
git clone https://github.com/Unikorn996/ku-polls.git
```

2. change the directory to ku-polls
```
cd ku-polls
```

3. create a virtual environment
```
python -m venv venv
```

4. create .env file
```
cp sample.env .env
```

5. configure the .env setting
```
nano .env
```

6. activate the virtual environment
```
venv\Scripts\activate (Windows)
source venv/bin/activate (MacOS, Linux)
```

7. install requirements from requirements.txt
```
pip install -r requirements.txt
```

8. run migrations
```
python manage.py migrate
```

9. load data (JSON)

```
python manage.py loaddata data/polls.json data/users-v1.json
```
