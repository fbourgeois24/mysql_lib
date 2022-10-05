import mysql.connector # Install with 'pip install mysql-connector-python'

""" Utilitaires pour gérer une db mariadb """
class mysql_database():
	def __init__(self, db_name=None, db_server=None, db_user="admin", db_password="", config=None):
		self.db = None
		self.cursor = None
		self.database = db_name
		self.host = db_server
		# self.port = db_port
		self.user = db_user
		self.password = db_password

		if config is not None:
			self.database = config.get("name")
			self.host = config.get("addr")
			# self.port = config.get("port")
			self.user = config.get("user")
			self.password = config.get("passwd")


	def connect(self):
		""" Connexion à la DB """
		self.db = mysql.connector.connect(host = self.host, database = self.database, user = self.user, password = self.password)
		if self.db is None:
			return False
		else:
			return True

	def disconnect(self):
		""" Méthode pour déconnecter la db """
		self.db.close()

	def open(self):
		""" Méthode pour créer un curseur """
		# On essaye de fermer le curseur avant d'en recréer un 
		self.connect()
		try:
			self.cursor.close()
		except:
			pass
		self.cursor = self.db.cursor()
		if self.cursor is not None:
			return True
		else:
			return False

	def close(self, commit = False):
		""" Méthode pour détruire le curseur, avec ou sans commit """
		if commit:
			self.db.commit()
		self.cursor.close()
		self.disconnect()

	def commit(self):
		""" Méthode qui met à jour la db """
		self.db.commit()
		
	def exec(self, query, params = None, fetch = "all", autoconnect = True):
		""" Méthode pour exécuter une requête et qui ouvre et ferme  la db automatiquement """
		# Détermination du renvoi d'info ou non
		if not "SELECT" in query[:20]:
			commit = True
		else:
			commit = False
		if autoconnect:
			self.connect()
		if self.open():
			self.cursor.execute(query, params)
			# Si pas de commit ce sera une récupération
			if not commit or "RETURNING" in query:	
				if fetch == "all":
					value = self.fetchall()
				elif fetch == "one":
					value = self.fetchone()
					# On vide le curseur pour éviter l'erreur de data restantes à la fermeture
					trash = self.fetchall()
				elif fetch == "single":
					# On essaie de prendre le premier mais si ça échoue c'est probablement que la requête n'a rien retourné
					value = self.fetchone()
					if value is not None:
						value = value[0]
				elif fetch == 'list':
					# On renvoie une liste composée du premier élément de chaque ligne
					value = [item[0] for item in self.fetchall()]
				else:
					raise ValueError("Wrong fetch type")
				self.close()
				if autoconnect:
					self.disconnect()
				return value
			else:
				self.close(commit=commit)
				if autoconnect:
					self.disconnect()
		else:
			raise AttributeError("Erreur de création du curseur pour l'accès à la db")

	def fetchall(self):
		""" Méthode pour le fetchall """
		return self.cursor.fetchall()


	def fetchone(self):
		""" Méthode pour le fetchone """
		return self.cursor.fetchone()

	def __enter__(self):
		""" Ouverture avec with """
		self.connect()
		return self

	def __exit__(self, *args, **kwargs):
		""" Fermeture avec with """
		self.disconnect()

# # Test
# if __name__ == "__main__":
# 	db = mariadb_database("aqua_py", "192.168.10.22", db_user="admin", db_password="admin")
# 	db.connect()
# 	result = db.exec(''' SELECT * FROM channels ''', fetch='single')
# 	print(result)
# 	db.disconnect()
