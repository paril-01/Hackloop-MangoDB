from sqlalchemy import inspect
from app.core.database import engine
ins = inspect(engine)
print('tables:', ins.get_table_names())
