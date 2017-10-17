# -*- coding: utf-8 -*-

import smtplib
import sys


def sendEmails(emails):

	fromaddr = 'comoecampina@gmail.com'
	username = 'comoecampina@gmail.com'
	password = 'comoecampina2017'
	server = None

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(username,password)
	except Exception as e:
		print "failed to login" + str(e.args) + " " + str(e)

	for data in emails:
		userData = data.split(",")
		toaddrs  = userData[1]

		# Prepare actual message
		msg = 'Olá ' + userData[0] + ', \n Como está? Estamos te enviando primeiramente para agradecer por sua contribuição em nossa versão anterior do projeto Como é Campina? na plataforma Contribua (https://contribua.org). A partir da sua ajuda conseguimos entender melhor a relação entre elementos presentes nas cidades, como árvores, carros, pessoas nas ruas e as percepções de segurança e agradabilidade de nossos contribuidores. Com isso, pudemos contribuir para o aperfeiçoamento da maneira como pesquisas de percepção podem utilizar ferramentas de computação como o Como é Campina? \nAgora uma nova versão do projeto foi lançada na plataforma. Nessa nova fase, estamos tentando melhorar ainda mais essas ferramentas de modo que automaticamente possamos construir a percepção sobre ruas e, assim, possamos agilizar ainda mais o trabalho de gestores e urbanistas na detecção de problemas e na melhoria das nossas cidades. Para isso precisamos novamente da sua ajuda! \n Você poderia nos ajudar novamente? Basta acessar a URL do projeto https://contribua.org/project/ruascampina/, fazer login com a sua conta e em 5 minutos responder mais algumas comparações de imagens. Sua ajuda é muito importante para nós. \n\n\n Atenciosamente, \n Equipe do Como é Campina?'
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
		""" % (fromaddr, toaddrs, "Nova Versão do Como é Campina?", msg)
		try:		
			server.sendmail(fromaddr, toaddrs, message)
			server.quit()
			server.close()
			print 'successfully sent the mail'
		except Exception as e:
			print "failed to send mail" + str(e.args) + " " + str(e)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com conjunto de e-mails para os quais a mensagem deve ser enviada>"
		sys.exit(1)

	dataFile1 = open(sys.argv[1], 'r')

	sendEmails(dataFile1.readlines())
