from sqlalchemy import Column, func
from sqlalchemy import Integer, TIMESTAMP

TSZ = TIMESTAMP(timezone=True)

def common_columns():
    return [
        Column("id"        , Integer , primary_key=True, autoincrement=True),
        Column("created_at", TSZ     , index=True, server_default=func.current_timestamp()),
        Column("updated_at", TSZ     , index=True, server_default=func.current_timestamp(), onupdate=func.current_timestamp()),
    ]
