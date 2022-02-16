import os
from functions.config import Config


class Attachments:

    def getAttachments(msgid):
        attachments = []
        for file in os.listdir(Config.get("attachments_path")+msgid):
            attachments.append(
                Config.get("attachments_path") + msgid + "/" + file
            )
        return attachments
