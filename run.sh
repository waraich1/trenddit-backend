export CLIENT_ID='7dlaGED5g8Z9nqyuWifKqA'
export SECRET_ID='qLG8_LvLVlix4p8gfjMJ1LOyTOZ8pg'
export USER_ID='Varun@legend'
export PASSWORD='trenddit-dev'



source ./venv/bin/activate

pip install -r requirements.txt

python3 application.py -p 500
