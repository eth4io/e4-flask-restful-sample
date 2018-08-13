from app import app
from werkzeug.serving import make_ssl_devcert
from OpenSSL import SSL


if __name__ == '__main__':
    app.run(debug = True, ssl_context = ('credentials/ssl.crt', 'credentials/ssl.key'))
