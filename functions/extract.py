import email
import os
import base64
from os import path


class Extraction:


    def extractSender(email):
        tot_sender = email.get('From')
        return tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]

    def extractBody(email):
        body = ""
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == 'text/plain':
                    body += part.get_payload().replace("\n","")
        else:
            if email.get_content_type() == 'text/plain':
                body = email.get_payload()
        return body


    def extractHtml(email):
        bodyhtml = None
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == 'text/html':
                    #if BeautifulSoup(part.get_payload(), "html.parser").find():
                        #soup = BeautifulSoup(part.get_payload(), "html.parser")
                        #headerhtml = soup.find('head')
                        #bodyhtml = soup.find('body')
                        #bodyhtml = bodyhtml.decode_contents().replace("\n","")
                    bodyhtml = part.get_payload()
        else:
            if email.get_content_type() == 'text/html':
                #if BeautifulSoup(part.get_payload(), "html.parser").find():
                    #soup = BeautifulSoup(part.get_payload(), "html.parser")
                    #headerhtml = soup.find('head')
                    #bodyhtml = soup.find('body')
                    #bodyhtml = bodyhtml.decode_contents().replace("\n","")
                bodyhtml = email.get_payload()
        return bodyhtml

    def extractAttachments(email,msgid):
        attachments = []
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() != 'text/plain' and part.get_content_type() != 'multipart/mixed' and part.get_content_type != 'text/html' and part.get_content_type() != 'multipart/alternative':
                    try:
                        os.mkdir("/home/marco/appNewsMail/attachments/"+str(msgid))
                        os.system("chown marco /home/marco/appNewsMail/attachments/"+str(msgid))
                        os.system("chmod 777 /home/marco/appNewsMail/attachments/"+str(msgid))
                    except OSError:
                        pass
                    if part.get_filename() is not None:
                        filename = part.get_filename()
                        attachments.append(filename)
                        with open("/home/marco/appNewsMail/attachments/"+str(msgid)+"/"+filename, 'ab') as f:
                            try:
                                os.system("chmod 777 /home/marco/appNewsMail/attachments/"+str(msgid)+"/"+filename)
                                message_bytes = base64.b64decode(str(part.get_payload()))
                                f.write(message_bytes)
                            except ValueError:
                                pass
        return attachments
