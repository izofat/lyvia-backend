import bcrypt
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(default=1)
    password: str
    username: str
    name: str
    lastName: str
    email: str

    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()

    def decrypt_password(self, decrypted_password: str):
        return bcrypt.checkpw(decrypted_password.encode(), self.password.encode())
