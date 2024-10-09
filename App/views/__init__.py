# blue prints are imported 
# explicitly instead of using *
from .auth import auth_views
from .index import index_views
from .listing import listing_views
from .application import application_views
from .job import job_views


views = [auth_views, index_views, listing_views, application_views, job_views] 
# blueprints must be added to this list