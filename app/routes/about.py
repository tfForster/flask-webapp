from flask import Blueprint, render_template
from app.models.timeline_event import TimelineEvent
from app.models.current_status import CurrentStatus
 
about = Blueprint('about', __name__)
 
 
@about.route('/')
def about_page():
    events = TimelineEvent.query.order_by(TimelineEvent.order.asc()).all()
    status = CurrentStatus.query.filter_by(is_active=True).first()
    return render_template('about.html', events=events, status=status)