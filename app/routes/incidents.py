from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
incidents_bp = Blueprint('incidents', __name__)

DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DB_URL)

@incidents_bp.route('/incidents/by-type')
def by_type():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT incident_type, COUNT(*) as count FROM incidents GROUP BY incident_type"
        ))
        return jsonify([dict(r) for r in result.mappings()])

@incidents_bp.route('/incidents/by-site')
def by_site():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT s.operator_name, COUNT(*) as incident_count
            FROM incidents i
            JOIN sites s ON i.site_id = s.site_id
            GROUP BY s.operator_name
            ORDER BY incident_count DESC
        """))
        return jsonify([dict(r) for r in result.mappings()])

@incidents_bp.route('/incidents/trifr')
def trifr():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                s.operator_name,
                COUNT(*) as total_incidents,
                SUM(i.days_lost) as total_days_lost,
                ROUND(COUNT(*) * 1000000.0 / NULLIF(s.lease_count * 2000, 0), 2) as trifr
            FROM incidents i
            JOIN sites s ON i.site_id = s.site_id
            WHERE i.incident_type IN ('LTI', 'MTI', 'FAI', 'Fatality')
            GROUP BY s.operator_name, s.lease_count
            ORDER BY trifr DESC
        """))
        return jsonify([dict(r) for r in result.mappings()])