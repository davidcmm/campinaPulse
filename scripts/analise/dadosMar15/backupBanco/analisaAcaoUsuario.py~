# coding=utf-8

import sys
import datetime
import os

import smtplib
import mimetypes
import email
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio


#Calculates the last time user has contributed to the system
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo periodo no qual usuario atuou no sistema>"
		sys.exit(1)

	dataFile = open(sys.argv[1], "r")
	lines = dataFile.readlines()

	userAction = {}

	for line in lines:
		data = line.split(",")
		userName = data[1]		
		mail = data[2]
		timeString = data[3]
		actionDate = datetime.datetime.strptime(timeString.strip(), "%Y-%m-%dT%H:%M:%S.%f").date()
		if mail.strip() not in userAction.keys():
			timePassed = (actionDate.today() - actionDate).days
			userAction[mail.strip()] = {userName.strip() : timePassed}
	
	#Sending emails
	user = "comoecampina@gmail.com"
	passw = "c0m0ec@mp1n@LSD"
	for mail in userAction.keys():
		for name in userAction[mail].keys():
			smtp_host = 'smtp.gmail.com'
			smtp_port = 587
			server = smtplib.SMTP()
			server.connect(smtp_host,smtp_port)
			server.ehlo()
			server.starttls()
			server.login(user,passw)
			fromaddr = "Como é Campina?"
			tolist = ["davcandeia@gmail.com"]
			sub = "Estamos sentindo sua falta!"

			msg = email.MIMEMultipart.MIMEMultipart()
			msg['From'] = fromaddr
			msg['To'] = email.Utils.COMMASPACE.join(tolist)
			msg['Subject'] = sub  
			msg.attach(MIMEText("Olá "+name+",\n\n"+"Tudo bem com você? Sua contribuição no Como é Campina? foi muito importante para finalizarmos 77% das nossas tarefas, estamos sentindo a sua falta! Você visitou nossa plataforma há "+ str(userAction[mail][name]) + " dias, mas a Ciência Cidadã ainda precisa de você! \n\n Gostaríamos de contar com mais uma contribuição sua: ajude-nos a divulgar nosso projeto de modo a  finalizarmos 100% das nossas tarefas, faça a diferença!\n\n Compartilhe o link do nosso projeto em suas redes sociais, convide seus amigos a participar e contribua conosco!\n"))
			msg.attach(MIMEText("<a href=https://www.facebook.com/sharer/sharer.php?u=https://contribua.org/pybossa/app/comoecampina><img src=\"https://contribua.org/aguanossa/images/facebook.png\"/></a> <a href=https://twitter.com/intent/tweet?text=Ajude&nbsp;a&nbsp;melhorar&nbsp;Campina&nbsp;avaliando&nbsp;fotos&nbsp;da&nbsp;cidade&url=https://contribua.org/pybossa/app/comoecampina&original_referer=><img src=\"https://contribua.org/aguanossa/images/twitter.png\"/></a>", "html"))
			msg.attach(MIMEText("\n"))
			msg.attach(MIMEText("Abraços,\n Equipe do Como é Campina?"))
			#img_data = open('facebook.png', 'rb').read()
			#msg.attach(MIMEImage(img_data, 'png'))
			#msg.attach(MIMEText('\nsent via python', 'plain'))
			server.sendmail(user,tolist,msg.as_string())
	
			print str(mail)+"\t"+ str(name)+"\t"+str(userAction[mail][name])
			break
