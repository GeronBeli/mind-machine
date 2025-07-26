import os
from dotenv import load_dotenv
from logger import LogLevels


load_dotenv()


min_log_level = LogLevels.info


root_directory = "./"

document_directory =  root_directory + "mm_docs/user/"

data_directory = root_directory + "data/"

log_directory = data_directory + "logs/"


database_url = os.getenv('DATABASE_URL')

file_extension = '.pdf'

ldap_server = os.getenv('LDAP_SERVER')
base_dn = os.getenv('BASE_DN')

qdrant_host = 'qdrant'
qdrant_port = 6333

date_time_format = '%d.%m.%Y'
units = ['B', 'KB', 'MB', 'GB', 'TB']

temp_pdf_directory = data_directory + 'temp_pdf/'

max_search_history_per_user = 50 
max_disk_space = 53687091200.0 
user_max_disk_space = 1073741824.0 
logout_timer = 60.0 