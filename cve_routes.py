from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database import get_db, CVEEntry

router = APIRouter()

@router.get("/cves/")
def get_cves(
    cve_id: str = Query(None, title="CVE ID"),
    year: int = Query(None, title="Year"),
    min_score: float = Query(None, title="Minimum CVE Score"),
    max_score: float = Query(None, title="Maximum CVE Score"),
    last_modified_days: int = Query(None, title="Last Modified in N Days"),
    db: Session = Depends(get_db)
):
    """
    Fetch CVE details with optional filters:
    - `cve_id`: Filter by CVE ID
    - `year`: Filter CVEs from a specific year
    - `min_score`, `max_score`: Filter by CVSS base score
    - `last_modified_days`: Fetch CVEs modified within the last N days
    """
    query = db.query(CVEEntry)

    if cve_id:
        query = query.filter(CVEEntry.cve_id == cve_id)
    
    if year:
        query = query.filter(CVEEntry.published_date.like(f"{year}%"))
    
    if min_score is not None and max_score is not None:
        query = query.filter(CVEEntry.cvss_score.between(min_score, max_score))
    
    if last_modified_days:
        date_limit = datetime.utcnow() - timedelta(days=last_modified_days)
        query = query.filter(CVEEntry.last_modified_date >= date_limit)

    cves = query.all()
    
    if not cves:
        raise HTTPException(status_code=404, detail="No CVEs found for the given filters.")

    return {"total_records": len(cves), "cves": cves}
