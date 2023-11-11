# Copyright 2023 gwondongmin
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pydantic import BaseModel

class DangerBase(BaseModel):
    image: str
    time: str
    user_id: int

class DangerCreate(DangerBase):
    pass

class Danger(DangerBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str
    address: str
    call: str
    age: int

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    reply: bool
    dangers: list[Danger] = []

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    message: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    activate: bool

    class Config:
        orm_mode = True
