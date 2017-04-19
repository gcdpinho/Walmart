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

# Adiciona ao arquivo de texto já existente, uma nova linha
def writeTxtFile(fileName, data):
	openFile = open("Files/"+fileName, "r")
	newData = openFile.readlines()
	newData.append(data)
	
	openFile = open("Files/"+fileName, "w")
	openFile.writelines(newData)
	openFile.close()

# Imprime as informações existente no arquivo txt de log
def showLog(fileName):
	openFile = open("Files/"+fileName, "r")
	data = openFile.readlines()
	for element in data:
		print element
	openFile.close()

# Cadastra n (parâmetro) usuários informados (REMEDY)
def users():
	entry = raw_input("Numero de usuarios:")
	users = []
	for i in xrange(int(entry)):
		user = []
		cad = "s"
		while cad == "s":	
			entry = raw_input("Classe:")
			entry = entry + ":" +raw_input("Informacao:")
			user.append(entry)
			cad = raw_input("Cadastrar outro atributo?(s/n)")
		users.append(user)
	return users

# Adiciona tarefas no arquivo, oriundas do REMEDY
def add(data, date, fuso):
	newLine = []
	temp = date.strftime("%d-%m-%Y")
	if date.hour > 9:
		hour = str(date.hour-int(fuso))
	else:
		hour = "0" + str(date.hour-int(fuso))
	if date.minute > 9:
		minute = str(date.minute)
	else:
		minute = "0" + str(date.minute)
	temp+= " " + hour + ":" + minute
	newLine.append(temp)
	
	entry = raw_input("Nome da Tarefa:")
	while verifyTasks(entry, data) == True:
		entry = raw_input("Ja existe tarefa com esse nome. Informe outro nome de Tarefa:")
	newLine.append(encodeWin(entry, "add"))
	entry = raw_input("Summary:")	
	newLine.append(encodeWin(entry.replace("\enter", "\n"), "add"))
	print "Remedy:"
	newLine.append(users())
	entry = raw_input("Helpdesk Voiza:")
	newLine.append(encodeWin(entry.replace("\enter", "\n"), "add"))

	data.append(newLine)
	writeCsvFile("tasks.csv", data)

# Adiciona tarefas com scopo livre
def addFree(data, date):
	newLine = []
	newLine.append(date.strftime("%d-%m-%Y %H:%M"))
	
	entry = raw_input("Nome da Tarefa:")
	while verifyTasks(entry, data) == True:
		entry = raw_input("Ja existe tarefa com esse nome. Informe outro nome de Tarefa:")
	newLine.append(encodeWin(entry, "add"))
	entry = raw_input("Informe o campo da mensagem:")	
	newLine.append(encodeWin(entry.replace("\enter", "\n"), "add"))
	
	data.append(newLine)
	writeCsvFile("tasks.csv", data)

# Imprime todas as tarefas presentes no arquivo csv
def list(data, hour):
	c = 0
	
	for row in data:
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
			temp = row[3].split(",")
			for element in temp:
				element = element.replace("[", "")
				element = element.replace("\'", "")
				element = element.replace("]", "")
				element = element.replace(" ", "", 1)
				print encodeWin(element, "list")
						
			print "\n--Helpdesk Voiza--" 
			if (hour < 13):
				print "Bom dia time,\n"
			else:
				print "Boa tarde time, \n"
			print encodeWin(row[4], "list") + "\n\nAtenciosamente."
			while len(row) > index:
				print "\n--Resposta--"
				print encodeWin(row[index], "list")
				index += 1
				print "\n--Helpdesk Voiza--"
				if (hour < 13):
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
def remove(data):
	count = 0
	entry = raw_input("Informe o que deseja remover:")
	if len(entry) < 2:
		for i in xrange(len(data)):
			if i == int(entry):
				del data[i]
				count += 1
	else:
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

# Busca uma tarefa por nome ou todas as tarefas por data
def find(data, hour):
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
			if row[1].lower() == entry:
				temp.append(row)
	
	list(temp, hour)
	print "\nForam encontrados "+str(len(temp))+ " resultados."

# Acrescenta a resposta do cliente + o Helpdesk Voiza a uma tarefa
def edit(data):
	entry = raw_input("Informe o nome da tarefa:")
	entry = entry.lower()
	for row in data:
		if row[1].lower() == entry:
			entry = raw_input("Resposta:")
			row.append(encodeWin(entry.replace("\enter", "\n"), "add"))
			entry = raw_input("Helpdesk Voiza:")
			row.append(encodeWin(entry.replace("\enter", "\n"), "add"))

	writeCsvFile("tasks.csv", data)

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
			print "\nTarefas que nao possuem horas alocadas."
	elif entry == "date":
		print "date"
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
				print "\nTarefas que nao possuem horas alocadas."
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
				print "\nNao foram encontradas horas alocadas."

# Edita uma alocação de hora (data ou tempo)
def editTime(time):
	entry = raw_input("Informe o nome da tarefa que deseja editar:")
	entry = entry.lower()
	for row in time:
		if entry == row[1].lower():
			entry = raw_input("Infome a nova data:")
			if entry != "":
				if validateData(entry) == True:
					row[0] = entry
			entry = raw_input("Informe a nova quantidade de horas:")
			if entry != "":
				row[2] = entry

	writeCsvFile("timeTasks.csv", time)

# Remove uma alocação de hora (pesquisa por data)
def removeTime(time):
	entry = raw_input("Informe o nome da tarefa que deseja remover:")
	entry = entry.lower()
	temp = []
	tempC = []
	c = 0
	for row in time:
		if entry == row[1].lower():
			temp.append(row)
			tempC.append(c)
		c += 1

	if len(temp) > 0:
		if len(temp) == 1:
			del time[tempC[0]]
		else:
			listHours(temp)
			entry = raw_input("\nInforme qual das horas alocadas deseja remover:")
			while int(entry) < 0 or int(entry) >= len(temp):
				entry = raw_input("Informe um indice valido:")
			del time[tempC[int(entry)]]
		writeCsvFile("timeTasks.csv", time)
	else:
		print "Nenhuma tarefa encontrada."

# Verifica se existe alocação de horas para determinada tarefa
def contaisHours(element, time):
	
	for row in time:
		if element.lower() == row[1].lower():
			return True

	return False

def verifyTasks(name, data):
	for row in data:
		if name == row[1]:
			return True
	
	return False

def encodeWin(string, op):
	if op == "add":
		return string.decode("cp850").encode("utf8")
	elif op == "list":	
		return string.decode("utf8").encode("cp850")


# Imprime as ações disponíveis no programa
def help():
	print "Voce pode realizar as seguintes acoes:"
	print "\nTarefas:"
	print "\t- add: para adicionar uma tarefa (usuarios do remedy nao podem possuir acentuacao);"
	print "\t- add free: para adicionar uma tarefa livre de mascaras"
	print "\t- find: para procurar uma tarefa por nome ou data;"
	print "\t- remove: para remover uma tarefa por nome ou indice;"
	print "\t- edit: para editar uma tarefa (reposta + helpdesk);"
	print "\t- list: para listar todas as tarefas cadastradas."
	print "Time:"
	print "\t- time add: para alocar horas em uma tarefa;"
	print "\t- time find: para procurar horas de determinada tarefa ou as tarefas sem horas (free);"
	print "\t- time remove: para remover as horas de uma tarefa;"
	print "\t- time edit: para editar a data ou as horas de uma tarefa;"
	print "\t- time list: para listar todas as horas alocadas."

	print "\n- show log: mostra todas as acoes realizadas;"
	print "- exit: sai do programa."

def developer():
	print "Se utilizar o bash, digitar 3 como parametro (sys);"
	print "Configuracao atual do cmd chcp 850 (encodeWin);"
	print "Comando time find > free: quando e listado uma tarefa sem horario é pq ele sofreu um edit e tem alocação de horas extras;"
	print "Decode + Encode para salvar em utf8 e printar no terminal em cp850."

def toDo():
	print "Dicionario para imprimir todas as horas alocadas por data;"
	print "Script de resetar senha: comando \scriptResetSenha;"

# Função main: trata as ações digitadas
def main(entry, fuso):

	data = readCsvFile("tasks.csv")
	time = readCsvFile("timeTasks.csv")

	date = datetime.datetime.now()

	if entry == "add":
		data = add(data, date, fuso)
	elif entry == "list":
		data = list(data, date.hour)
	elif entry == "remove":
		data = remove(data)
	#elif entry == "clean":
	#	writeCsvFile("tasks.csv", "")
	elif entry == "show log":
		showLog("logTasks.txt")
	elif entry == "find":
		find(data, date.hour)
	elif entry == "edit":
		edit(data)
	elif entry == "time add":
		timeAdd(time, data)
	elif entry == "time list":
		try:
			listHours(time)
		except IndexError:
			print "Nao existe horas trabalhadas."
	elif entry == "time find":
		findTime(time, date, data)
	elif entry == "add free":
		addFree(data, date)
	elif entry == "time edit":
		editTime(time)
	elif entry == "time remove":
		removeTime(time)
	elif entry == "help":
		help()
	elif entry == "--developer":
		developer()

	# Salva no log qual ação foi digitada (mesmo que não seja válida)
	temp = date.strftime("%d-%m-%Y")
	if date.hour > 9:
		hour = str(date.hour-int(fuso))
	else:
		hour = "0" + str(date.hour-int(fuso))
	if date.minute > 9:
		minute = str(date.minute)
	else:
		minute = "0" + str(date.minute)
	temp+= " " + hour + ":" + minute
	writeTxtFile("logTasks.txt", temp + " - " + entry + "\n")

# Início do programa
if (len(sys.argv) > 1):
	fuso = sys.argv[1]
else:
	fuso = 0
		
entry = raw_input("Digite uma acao:")

while (entry != "exit"):
	main(entry, fuso)
	entry = raw_input("\nDigite uma acao:")
