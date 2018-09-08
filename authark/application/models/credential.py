class Credential:
    def __init__(self, id: str, user_id: str, value: str,
                 type: str = 'password') -> None:
        self.id = id
        self.user_id = user_id
        self.type = type
        self.value = value