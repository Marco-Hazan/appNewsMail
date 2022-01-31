class News:

    def __init__(self,msgid,sender,title,body,htmlbody,creation_date,expiration_date):
        if id == None or sender == None or title == None or creation_date == None:
            raise TypeError('Non ci possono essere argomenti None')
        self.__msgid = msgid
        self.__sender = sender
        self.__title = title
        self.__body = body
        self.__htmlbody = htmlbody
        self.__creation_date = creation_date
        self.__expiration_date = expiration_date

    def __str__(self):
        s = "sender:"+self.__sender+"\ntitle:"+self.__title + "\n";
        s += "\n"+self.__htmlbody;
        return s

    def __eq__(self,other):
        if other is None:
            return False
        return other.msgid is not self.msgid


    @property
    def sender(self):
        return self.__sender

    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body

    @property
    def msgid(self):
        return self.__msgid

    def is_html(self):
        return self.__htmlbody is not None

    @property
    def htmlbody(self):
            return self.__htmlbody

    @property
    def creation_date(self):
        return self.__creation_date

    @property
    def expiration_date(self):
        return self.__expiration_date
