### Install dependencies

`pip install -r requirements.txt`

### Run populate script

The populate script will create dummy data in the server DB and copy artwork images to either the AWS bucket or to a local folder. This script can be used as follows:

`python populate.py --url <server url>`

For more arguments, run ```python populate.py -h```