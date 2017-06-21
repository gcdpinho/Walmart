# -*- coding: UTF-8 -*-
import csv
import datetime
import sys

# Lê os dados de um arquivo csv e coloca em uma lista
def readCsvFile(fileName):
	data = []

	with open("Files/"+fileName, "r") as csvFile:
		reader = csv.reader(csvFile, delimiter =',', quotechar = '\"')

		for row in reader:
			num = [x for x in row]
			data.append(num)

	return data

# Escreve em um arquivo csv uma lista de dados
def writeCsvFile(fileName, data):
	with open("Files/"+fileName, 'wb') as csvFile:
		writer = csv.writer(csvFile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
		writer.writerows(data)

# Lê os dados (por linha) de um arquivo e retorna uma lista com os dados
def openTxtFile(fileName):
	openFile = open(fileName, "r")
	newData = openFile.readlines()
	openFile.close()

	return newData

# Adiciona ao arquivo de texto já existente, uma nova linha
def writeTxtFile(fileName, data):
	newData = openTxtFile("Files/"+fileName)
	newData.append(data)
	
	openFile = open("Files/"+fileName, "w")
	openFile.writelines(newData)
	openFile.close()

# Imprime as informações existente no arquivo txt de log
def showLog(fileName):
	openFile = openTxtFile("Files/"+fileName)

	for element in openFile:
		print element

# Cadastra n (parâmetro) usuários informados (REMEDY)
def users():
	entry = raw_input(encodeWin("Número de usuários:", "list"))
	users = []
	for i in xrange(int(entry)):
		user = []
		cad = "s"
		while cad == "s":	
			entry = raw_input("Classe:")
			temp = raw_input(encodeWin("Informação:", "list"))

			if entry.lower() == "cpf":
				temp = temp.replace(".", "")
				temp = temp.replace("-", "")
			entry = entry + ":" + temp
			user.append(entry)
			cad = raw_input("Cadastrar outro atributo?(s/n)")
		users.append(user)
	
	return users

# Adiciona tarefas no arquivo, oriundas do REMEDY
def add(data, date):
	newLine = []
	newLine.append(date.strftime("%d-%m-%Y %H:%M"))
	
	entry = raw_input("Nome da Tarefa:")
	while verifyTasks(encodeWin(newEntry(entry), "add"), data) == True:
		entry = raw_input(encodeWin("Já existe tarefa com esse nome. Informe outro nome de Tarefa:", "list"))
	temp = newEntry(entry)
	while temp == "false":
		temp = raw_input(encodeWin("Nome de Tarefa inválido:", "list"))
		temp = newEntry(temp)
	entry = temp
	newLine.append(encodeWin(entry, "add"))
	entry = raw_input("Summary:")	
	if entry[-1::] != "." and entry[-1::] != "?" and entry[-1::] != "!" and entry != "":
		entry += "."
	newLine.append(encodeWin(entry.replace("\enter", "\n"), "add"))
	print "Remedy:"
	temp = users()
	tempAux = ""
	if len(temp) > 0:
		tempAux = "["
	for row in temp:
		tempAux += "["
		for element in row:
			tempAux += element + ","
		tempAux = tempAux[:-1] + "]+"
	if len(temp) > 0:
		tempAux = tempAux[:-1] + "]"

	newLine.append(encodeWin(tempAux, "add"))
	entry = raw_input("Helpdesk Voiza:")
	if entry[-1::] != "." and entry[-1::] != "?" and entry[-1::] != "!" and entry != "":
		entry += "."
	entry = entry.replace("\includeResetSenha", includeScript("resetSenha.txt"))
	entry = entry.replace("\includeSolicitarAcesso", includeScript("solicitarAcesso.txt"))
	newLine.append(encodeWin(entry.replace("\enter", "\n"), "add"))

	data.append(newLine)
	writeCsvFile("tasks.csv", data)

# Adiciona tarefas com scopo livre
def addFree(data, date):
	newLine = []
	newLine.append(date.strftime("%d-%m-%Y %H:%M"))
	
	entry = raw_input("Nome da Tarefa:")
	while verifyTasks(encodeWin(entry, "add"), data) == True:
		entry = raw_input("Ja existe tarefa com esse nome. Informe outro nome de Tarefa:")
	newLine.append(encodeWin(entry, "add"))
	entry = raw_input("Informe o campo da mensagem:")
	if entry[-1::] != "." and entry[-1::] != "!" and entry[-1::] != "?" and entry != "":
		entry += "."	
	entry = entry.replace("\includeResetSenha", includeScript("resetSenha.txt"))
	newLine.append(encodeWin(entry.replace("\enter", "\n"), "add"))
	
	data.append(newLine)
	writeCsvFile("tasks.csv", data)

# Imprime todas as tarefas presentes no arquivo csv
def list(data):
	c = 0
	
	for row in data:
		hour = row[0].split(":")[0].split(" ")[1]
		if len(row) > 3:
			index = 5
			print "-----------" + str(c+1) + "-----------\n"
			print "Data:" + row[0] + "\n"
			print "Nome da Tarefa:" + encodeWin(row[1], "list") + "\n"
			if "Email" in row[1]:
				print "--Email--\n"+ encodeWin(row[2], "list") + "\n"
			else:	
				print "--Summary--\n"+ encodeWin(row[2], "list") + "\n"
				print "--Remedy--"
			temp0 = row[3].split("+")
			for e in temp0:
				temp = e.split(",")
				for element in temp:
					element = element.replace("[", "")
					element = element.replace("\'", "")
					element = element.replace("]", "")
					if "CPF" in element or "cpf" in element:
						temp = element.split(":")
						print encodeWin(temp[0]+ ":" + maskCPF(temp[1]), "list")
					else:
						print encodeWin(element, "list")
						
			print "\n--Helpdesk Voiza--" 
			if (int(hour) < 13):
				print "Bom dia time,\n"
			else:
				print "Boa tarde time, \n"
			print encodeWin(row[4], "list") + "\n\nAtenciosamente."
			while len(row) > index:
				if isDate(row[index]) == True:
					print "\nData:"+ row[index] + "\n"
					index += 1
				print "\n--Resposta--"
				print encodeWin(row[index], "list")
				index += 1
				print "\n--Helpdesk Voiza--"
				if (int(hour) < 13):
					print "Bom dia time,\n"
				else:
					print "Boa tarde time, \n"
				print encodeWin(row[index], "list") + "\n\nAtenciosamente."
				index+=1
		else:
			print "-----------" + str(c+1) + "-----------\n"
			print "Data:" + row[0] + "\n"
			print "Nome da Tarefa:" + encodeWin(row[1], "list") + "\n"
			print "--Mensagem--\n" + encodeWin(row[2], "list") + "\n"
		c += 1

	if len(data) == 0:
		print "Nenhuma tarefa encontrada."

# Remove uma tarefa do arquivo (por nome ou por índice)
def remove(data, time):
	count = 0
	entry = raw_input("Informe o nome da tarefa que deseja remover:")
	entry = entry.lower()
	entry = encodeWin(entry, "add")
	c = 0
	for row in data:
		if row[1].lower() == entry:
			del data[c]
			count += 1
		c += 1	

	if count > 0:
		writeCsvFile("tasks.csv", data)
		print "\n" + str(count) +" tarefas foram removidas com sucesso."

		removeTime(time, entry)

# Busca uma tarefa por nome ou todas as tarefas por data
def find(data):
	temp = []
	entry = raw_input("Informe o nome da tarefa:")
	if entry == "date":
		entry = raw_input("Informe a data(dd-mm-yyyy):")
		while (validateData(entry) == False):
			entry = raw_input("Informe uma data valida (dd-mm-yyyy):")
		for row in data:
			if row[0].split(" ")[0] == entry:
				temp.append(row)	
	else:
		entry = entry.lower()
		entry = encodeWin(entry, "add")
		for row in data:
			if entry in row[1].lower():
				temp.append(row)
	
	list(temp)
	print "\nForam encontrados "+str(len(temp))+ " resultados."

# Acrescenta a resposta do cliente + o Helpdesk Voiza a uma tarefa
def edit(data, date, time):
	entry = raw_input("Informe o nome da tarefa:")
	entry = entry.lower()
	entry = encodeWin(entry, "add")
	flag = False
	for row in data:
		if row[1].lower() == entry:
			flag = True
			task = entry
			row.append(date.strftime("%d-%m-%Y %H:%M"))
			entry = raw_input("Resposta:")
			if entry[-1::] != "." and entry[-1::] != "!" and entry[-1::] != "?" and entry != "":
				entry += "."
			row.append(encodeWin(entry.replace("\enter", "\n"), "add"))
			entry = raw_input("Helpdesk Voiza:")
			if entry[-1::] != "." and entry[-1::] != "!" and entry[-1::] != "?" and entry != "":
				entry += "."
			entry = entry.replace("\includeResetSenha", includeScript("resetSenha.txt"))
			entry = entry.replace("\includeSolicitarAcesso", includeScript("solicitarAcesso.txt"))
			row.append(encodeWin(entry.replace("\enter", "\n"), "add"))
			break;
	
	if flag == True:
		writeCsvFile("tasks.csv", data)
		addTimeEdit(date, task.upper(), time)
	else:
		print "\nNenhuma tarefa encontrada."

# Permite a edição do campo mensagem (helpdesk) da tarefa e lista as tarefas com campo vazio
def editAnswer(data):
	entry = raw_input("Informe o nome da tarefa:")
	entry = entry.lower()
	entry = encodeWin(entry, "add")
	flag = False
	if entry == "":
		print "Tarefas que possuem o campo mensagem vazio:\n"
		temp = []
		index = []
		j = 0
		for row in data:
			if len(row) > 3 and row[4] == "":
				print encodeWin(row[1], "list")
				temp.append(row[1])
				index.append(j)
			j += 1
		if len(temp) > 0:
			entry = raw_input("\nDigite o nome da tarefa para alterar seu campo mensagem:")
			entry = encodeWin(entry, "add")
			j = 0
			for element in temp:
				if element.lower() == entry.lower():
					flag = True
					entry = raw_input("Digite o campo mensagem:")
					if entry[-1::] != "." and entry[-1::] != "!" and entry[-1::] != "?" and entry != "":
						entry += "."
					entry = entry.replace("\includeResetSenha", includeScript("resetSenha.txt"))
					entry = entry.replace("\includeSolicitarAcesso", includeScript("solicitarAcesso.txt"))
					data[index[j]][4] = encodeWin(entry.replace("\enter", "\n"), "add")
				j += 1
	else:
		for row in data:
			if row[1].lower() == entry:
				if row[4] == "":
					flag = True
					entry = raw_input("Digite o campo mensagem:")
					if entry[-1::] != "." and entry[-1::] != "!" and entry[-1::] != "?" and entry != "":
						entry += "."
					entry = entry.replace("\includeResetSenha", includeScript("resetSenha.txt"))
					entry = entry.replace("\includeSolicitarAcesso", includeScript("solicitarAcesso.txt"))
					row[4] = encodeWin(entry.replace("\enter", "\n"), "add")
	if flag == True:
		writeCsvFile("tasks.csv", data)
	else:
		print "\nNenhuma tarefa encontrada."

# Aloca uma quantidade de horas para uma tarefa
def timeAdd(time, data):
	temp = []
	flag = False
	entry = raw_input("Informe a data (dd-mm-yyyy):")
	while (validateData(entry) == False):
			entry = raw_input("Informe uma data valida (dd-mm-yyyy):")
	temp.append(entry)
	entry = raw_input("Informe o nome da tarefa:")
	entry = encodeWin(entry, "add")
	while flag == False:
		for row in data:
			if entry.lower() == row[1].lower() or entry == "exit":
				flag = True
				break
		if flag == False:
			entry = raw_input("Informe um nome de tarefa correto:")
			entry = encodeWin(entry, "add")
	if entry != "exit":
		temp.append(entry)
		entry = raw_input("Informe a quantidade de horas:")
		temp.append(entry)

		time.append(temp)

		writeCsvFile("timeTasks.csv", time)

# Valida se o formato da data está correto
def validateData(date):
	temp = date.split("-")
	if len(temp[0]) == 2 and len(temp[1]) == 2 and len(temp[2]) == 4:
		return True

	return False

# Lista todas as horas alocadas
def listHours(data):
	for row in data:
		print "\nData:" + row[0]
		print "Tarefa:" + encodeWin(row[1], "list")
		print "Horas:" + row[2]

# Busca todas as horas alocadas em determinado dia ou busca todas as tarefas sem horas alocadas
def findTime(time, date, data):
	entry = raw_input("Informe a data (dd-mm-yyyy):")
	temp = []
	if entry == "free":
		for row in data:
			aux = []
			if contaisHours(row[1], time) == False:
				aux.append(row[0])
				aux.append(row[1])
				aux.append("0")
				temp.append(aux)
		
		for row in time:
			if row[2] == "0":
				temp.append(row)

		listHours(temp)
		if len(temp) > 0:
			print encodeWin("\nTarefas que nao possuem horas alocadas.", "list")
		else:
			print encodeWin("\nNão foram encontradas horas alocadas.", "list")
	elif entry == "date":
		hourDate = {}
		for row in time:
			temp = datetime.datetime.strptime(row[0], "%d-%m-%Y").date()
			if temp not in hourDate.keys():
				hourDate[temp] = float(row[2])
			else:
				hourDate[temp] += float(row[2])
			
		hourDate = sorted(hourDate.items())
		
		for d,v in hourDate:
			if v > 0:
				print str(d.strftime("%d-%m-%Y")) + ": " + str(v)
	else:
		if entry == "":
			entry = date.strftime("%d-%m-%Y")
		while validateData(entry) == False and entry != "free" and entry != "":
				entry = raw_input("Informe uma data valida (dd-mm-yyyy):")
		if entry == "free":
			for row in data:
				aux = []
				if contaisHours(row[1], time) == False:
					aux.append(row[0])
					aux.append(row[1])
					aux.append("0")
					temp.append(aux)
			
			for row in time:
				if row[2] == "0":
					temp.append(row)

			listHours(temp)
			if len(temp) > 0:
				print encodeWin("\nTarefas que nao possuem horas alocadas.", "list")
			else:
				print encodeWin("\nNão foram encontradas horas alocadas.", "list")
		else:
			if entry == "":
				entry = date.strftime("%d-%m-%Y")
			s = 0.0
			for row in time:
				if entry == row[0] and row[2] != "0":
					temp.append(row)
					s += float(row[2])

			listHours(temp)
			if s > 0.0:
				print "\nForam encontradas " + str(s) + " horas alocadas."
			else:
				print encodeWin("\nNão foram encontradas horas alocadas.", "list")

# Edita uma alocação de hora (data ou tempo)
def editTime(time):
	entry = raw_input("Informe o nome da tarefa que deseja editar:")
	entry = encodeWin(entry.lower(), "add")
	matchs = []

	for i in xrange(len(time)):
		if entry == time[i][1].lower():
			matchs.append(i)

	if len(matchs) == 1:
		entry = raw_input("Infome a nova data:")
		if entry != "":
			if validateData(entry) == True:
				time[matchs[0]][0] = entry
		entry = raw_input("Informe a nova quantidade de horas:")
		if entry != "":
			time[matchs[0]][2] = entry
	elif len(matchs) > 1:
		print "Tarefa: " + encodeWin(time[matchs[0]][1], "list")
		index = 0
		for element in matchs:
			print str(index) + ": Data: " + time[element][0]
			if index <= 9:
				print "   Horas: " + time[element][2]
			else:
				print "    Horas: " + time[element][2]
			index += 1
		entry = raw_input(encodeWin("Informe qual alocação deseja editar (index):", "list"))
		while int(entry) < 0 or int(entry) >= len(matchs):
			entry = raw_input(encodeWin("Informe uma alocação válida (index):"), "list")
		temp = int(entry)
		entry = raw_input("Infome a nova data:")
		if entry != "":
			if validateData(entry) == True:
				time[matchs[temp]][0] = entry
		entry = raw_input("Informe a nova quantidade de horas:")
		if entry != "":
			time[matchs[temp]][2] = entry
		
	writeCsvFile("timeTasks.csv", time)

# Remove uma alocação de hora (pesquisa por data)
def removeTime(time, task):
	if task == None:		
		entry = raw_input("Informe o nome da tarefa que deseja remover:")
	else:
		entry = task
	entry = entry.lower()
	entry = encodeWin(entry, "add")
	temp = []
	tempC = []
	c = 0
	for row in time:
		if entry == row[1].lower():
			temp.append(row)
			tempC.append(c)
		c += 1
	if len(temp) > 0:
		if task == None:
			if len(temp) == 1:
				del time[tempC[0]]
				print encodeWin("\nAlocação deletada com sucesso.", "list")
			else:
				print "Tarefa: " + encodeWin(temp[0][1], "list")
				index = 0
				for element in temp:
					print str(index) + ": Data: " + element[0]
					if index <= 9:
						print "   Horas: " + element[2]
					else:
						print "    Horas: " + element[2]
					index += 1
				entry = raw_input("\nInforme qual das horas alocadas deseja remover:")
				while int(entry) < 0 or int(entry) >= len(temp):
					entry = raw_input(encodeWin("Informe um índice válido:", "list"))
				del time[tempC[int(entry)]]
				print encodeWin("\nAlocação deletada com sucesso.", "list")
			writeCsvFile("timeTasks.csv", time)
		else:
			for element in tempC:
				del time[element]
			writeCsvFile("timeTasks.csv", time)
			if len(tempC) > 1:
				print encodeWin("\n"+str(len(tempC))+" alocações excluídas.", "list")
			else:
				print encodeWin("\n"+str(len(tempC))+" alocação excluída.", "list")
	else:
		print encodeWin("Nenhuma alocação encontrada.", "list")


# Verifica se existe alocação de horas para determinada tarefa
def contaisHours(element, time):
	
	for row in time:
		if element.lower() == row[1].lower():
			return True

	return False

# Verifica se existe uma tarefa com o mesmo nome
def verifyTasks(name, data):
	for row in data:
		if name.lower() == row[1].lower():
			return True
	
	return False

# Codifica a string para poder armazenar no arquivo em utf-8 e mostrar no terminal em cp850
def encodeWin(string, op):
	if op == "add":
		return string.decode("cp850").encode("utf8")
	elif op == "list":	
		return string.decode("utf8").encode("cp850")

# Inclui no texto o conteúdo do arquivo
def includeScript(fileName):
	data = openTxtFile("Scripts/"+fileName)
	string = ""
	for row in data:
		string += row
	
	return string.decode('utf-8-sig').encode('cp850')

# Verifica se a string é uma data (DD-MM-YYYY HH:MM)
def isDate(date):
	temp = date.split("-")
	if len(temp) == 3:
		temp = temp[2].split(" ")
		if len(temp) == 2:
			temp = temp[1].split(":")
			if len(temp) == 2:
				return True
	
	return False

# Permite que a tarefa não precise do INC0000
def newEntry(entry):
	if entry[0] == "I" and entry[1] == "N" and entry[2] == "C" and entry[3] == "0" and entry[4] == "0" and entry[5] == "0":
		if len(entry) == 15:
			return entry
		else:
			return "false"
	else:
		if len(entry) == 8:
			try:
				int(entry)
				return "INC0000" + entry
			except ValueError:
				return entry

	return entry

# Retorna o cpf com a máscara de pontuação 000.000.000-00
def maskCPF(cpf):
	cpf = cpf.replace(".", "")
	cpf = cpf.replace("-", "")
	return cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]


def addTimeEdit(date, task, time):
	aux = []
	aux.append(date.strftime("%d-%m-%Y"))
	aux.append(task)
	aux.append(0)
	time.append(aux)

	writeCsvFile("timeTasks.csv", time)


# Imprime as ações disponíveis no programa
def help():
	print encodeWin("Você pode realizar as seguintes ações:", "list")
	print "\nTarefas:"
	print "\t- add: para adicionar uma tarefa;"
	print encodeWin("\t- add free: para adicionar uma tarefa livre de máscaras (título e mensagem);", "list")
	print "\t- find: para procurar uma tarefa por nome ou data;"
	print "\t- remove: para remover uma tarefa por nome ou indice;"
	print "\t- edit: para editar uma tarefa (reposta + helpdesk);"
	print "\t- edit answer: para editar a resposta helpdesk (usualmente usada para editar respostas vazias);"
	print "\t- list: para listar todas as tarefas cadastradas."
	print "Time:"
	print "\t- time add: para alocar horas em uma tarefa;"
	print "\t- time find: para procurar horas de determinada tarefa, tarefas sem horas (free) ou tarefas pode date (date);"
	print "\t- time remove: para remover as horas de uma tarefa;"
	print "\t- time edit: para editar a data ou as horas de uma tarefa;"
	print "\t- time list: para listar todas as horas alocadas."

	print encodeWin("\n- show log: mostra todas as ações realizadas;", "list")
	print "- --developer: dicas para o desenvolvedor do sistema;"
	print encodeWin("- função toDo no código é referente ao que precisa ser feito no sistema;", "list")
	print "- exit: sai do programa."

# Dicas para o desenvolvendor do sistema
def developer():
	print encodeWin("- Se utilizar o bash, digitar 3 como parâmetro (sys); --desativado", "list")
	print encodeWin("- Configuração atual do cmd chcp 850 (encodeWin);", "list")
	print encodeWin("- Comando time find > free: quando é listado uma tarefa sem horário, tem que editar aquela alocação (0);", "list")
	print "- Decode + Encode para salvar em utf8 e printar no terminal em cp850;"
	print encodeWin("- Codificação para scripts em txt UTF8: utf-8-sig;", "list")
	print encodeWin("- Funiconalidades dos sistema que precisam pesquisar nome de tarefa estão utilizando o parâmetro IN (contém);", "list")
	print encodeWin("- Mais de 99 alocacoes para a mesma tarefa (quase impossível) verificar espaçamento no edit time;", "list")
	print encodeWin("- Comando remove: limpa todas as alocações com da tarefa (timeTask)", "list")
	print encodeWin("- Comando edit: adiciona uma alocação de hora para o dia atual de valor 0 ", "list")

# O que precisa ser feito no sistema
def toDo():
	print "Script para fazer backup dos arquivos diariamente."
	#print "100%."

# Função main: trata as ações digitadas
def main(entry):

	data = readCsvFile("tasks.csv")
	time = readCsvFile("timeTasks.csv")

	date = datetime.datetime.now()

	if entry == "add":
		data = add(data, date)
	elif entry == "list":
		data = list(data)
	elif entry == "remove":
		data = remove(data, time)
	#elif entry == "clean":
	#	writeCsvFile("tasks.csv", "")
	elif entry == "show log":
		showLog("logTasks.txt")
	elif entry == "find":
		find(data)
	elif entry == "edit":
		edit(data, date, time)
	elif entry == "time add":
		timeAdd(time, data)
	elif entry == "time list":
		try:
			listHours(time)
		except IndexError:
			print encodeWin("Não existe horas trabalhadas.", "list")
	elif entry == "time find":
		findTime(time, date, data)
	elif entry == "add free":
		addFree(data, date)
	elif entry == "time edit":
		editTime(time)
	elif entry == "time remove":
		removeTime(time, None)
	elif entry == "help":
		help()
	elif entry == "--developer":
		developer()
	elif entry == "edit answer":
		editAnswer(data)

	# Salva no log qual ação foi digitada (mesmo que não seja válida)
	temp = date.strftime("%d-%m-%Y %H:%M")
	writeTxtFile("logTasks.txt", temp + " - " + entry + "\n")

# Início do programa	
entry = raw_input(encodeWin("Digite uma ação:", "list"))

while (entry != "exit"):
	main(entry)
	entry = raw_input(encodeWin("\nDigite uma ação:", "list"))
