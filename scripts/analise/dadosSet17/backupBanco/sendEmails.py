# -*- coding: utf-8 -*-

import smtplib
import sys
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Added
from email.mime.image import MIMEImage


def sendEmails(emails):

	fromaddr = "davcandeia@gmail.com"#'comoecampina@gmail.com'
	username = "davcandeia@gmail.com"#'comoecampina@gmail.com'
	password = "erigm201409"#'comoecampina2017'
	server = None

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(username,password)
	except Exception as e:
		print "failed to login" + str(e.args) + " " + str(e)

	for data in emails:#["davcandeia@gmail.com,David"]:
		userData = data.split(",")
		toaddrs  = userData[0].strip(' \t\n\r')
		#subject = "Nova Versão do Como é Campina?"
		subject = "Alumni Contact - Help in Research"

		# Prepare actual message
		#msg = 'Olá ' + userData[1].strip(' \t\n\r') + ', <br><br>Como está? Primeiramente queríamos te agradecer por sua contribuição em nossa versão anterior do projeto Como é Campina?, aquele mesmo que te pediu para comparar fotos da cidade de Campina Grande. A partir da sua ajuda conseguimos entender melhor a relação entre elementos presentes nas cidades (e.g., como árvores, carros e pessoas nas ruas) e as percepções de segurança e agradabilidade de nossos contribuidores. Com isso, pudemos contribuir para o aperfeiçoamento da maneira como pesquisas de percepção podem utilizar ferramentas de computação como o Como é Campina? <br><br>Em nossa nova versão do projeto, estamos tentando melhorar ainda mais essas ferramentas de modo que automaticamente possamos construir a percepção sobre ruas e, assim, agilizar ainda mais o trabalho de gestores e urbanistas na detecção de problemas e na melhoria das nossas cidades. Para isso <b>precisamos novamente da sua ajuda!</b> <br><br>Basta acessar a URL do projeto https://contribua.org/project/ruascampina/, fazer login com a sua conta (se você não lembrar da sua senha você pode resgatá-la, ou entrar com uma conta sua do Facebook ou Google) e em 5 minutos responder mais algumas comparações de imagens. Sua ajuda é muito importante para nós. Vamos contribuir? <br><br><br> Abraços, <br> Equipe do Como é Campina?'
		msg = 'Hi ' + userData[1].strip(' \t\n\r') + ', <br><br>How are you? My name is David, I\'ve participated in the Study of the United States Institutes for Student Leaders from Brazil in 2009, an US Department of State program, and currently I\'m a Computer Science PhD candidate. <br> <br> I\'ve found your contact through the US programs alumni website and I\'m here to ask you for a help with our research. We\'re studying how computer systems can help in urban planning by capturing and analyzing impressions about images of cities. We\'re asking people to give their impressions about some city images, pointing the scenes that look more pleasant to them. It\'s very important to us to gather opinions from different places and cultures, and your contribution is very important to help us achieve that. <br><br> In 5 minutes you can login in our site (you can use your Facebook or Google account) <br><br> https://contribua.org/project/ruascampina/ <br><br> And answer some images comparison. I would really appreciate your help. <br><br> Thanks in advance! <br><br> David Candeia M Maia - <br> http://www.lsd.ufcg.edu.br/~davidcmm/ <br> http://sites.google.com/site/davidcmmaia/ <br><br> Mestre em Ciência da Computação pela Universidade Federal de Campina Grande<br>Professor do Instituto de Educação, Ciência e Tecnologia do Estado da Paraíba - IFPB<br>Paraíba - Brasil<br><br>MS in Computer Science at Federal University of Campina Grande<br>Professor at Instituto de Educação, Ciência e Tecnologia do Estado da Paraíba - IFPB<br>Paraíba - Brazil'
		#message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
		#""" % (fromaddr, toaddrs, "Nova Versão do Como é Campina?", msg)
		#message = email.message.Message()
		message = MIMEMultipart()
		message['Subject'] = subject
		message['From'] = fromaddr
		message['To'] = toaddrs
		message.add_header('Content-Type','text/html')
		#message.set_payload(msg)
		message.attach(MIMEText(msg, 'html'))

		fp = open("/home/davidcmm/workspace_doutorado/campinaPulse/imagens_divulgacao/avatar.jpg", "rb")#open("/local/david/pybossa_env/campinaPulse/imagens_divulgacao/avatar.jpg", 'rb')                                                    
		img = MIMEImage(fp.read())
		fp.close()
		img.add_header('Content-ID', '<{}>'.format("/local/david/pybossa_env/campinaPulse/imagens_divulgacao/avatar.jpg"))
		message.attach(img)

		try:		
			server.sendmail(fromaddr, toaddrs, message.as_string())
			print 'successfully sent the mail to ' + str(toaddrs)
		except Exception as e:
			print "failed to send mail" + str(e.args) + " " + str(e)

	try:
		server.quit()
		server.close()
	except Exception as e:
		print "failed to close " + str(e.args) + " " + str(e)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com conjunto de e-mails para os quais a mensagem deve ser enviada>"
		sys.exit(1)

	dataFile1 = open(sys.argv[1], 'r')

	sendEmails(dataFile1.readlines())
