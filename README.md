
# Flask Web APP - CRUD Jogadores de CS:GO

Projeto para criação de uma página web com integração ao MySQL.

  

# Requerimentos:

* MySQL==8.0 CE

* Python==3.8.1

  

# Dependências Python:
```
pip install Flask, mysql-connector-python
```

# Configuration
* Altere os valores no arquivo `config.json` para corresponder ao seu banco de dados SQL.
* Defina as variáveis de configuração com os comandos CLI na pasta web:
	```
	cd ./web
	set FLASK_ENV=develpoment
	set FLASK_DEBUG=1
	set FLASK_APP=app.py
	```
# Execução
Após configurar o projeto, rode estes comandos: 
	
```
cd ./web
flask run
```

OBS: Existe um script para inserção automática de alguns valores no banco para executá-los basta:
```
cd ./database
python create_table.py
```
	