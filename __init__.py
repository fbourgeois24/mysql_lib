import os

try:
	# On importe tout
	from mysql_lib.mysql_lib import mysql_database
except ModuleNotFoundError:
	# Si module non trouvé, on installe les dépendances
	os.popen(f"pip install --no-cache-dir -r {os.path.dirname(os.path.realpath(__file__))}/requirements.txt").read()
	from mysql_lib.mysql_lib import mysql_database

