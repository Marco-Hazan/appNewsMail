class News:

    def __init__(self,msgid,sender,subject,channels,body,htmlbody,creation_date,pub_date,expiration_date):
        if id == None or sender == None or subject == None or channels == None or body == None or creation_date == None or expiration_date == None:
            raise TypeError('Non ci possono essere argomenti None')
        self.__msgid = msgid
        self.__sender = sender
        self.__channels = []
        for c in channels:
            self.__channels.append(c)
        self.__subject = subject
        self.__body = body
        self.__htmlbody = htmlbody
        self.__is_html = False
        self.__htmlbody =  None
        self.__creation_date = creation_date
        self.__pub_date = pub_date
        self.__expiration_date = expiration_date

    def __str__(self):
        s = "sender:"+self.__sender+"\nsubject:"+self.__subject + "\n";
        s += "pub_date: "+ self.__pub_date
        for c in self.__channels:
            s += c + "\t"
        s += "\n"+self.__body;
        return s

    @property
    def sender(self):
        return self.__sender

    @property
    def subject(self):
        return self.__subject

    @property
    def channels(self):
        return self.__channels

    @property
    def body(self):
        return self.__body

    @property
    def msgid(self):
        return self.__msgid

    @property
    def is_html(self):
        return self.__ishtml

    @property
    def htmlbody(self):
            return self.__htmlbody

    @property
    def creation_date(self):
        return self.__creation_date

    @property
    def pub_date(self):
        return self.__pub_date

    @property
    def expiration_date(self):
        return self.__expiration_date
