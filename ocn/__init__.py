from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from ocn.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    config = Configurator(settings=settings)
    config.add_static_view('static', 'ocn:static')

    # Homepage route
    config.add_route('home', '/')
    config.add_view('ocn.views.view_home', route_name='home',
                    renderer='ocn:templates/home.pt')

    # Routes for subject list page
    config.add_route('subject_list', '/subjects')
    config.add_view('ocn.views.view_subject_list', route_name='subject_list',
                    renderer='ocn:templates/sublist.pt')

    # Routes for section list pages
    config.add_route('subject_index', '/subjects/{subjectcode}')
    config.add_view('ocn.views.view_subject_index', route_name='subject_index',
                    renderer='ocn:templates/sectionlist.pt')

    # Routes for section pages
    config.add_route('section', '/subjects/{subjectcode}/{sectionurlname}')
    config.add_view('ocn.views.view_section', route_name='section',
                    renderer='ocn:templates/sectiontemplate.pt')

    # If comments are eventually loaded by jQuery, a separate route and view
    # will be necessary.
    #
    ## Routes for comments
    #config.add_route('comments', '/subjects/{subjectcode}/{sectionurlname}/{paragraphid}')
    #config.add_view('ocn.views.view_comments', route_name='comments')

    return config.make_wsgi_app()
