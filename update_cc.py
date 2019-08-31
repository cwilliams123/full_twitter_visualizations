import sqlite3 as db
import json
import datetime
import pandas as pd
from twython import Twython
import numpy as np
import time
import update_functions

consumer_key = 'f0RtjQ2jcq9ZNw1jOprB3EVeC'
consumer_secret = '5YjR83H05slPnaDVl1KNafonWU36ewtQAb2JNMOpLZeMJipSn4'
access_token = '1136378599227953152-Xqn4sl2Fa7X4ycvP5pFUlTte7iT1v2'
access_secret = 'UdRdEBiUxgpCa2fJibcA1S5uzz4NxJRC4Di5cc9uaMyuv'

database = "all_data"

big_table = "cc"

data_table = "cc_with_updates"

update_functions.append_new_data(consumer_key, consumer_secret, access_token, access_secret, database, big_table, data_table)

