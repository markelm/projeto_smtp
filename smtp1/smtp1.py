import smtplib
import smtpd #bib do servidor
import asyncore #multiplas conexoes
import os
import base64

#tabela com 
domainTable = {'rivendell.com': ['127.0.0.2', 1026]}
destination = 'home'
receiver = ''

def createFolder(direc):
    print('chamando createFolder')
    try:
        if not os.path.exists(direc):
            os.makedirs(direc)
    except OSError:
        print ('Error: creating directory. ' + direc)


#simula request para o DNS e caso nao encontrado return a string 'Not Found'
def DNSrequest(domain):
    return domainTable.get(domain, 'Not Found')

#classe herdada para sobrescrita do metido de processamento de mensagens
class CustomsSMTPServer(smtpd.SMTPServer):
    
    #metodo de processamento de mensagens
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        print("Mensagem enviada pelo IP {}".format(peer))
        print("Mensagem enviada pelo e-mail {}".format(mailfrom))
        print("Mensagem destinada ao e-mail {}".format(rcpttos))
        print("Tamanho da mensagem: {}".format(len(data)))
        print(f'{data}')

        #obtendo a bytecode do anexo
        datatemp = data.decode('utf-8')
        data_loc = datatemp.find('attachment; filename=')
        datatemp = f'{datatemp[data_loc:]}'

        #nome do arquivo
        name_loc = datatemp.find('=')
        filename = datatemp[name_loc + 2: datatemp.find('\n')]
        #print(filename)

        data_loc = datatemp.find('\n\n')
        datatemp = f'{datatemp[data_loc + 2:]}'
        data_loc = datatemp.find('\n\n')
        datatemp = f'{datatemp[:data_loc]}'
        #print(datatemp)
        #fim da obtencao do bytecode do anexo

        destination = rcpttos[0]
        receiver = destination[:destination.find('@')]
        #print(receiver)
        destination = destination[destination.find('@') + 1:]
        if destination == 'gondor.com':
            destination = 'home'
        #print(destination)
        #print(domainTable[destination])

        if destination != 'home':
            d = DNSrequest(destination)
            print('\nDESTINATION ACQUIRED!!!')
            server_to = smtplib.SMTP(d[0], d[1])
            server_to.sendmail(mailfrom, rcpttos, data)
        else:
            createFolder(f'./{receiver}/Inbox/')
            f = open(f'./{receiver}/Inbox/msg_{mailfrom}.txt', 'w+')
            f.write(f'{data}')

            base64_bytes = datatemp.encode('utf-8')
            with open(f'./{receiver}/Inbox/{filename}', 'wb') as file_to_server:
                decoded_bytes = base64.decodebytes(base64_bytes)
                file_to_server.write(decoded_bytes)

server = CustomsSMTPServer(("127.0.0.1", 1025), None)

print("Servidor em execucao")
asyncore.loop()#entra em loop para aceitar multiplas conexoes(se necessario)


