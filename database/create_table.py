from sql import SQL
from json import load

user, password, schema = ('', '', '')
with open('./../config.json') as json_file:
    data = load(json_file)
    user = data['user']
    password = data['password']
    schema = data['schema']

mysql = SQL(user, password, schema)

comando = "DROP TABLE IF EXISTS tb_jogador;"

if mysql.executar(comando):
	print ("Tabela de Jogadores excluída com sucesso!")


comando = "CREATE TABLE tb_jogador (" + \
		"idt_jogador INT AUTO_INCREMENT PRIMARY KEY," + \
		"name_jogador VARCHAR(50) NOT NULL, " + \
		"team_jogador VARCHAr(50) NOT NULL, " + \
		"cntr_jogador VARCHAR(50) NOT NULL); "

if mysql.executar(comando):
	print ("Tabela de jogadores criada com sucesso!")


comando = "INSERT INTO tb_jogador(name_jogador, team_jogador, cntr_jogador) VALUES " + \
         "('ScreaM', 'G2 Esports', 'Bélgica'), " + \
		 "('SmithZz', 'G2 Esports', 'França'), " + \
		 "('shox', 'G2 Esports', 'França'), " + \
		 "('Ex6TenZ', 'G2 Esports', 'Bélgica'), " + \
		 "('RpK', 'G2 Esports', 'França'), " + \
         "('GuardiaN', 'Natus Vincere', 'Eslováquia'), " + \
         "('Zeus', 'Natus Vincere', 'Ucrânia'), " + \
         "('seized', 'Natus Vincere', 'Rússia'), " + \
         "('flamie', 'Natus Vincere', 'Rússia'), " + \
         "('Edward', 'Natus Vincere', 'Ucrânia'), " + \
		 "('fnx', 'Luminosity', 'Brasil'), " + \
		 "('fer', 'Luminosity', 'Brasil'), " + \
		 "('FalleN', 'Luminosity', 'Brasil'), " + \
		 "('coldzera', 'Luminosity', 'Brasil'), " + \
		 "('TACO', 'Luminosity', 'Brasil'), " + \
		 "('DEVIL', 'EnVyUs', 'França'), " + \
		 "('NBK', 'EnVyUs', 'França'), " + \
		 "('Happy', 'EnVyUs', 'França'), " + \
		 "('apEX', 'EnVyUs', 'França'), " + \
		 "('kennyS', 'EnVyUs', 'França'), " + \
		 "('ShahZaM', 'Conquest', 'Estados Unidos'), " + \
		 "('daps', 'Conquest', 'Canadá'), " + \
		 "('RUSH', 'Conquest', 'Estados Unidos'), " + \
		 "('NAF', 'Conquest', 'Canadá'), " + \
		 "('stanislaw', 'Conquest', 'Canadá'), " + \
		 "('Skadoodle', 'Cloud9', 'Estados Unidos'), " + \
         "('n0thing', 'Cloud9', 'Estados Unidos'), " + \
         "('shroud', 'Cloud9', 'Canadá'), " + \
         "('freakazoid', 'Cloud9', 'Estados Unidos'), " + \
         "('Stewie2k', 'Cloud9', 'Estados Unidos');"

if mysql.executar(comando):
   print("Jogadores cadastrados com sucesso!")