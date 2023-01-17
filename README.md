## trenddit-backend

## Initialize Trenddit
### run.sh
```
python3 -m venv ./venv
source ./venv/bin/activate

pip3 install --upgrade pip
pip3 install -r requirements.txt

export CLIENT_ID='XXXXXXXX'
export SECRET_ID='XXXXXXXX'
export PASSWORD='XXXXXXXX'
export USER_ID='XXXXXXXX'

python3 application.py -p 500

```

## Run Backend

sh run.sh
