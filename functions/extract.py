import email
import os
import base64
from functions.config import Config


class Extraction:

    def extractSender(mail):
        tot_sender = mail.get('From')
        return tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]

    def extractBody(mail):
        body = ""
        if mail.is_multipart():
            print()
            for part in mail.walk():
                if (
                        part.get_content_type() == 'text/plain'
                        and part.get_filename() is None
                ):
                    if part['Content-Transfer-Encoding'] == 'base64':
                        body += base64.b64decode(part.get_payload()
                                                 ).decode("UTF-8")
                    else:
                        body += str(part.get_payload())
            body = body.rstrip()
        else:
            if mail.get_content_type() == 'text/plain':
                if mail['Content-Transfer-Encoding'] == 'base64':
                    body = base64.b64decode(
                        mail.get_payload()).decode("UTF-8")
                else:
                    body = str(mail.get_payload()).rstrip()
        return body

    def extractHtml(mail):
        bodyhtml = None
        if mail.is_multipart():
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    bodyhtml = part.get_payload()
        else:
            if mail.get_content_type() == 'text/html':
                bodyhtml = mail.get_payload()
        return bodyhtml

    def extractAttachments(mail, msgid):
        iddir = str(msgid)[0:32]
        attachments = []
        directorycreated = False
        if mail.is_multipart():
            for part in mail.walk():
                if part.get_filename() is not None:
                    print(part.get_filename())
                    if (
                        part["Content-Type"].split(";")[0]
                        != "application/pgp-signature"
                    ):
                        if not directorycreated:
                            os.mkdir(Config.get("attachments_path")+iddir)
                            directorycreated = True
                        filename = part.get_filename()
                        attachments.append(filename)
                        with open(
                                Config.get("attachments_path")
                                + iddir+"/"+filename,
                                'ab'
                                ) as f:
                            try:
                                message_bytes = base64.b64decode(
                                    str(part.get_payload()))
                                f.write(message_bytes)
                                os.system(
                                    "chmod 744 "
                                    + Config.get("attachments_path")
                                    + iddir+"/"+filename)
                            except ValueError:
                                pass
            if directorycreated:
                os.system(
                    "chmod 744 " + Config.get("attachments_path") + iddir)
        return attachments
