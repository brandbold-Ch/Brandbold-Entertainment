from sqlmodel import Session


class UserServices:

    def __init__(self, session: Session):
        self.session = session
