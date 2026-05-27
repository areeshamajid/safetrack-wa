from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
safety_bp = Blueprint('safety', __name__)

DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DB_URL)

@safety_bp.route('/nearmiss/trend')
def nearmiss_trend():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                DATE_TRUNC('month', report_date::date) as month,
                COUNT(*) as count
            FROM near_miss
            GROUP BY month
            ORDER BY month
        """))
        return jsonify([dict(r) for r in result.mappings()])

@safety_bp.route('/inspections/compliance-rate')
def compliance_rate():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                s.operator_name,
                COUNT(*) as total_inspections,
                SUM(CASE WHEN i.passed THEN 1 ELSE 0 END) as passed,
                ROUND(AVG(i.score), 1) as avg_score
            FROM inspections i
            JOIN sites s ON i.site_id = s.site_id
            GROUP BY s.operator_name
            ORDER BY avg_score DESC
        """))
        return jsonify([dict(r) for r in result.mappings()])

@safety_bp.route('/compliance/overdue')
def overdue():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                ca.action_id,
                s.operator_name,
                ca.action_description,
                ca.due_date,
                ca.priority
            FROM compliance_actions ca
            JOIN sites s ON ca.site_id = s.site_id
            WHERE ca.status = 'Overdue'
            ORDER BY ca.due_date ASC
            LIMIT 50
        """))
        return jsonify([dict(r) for r in result.mappings()])