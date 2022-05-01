import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
@click.option('--length', default=25, help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None, help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """在代码分析器下启动应用程序"""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    if __name__ == '__main__':
        app.run(debug=False)