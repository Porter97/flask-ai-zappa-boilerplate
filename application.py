import os
import sys

import click
from dotenv import load_dotenv
from flask_migrate import Migrate


from app import create_app, db


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'DEV')
migrate = Migrate(app, db)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    test_results = unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

    if test_results.wasSuccessful():
        exit(0)
    else:
        exit(1)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


@app.cli.command()
def init_opensearch():
    from app.utils.opensearch_utils.indices import create_index
    from app.utils.opensearch_utils.indices.templates.document_index import create_document_index_template
    from app.utils.opensearch_utils.indices.templates.chat_history_index import create_chat_history_index_template
    from app.utils.opensearch_utils.session import opensearch_session

    indices = [{
        'index_name': os.environ.get('DOCUMENT_INDEX'),
        'template': create_document_index_template()
    }, {
        'index_name': os.environ.get('CHAT_HISTORY_INDEX'),
        'template': create_chat_history_index_template()
    }]

    try:
        es = opensearch_session()
    except Exception as e:
        print('Failed to initialize OpenSearch')
        print(e)
        return 1

    for index in indices:
        if not es.indices.exists(index=index['index_name']):
            create_index(es, index['template'])

    print('OpenSearch initialized successfully')

    return 0


