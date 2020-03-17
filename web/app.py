import mysql.connector
import locale
import sys
sys.path.append('../')
from database import sql
from flask import Flask, render_template, request


app = Flask(__name__)
def get_consult_values():
    # Connecting to db
    mysql = sql.SQL('root', '12qwaszx', 'db_python')

    # Getting list of teams
    command = "SELECT DISTINCT team_jogador FROM tb_jogador ORDER BY team_jogador;"
    cs = mysql.consultar(command)

    sel_team = "<SELECT CLASS = 'select-css' id='team'>"
    sel_team += "<OPTION>Todos</OPTION>"
    for [team] in cs:
        sel_team += f"<OPTION>{team}</OPTION>"
    sel_team += "</SELECT>"

    # Getting list of countries
    command = "SELECT DISTINCT cntr_jogador FROM tb_jogador ORDER BY cntr_jogador;"
    cs = mysql.consultar(command)

    sel_country = "<SELECT CLASS = 'select-css' id='country'>"
    sel_country += "<OPTION>Todos</OPTION>"
    for [country] in cs:
        sel_country += f"<OPTION>{country}</OPTION>"
    sel_country += "</SELECT>"

    return (sel_team, sel_country)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/fCreate')
def formCreate():
	return render_template('fCreate.html')

@app.route('/create', methods=['POST'])
def create():
    # Requesting values from create form
    name = request.form['name']
    team = request.form['team']
    country = request.form['country']

    # Acessing db and inserting values
    mysql = sql.SQL('root', '12qwaszx', 'db_python')
    comando = "INSERT INTO tb_jogador(name_jogador, team_jogador, cntr_jogador) VALUES (%s, %s, %s);"

    if mysql.executar(comando, [name, team, country]):
        msg="<div id = 'operation' value = 'incluir'></div>"
    else:
        msg="<div id = 'operation' value = 'falha'></div>"

    return render_template('result.html', msg=msg, op_from='create')

@app.route('/fRead')
def formConsultar():
    # Getting base values for consult form
    teams, countries = get_consult_values()
    return render_template('fRead.html', teams=teams, countries=countries)

@app.route('/read', methods=['POST'])
def consultar():
    # Pegando os dados de parâmetro vindos do formulário parConsultar()
    name = request.form['name']
    team = request.form['team']
    country = request.form['country']

    name = "a" if name == "undefined" else name

    # Recuperando jogadorss que satisfazem aos parâmetros de filtragem
    mysql = sql.SQL("root", "12qwaszx", "db_python")
    country_list = [name]

    command = "SELECT * FROM tb_jogador WHERE name_jogador LIKE CONCAT('%', %s, '%')"

    if team != "Todos":
        command += " AND team_jogador = %s"
        country_list.append(team)
    
    if country != "Todos":
        command += " AND cntr_jogador = %s"
        country_list.append(country)

    command += "ORDER BY name_jogador;"

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

    cs = mysql.consultar(command, country_list)
    players = "<table>" + \
        "<tr>" + \
        "<th>Nome</th>" + \
        "<th>Time</th>" + \
        "<th>País</th>" + \
        "</tr>"

    for [idt, name, team, country] in cs:
        players += "<TR CLASS = 'player-row'>"
        players += "<TD CLASS = 'consulta-result' >" + name + "</TD>"
        players += "<TD CLASS = 'consulta-result' >" + team + "</TD>"
        players += "<TD CLASS = 'consulta-result' >" + country + "</TD>"
        players += "</TR>"
    cs.close()

    players += "</table>"

    return render_template('ajax.html', AJAX=players)

@app.route('/index-read', methods=['POST'])
def indexRead():
    # Requesting data from form
    name = request.form['name']
    # Getting base values for consult form
    teams, countries = get_consult_values()

    return render_template('fRead.html', name_from_index = name, teams=teams, countries=countries)

@app.route('/sUpdate')
def parUpdate():
    return render_template('sUpdate.html')

@app.route('/fUpdate', methods=['POST'])
def formUpdate():
    # Pegando os dados de parâmetro vindos do formulário parConsultar()
    name = request.form['name']

    # Recuperando modelos que satisfazem aos parâmetros de filtragem
    mysql = sql.SQL("root", "12qwaszx", "db_python")
    command = "SELECT * FROM tb_jogador WHERE name_jogador=%s;"

    cs = mysql.consultar(command, [name])
    data = cs.fetchone()
    cs.close()

    if data == None:
        ajx = "<div class='input-area'>" + \
              "<label for='name'>Nome</label>" + \
              "<input type='text' placeholder='(Ex: fiB0b)' id='name' name='name' size='50' maxlength='50' required />" + \
              "</div>" + \
              "<input type='submit' class = 'button' value='Alterar' onclick='exec()'/>" + \
              "<div class='error-area'>" + \
              "<p>Não foi possível encontrar este jogador.</p>" + \
              "</div>" 
        return render_template('ajax.html', AJAX = ajx)
    else:
        ajx = "<form action='/update' method='post'>" + \
            "<div class='input-area'>" + \
            "<label for='name'>Nome</label>" + \
            "<input type='text' placeholder='(Ex: fiB0b)' id='name' name='name' size='50' maxlength='50' value="+data[1]+" required />" + \
            "</div>" + \
            "<div class='input-area'>" + \
            "<label for='name'>Nome</label>" + \
            "<input type='text' placeholder='(Ex: B4n4n4s In Pij4m4s)' id='team' name='team' size='50' maxlength='50' value="+data[2]+" required />" + \
            "</div>" + \
            "<div class='input-area'>" + \
            "<label for='name'>Nome</label>" + \
            "<input type='text' placeholder='(Ex: Brasil)' id='country' name='country' size='50' maxlength='50' value="+data[3]+" required />" + \
            "</div>" + \
            "<input type='hidden' name='idt' value= "+str(data[0])+" />" + \
            "<input class = 'button' type='submit' value='Alterar jogador'/>" + \
            "</form>"
        return render_template('ajax.html', AJAX = ajx)

@app.route('/update', methods=['POST'])
def alterar():
   # Recuperando dados do formulário de formAlterar()
   idt = int(request.form['idt'])
   name = request.form['name']
   team = request.form['team']
   country = request.form['country']

   # Alterando dados no SGBD
   mysql = sql.SQL("root", "12qwaszx", "db_python")
   command = "UPDATE tb_jogador SET name_jogador=%s, team_jogador=%s, cntr_jogador = %s WHERE idt_jogador=%s;"

   if mysql.executar(command, [name, team, country, idt]):
       msg="<div id = 'operation' value = 'alterar'></div>"
   else:
       msg = "<div id = 'operation' value = 'falha'></div>"

   return render_template('result.html', msg=msg, op_from='update')
   
@app.route('/result', methods=['POST'])
def getResult():

    operation = request.form['op']
    ajx = ""
    
    if operation == "falha":
        ajx = "<h1 class = 'title'>Falha ao completar operação</h1>" + \
        "<h2 class = 'result-msg'>Não foi possível completar a operação</h2>" 

    elif operation == "incluir":
        ajx = "<h1 class = 'title'>Resultado da inclusão de jogador</h1>" + \
        "<h2 class = 'result-msg'>Jogador inserido com sucesso</h2>" + \
        "<div class='button-area'>" + \
        "<a class = 'button' href='/fCreate'> Incluir outro jogador </a>" + \
        "</div>"

    elif operation == "alterar":
        ajx = "<h1 class = 'title'>Resultado da alteração de jogador</h1>" + \
        "<h2 class = 'result-msg'>Jogador alterado com sucesso</h2>" + \
        "<div class='button-area'>" + \
        "<a class = 'button' href='/sUpdate'> Alterar outro jogador </a>" + \
        "</div>"

    elif operation == "excluir":
        ajx = "<h1 class = 'title'>Resultado da exclusão de jogador</h1>" + \
        "<h2 class = 'result-msg'>Jogador excluído com sucesso</h2>" + \
        "<div class='button-area'>" + \
        "<a class = 'button' href='/sExcluir'> Excluir outro jogador </a>" + \
        "</div>"   

    return render_template('ajax.html', AJAX=ajx)

@app.route('/sExcluir')
def parExcluir():
   # Recuperando todos os modelos da base de dados
   mysql = sql.SQL("root", "12qwaszx", "db_python")
   comando = "SELECT idt_jogador, name_jogador, team_jogador, cntr_jogador FROM tb_jogador ORDER BY team_jogador;"

   cs = mysql.consultar(comando, ())
   players = ""
   for [idt, nome, time, pais] in cs:
       players += "<TR>"
       players += "<TD CLASS = 'item-excluir'>" + nome + " (" + time + ")" + "</TD>"
       players += "<TD CLASS = 'item-excluir'>" + pais + "</TD>"
       players += "<TD><BUTTON CLASS = 'button-excluir' ONCLICK=\"jsExcluir('" + nome + " (" + time + ")" + "', " + str(idt) + ")\">Excluir" + "</BUTTON></TD>"
       players += "</TR>"
   cs.close()

   return render_template('sExcluir.html', players = players )



@app.route('/excluir', methods=['POST'])
def excluir():
    # Recuperando dados do formulário de parExcluir()
    idt = int(request.form['idt'])

    # Alterando dados no SGBD
    mysql = sql.SQL("root", "12qwaszx", "db_python")
    comando = "DELETE FROM tb_jogador WHERE idt_jogador=%s;"

    if mysql.executar(comando, [idt]):
        msg="<div id = 'operation' value = 'excluir'></div>"
    else:
        msg = "<div id = 'operation' value = 'falha'></div>"

    return render_template('result.html', msg=msg, op_from='delete')

