import email
import os
import base64
import quopri
from functions.config import Config


class Extraction:

    def extractSender(mail):
        tot_sender = mail.get('From')
        return tot_sender[tot_sender.find("<")+1:tot_sender.find(">")]

    def extractBody(mail):
        body = ""
        if mail.is_multipart():
            for part in mail.walk():
                if (
                        part.get_content_type() == 'text/plain'
                        and part.get_filename() is None
                ):
                    body += Extraction.decodeBody(part)
            body = body.rstrip()
        else:
            if mail.get_content_type() == 'text/plain':
                body = Extraction.decodeBody(mail)
        return body

    def extractHtml(mail):
        bodyhtml = None
        if mail.is_multipart():
            for part in mail.walk():
                if part.get_content_type() == 'text/html':
                    bodyhtml = Extraction.decodeBody(part)
        else:
            if mail.get_content_type() == 'text/html':
                bodyhtml = Extraction.decodeBody(mail)
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
                                    "chmod 755 "
                                    + Config.get("attachments_path")
                                    + iddir+"/"+filename)
                            except ValueError:
                                pass
            if directorycreated:
                os.system(
                    "chmod 755 " + Config.get("attachments_path") + iddir)
        return attachments

    def extractPublicKey(msg):
        if msg.is_multipart():
            for part in msg.walk():
                if(
                    "application/pgp-keys" in part["Content-Type"]
                ):
                    print(part["Content-Transfer-Encoding"])
                    with open(
                        Config.get("master_path") + "registration_pubkey.pgp",
                        "w"
                    ) as f:
                        if(
                            part["Content-Transfer-Encoding"] == "quoted-printable"
                        ):
                            f.write(quopri.decodestring(str(part.get_payload())).decode("utf-8"))
                        elif part["Content-Transfer-Encoding"] == "base64":
                            message_bytes = base64.b64decode(
                                message_bytes = str(part.get_payload())
                            )
                            quopri.decodestring(message_bytes).decode("utf-8")
                            print(message_bytes)
                            f.write(message_bytes)
                        else:
                            f.write(str(part.get_payload()))
                        f.close()
                    return Config.get("master_path") + "registration_pubkey.pgp"

    def decodeBody(part):
        if part['Content-Transfer-Encoding'] == 'base64':
            return  base64.b64decode(
                part.get_payload()).decode('latin-1').encode('latin-1').decode('utf-8')
        elif part['Content-Transfer-Encoding'] == 'quoted-printable':
            return quopri.decodestring(str(part.get_payload())).decode("utf-8")
        else:
            return part.get_payload()
