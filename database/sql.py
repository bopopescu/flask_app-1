import mysql.connector


class SQL:
	def __init__(self, usuario, senha, esquema):
		self.cnx = mysql.connector.connect(user=usuario, password=senha, host='127.0.0.1', database=esquema)

	def executar(self, comando, parametros = []):
		try:
			cursor = self.cnx.cursor()
			cursor.execute(comando, parametros)
			self.cnx.commit()
			cursor.close()
			return True

		except Exception as e:
			print(e)
			return False



	def consultar(self, comando, parametros = []):
		cursor = self.cnx.cursor()
		cursor.execute(comando, parametros)
		return cursor

	def __del__(self):
		self.cnx.close()
