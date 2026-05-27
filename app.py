from app import create_app
from flask import jsonify

app = create_app()

@app.route('/')
def health():
    return jsonify({'status': 'ok', 'project': 'SafeTrack WA'})

@app.route('/summary')
def summary():
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    import os
    load_dotenv()
    DB_URL = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(DB_URL)
    tables = ['sites', 'workers', 'incidents', 'near_miss', 'inspections', 'compliance_actions']
    summary = {}
    with engine.connect() as conn:
        for t in tables:
            result = conn.execute(text(f'SELECT COUNT(*) FROM {t}'))
            summary[t] = result.scalar()
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
