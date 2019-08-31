import sqlite3 as db
import json
import datetime
import pandas as pd
from twython import Twython
import numpy as np
import time
import update_functions

consumer_key = 'TpFFRQhpLU6xB8Ju48XVprWMg'
consumer_secret = 'KMi4t6ciEISo23rxJxltJ4bvt6MdQg1sipCt2TnnOluGN295qq'
access_token= '1135946096449138689-RNoNCILwV70CGX0aHBWTDXoshkCIqH'
access_secret= 'WIckI9PXgskqN1H8gW3B1QgFZAqG8bYGqDHN4gOHPzMo1'

database = "all_data"

big_table = "ccr"

data_table = "ccr_with_updates"

update_functions.append_new_data(consumer_key, consumer_secret, access_token, access_secret, database, big_table, data_table)
