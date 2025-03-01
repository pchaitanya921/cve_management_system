from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database import get_db
from models import CVEEntry
from backend.models import get_db
from flask import Blueprint, request, jsonify


filter_routes = Blueprint('filter_routes', __name__)
router = APIRouter()

# Filter by CVE ID
@router.get("/cves/{cve_id}")
def get_cve_by_id(cve_id: str, db: Session = Depends(get_db)):
    cve = db.query(CVEEntry).filter(CVEEntry.cve_id == cve_id).first()
    if not cve:
        raise HTTPException(status_code=404, detail="CVE not found")
    return cve

# Filter by Year
@router.get("/cves/year/{year}")
def get_cves_by_year(year: int, db: Session = Depends(get_db)):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    cves = db.query(CVEEntry).filter(CVEEntry.published_date.between(start_date, end_date)).all()
    return {"count": len(cves), "results": cves}

# Filter by CVE Score
@router.get("/cves/score/{score}")
def get_cves_by_score(score: float, db: Session = Depends(get_db)):
    cves = db.query(CVEEntry).filter(CVEEntry.cvss_score >= score).all()
    return {"count": len(cves), "results": cves}

# Filter by Last Modified in N days
@router.get("/cves/recent/{days}")
def get_recent_cves(days: int, db: Session = Depends(get_db)):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    cves = db.query(CVEEntry).filter(CVEEntry.last_modified_date >= cutoff_date).all()
    return {"count": len(cves), "results": cves}


@filter_routes.route('/api/cve/filter', methods=['GET'])
def filter_cve():
    """Filters CVEs based on severity and date range."""
    severity = request.args.get('severity')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    db = get_db()
    query = "SELECT cve_id, description, published_date, severity FROM cve_entries WHERE 1=1"
    params = {}

    if severity:
        query += " AND severity = :severity"
        params["severity"] = severity

    if start_date and end_date:
        query += " AND published_date BETWEEN :start_date AND :end_date"
        params["start_date"] = start_date
        params["end_date"] = end_date

    cves = db.execute(query, params).fetchall()

    return jsonify({"cve_list": [dict(row) for row in cves]})