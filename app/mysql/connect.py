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

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "mysql+pymysql://root:1234@mysql:3306/unidthon"

class engineconn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def getDB(self):
        db = self.sessionLocal()
        try:
            yield db
        finally:
            db.close()
        return db

    def connection(self):
        conn = self.engine.connect()
        return conn

Base = declarative_base()