from sqlalchemy import create_engine, inspect
from backend.app.core.config import settings

eng = create_engine(settings.DATABASE_URL)
ins = inspect(eng)
print('tables:', ins.get_table_names())
