import uuid

class Client:
    
    def __init__(self, name, email, company, position, uid=None):
        self.name = name
        self.email = email
        self.company = company
        self.position = position
        self.uid = uid or uuid.uuid4()
    
        
    def to_dict(self):
        return vars(self)
    
    @staticmethod
    def schema():
        return ['uid', 'name', 'email', 'company', 'position',]
    