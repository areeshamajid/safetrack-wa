import pandas as pd
from sqlalchemy import create_engine, text
from app.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL)

def load_all():
    print('Dropping existing tables...')
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS compliance_actions CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS near_miss CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS incidents CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS inspections CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS workers CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS sites CASCADE"))
        conn.commit()

    print('Creating tables...')
    Base.metadata.create_all(engine)

    tables = {
        'sites':              'data/processed/sites.csv',
        'workers':            'data/processed/workers.csv',
        'incidents':          'data/processed/incidents.csv',
        'near_miss':          'data/processed/near_miss.csv',
        'inspections':        'data/processed/inspections.csv',
        'compliance_actions': 'data/processed/compliance_actions.csv',
    }

    for table, path in tables.items():
        df = pd.read_csv(path)
        df.columns = [c.lower() for c in df.columns]
        df.to_sql(table, engine, if_exists='append', index=False)
        print(f'  Loaded {len(df):,} rows into {table}')

    print('Done.')

if __name__ == '__main__':
    load_all()