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

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from . import connect
from sqlalchemy.orm import relationship

class User(connect.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32))
    password = Column(String(32))
    address = Column(String(128))
    call = Column(String(32))
    age = Column(Integer)
    reply = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    dangers = relationship("Danger", back_populates="user")

class Message(connect.Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(String(128))

class Danger(connect.Base):
    __tablename__ = "danger"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="dangers")
