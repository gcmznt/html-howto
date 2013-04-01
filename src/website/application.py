import os
import sys
from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_frozen import Freezer


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

app = Flask(
    import_name=__name__,
    static_folder=os.path.join(SITE_ROOT, '..', '..', 'static'),
    template_folder=os.path.join(SITE_ROOT, '..', '..', 'templates'),
)

assets = Environment(app)
assets.manifest = False
assets.cache = False
assets.debug = True

freezer = Freezer(app)

app.config.update(
    DEBUG=True,
    FREEZER_DESTINATION=os.path.join(SITE_ROOT, '..', '..', 'build')
)


assets.register('js_all', Bundle(
    'js/website.js',
    filters='jsmin',
    output='build/website.js'
))
assets.register('css_all', Bundle(
    'css/website.less',
    filters='less, cssutils',
    output='build/website.css'
))


@app.route('/')
def homepage():
    return render_template('homepage.html')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        assets.debug = False
        freezer.freeze()
    else:
        app.run('0.0.0.0')
