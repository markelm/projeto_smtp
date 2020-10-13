#cliente SMTP que se comunica sem nenhum protocolo de seguranca

import smtplib #biblioteca para implementar o clinete
import email.utils #provem funcoes utilitarias para formatacao/geracao
from email.mime.text import MIMEText#classe de mensagens
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
#criando mensagem a ser enviada

#msg = MIMEText("Bilbo esta com saudades. Pediu para vc trazer o anel.")
#msg["To"] = email.utils.formataddr(("Aragorn", "aragorn@gondor.com"))
#msg["From"] = email.utils.formataddr(("Frodo", "frodo@gondor.com"))
#msg["Subject"] = "Quando voce vem pra ca?"


msg = MIMEMultipart()
body = "Bilbo esta com saudades. Pediu para vc trazer o anel."
msg["To"] = "aragorn@rivendell.com"
msg["From"] = "arwen@rivendell.com"
msg["Subject"] = "Quando voce vem pra ca?"

msg.attach(MIMEText(body, 'plain'))

filename = 'test.txt'
attachment = open(filename, 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= "+filename)
msg.attach(part)

#Agora criamos o servidor SMTP que roda do lado do cliente para enviar
server = smtplib.SMTP("127.0.0.2", 1026)
server.set_debuglevel(True)#debug para ver a interacao de msgs

#enviamos a msg
server.sendmail("arwen@rivendell.com", ["aragorn@rivendell.com"], msg.as_string())

#encerra
server.quit()
