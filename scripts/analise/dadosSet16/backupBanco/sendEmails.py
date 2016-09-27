import smtplib

fromaddr = 'davcandeia@gmail.com'
toaddrs  = 'david.maia@ifpb.edu.br'
msg = 'Why,Oh why!'
username = 'davcandeia@gmail.com'
password = 'davgm201409'

# Prepare actual message
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (fromaddr, toaddrs, "Teste", msg)

try:
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	server.close()
	print 'successfully sent the mail'
except:
	print "failed to send mail"
