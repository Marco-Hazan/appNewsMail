import os
from functions.config import Config


class Attachments:

    def getAttachments(msgid):
        attachments = []
        if os.path.exists(Config.get("attachments_path")+msgid):
            for file in os.listdir(Config.get("attachments_path")+msgid):
                attachments.append(
                    Config.get("attachments_path") + msgid + "/" + file
                )
        return attachments
