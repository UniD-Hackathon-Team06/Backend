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

def set_message_template(db: Session, template_id: int):
    item = db.query(models.MessageTemplate).filter(models.MessageTemplate.id == template_id).first()

    if item is None:
        return None

    message = item.template
    print(message)
    item.activate = True
    db.commit()

    args = {
        'message': message
    }

    db_message = models.Message(**args)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message
