# from pydantic import BaseModel
# from schemas.model import ModelProviderAuthBase


# class UserBase(BaseModel):
#     id: str
#     username: str
#     email: str
#     password: str


# class UserCreate(UserBase):
#     pass


# class UserRead(UserBase):
#     id: str
#     username: str
#     email: str
#     model_provider_auths: list[ModelProviderAuthBase] = []

#     class Config:
#         from_attributes = True
