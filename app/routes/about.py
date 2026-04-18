from flask import Blueprint, render_template
from app.models.timeline_event import TimelineEvent

about = Blueprint('about', __name__)


@about.route('/')
def about_page():
    events = TimelineEvent.query.order_by(TimelineEvent.order.asc()).all()
    return render_template('about.html', events=events)