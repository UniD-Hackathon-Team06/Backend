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
from sqlalchemy.orm import Session

from . import models, schema

def create_danger(db: Session, danger: schema.Danger):

    args = {
        'image': danger.image,
        'time': danger.time,
        'user_id': danger.user_id,
    }

    db_danger = models.Danger(**args)
    db.add(db_danger)
    db.commit()
    db.refresh(db_danger)
    return db_danger

def get_danger_by_id(db: Session, id: int):
    return db.query(models.Danger).filter(models.Danger.user_id == id).first()