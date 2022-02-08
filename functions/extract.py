import email
import os
import base64
from os import path
from functions.config import Config


class Extraction:


    def extractSender(email):
        tot_sender = email.get('From')
        return tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]

    def extractBody(email):
        body = ""
        if email.is_multipart():
            for part in email.walk():
                if part.get_content_type() == 'text/plain':
                    if part['Content-Transfer-Encoding'] == 'base64':
                        body += base64.b64decode(part.get_payload()).decode("UTF-8")
                    else:
                        body += str(part.get_payload())
        else:
            if email.get_content_type() == 'text/plain':
                if email['Content-Transfer-Encoding'] == 'base64':
                    body = base64.b64decode(email.get_payload()).decode("UTF-8")
                else:
                    body = str(email.get_payload())
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
        iddir = str(msgid)[0:32]
        attachments = []
        directorycreated = False
        if email.is_multipart():
            for part in email.walk():
                if part.get_filename() is not None:
                    print(part.get_filename())
                    if part["Content-Type"].split(";")[0] != "application/pgp-signature":
                        if not directorycreated:
                            os.mkdir(Config.get("attachments_path")+iddir)
                            directorycreated = True
                        filename = part.get_filename()
                        attachments.append(filename)
                        with open(Config.get("attachments_path")+iddir+"/"+filename, 'ab') as f:
                            try:
                                message_bytes = base64.b64decode(str(part.get_payload()))
                                f.write(message_bytes)
                                os.system("chmod 744 "+ Config.get("attachments_path") +iddir+"/"+filename)
                            except ValueError:
                                pass
            if directorycreated:
                os.system("chmod 744 "+ Config.get("attachments_path") +iddir)
        return attachments
