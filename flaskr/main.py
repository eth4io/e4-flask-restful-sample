from flaskr.app import app


if __name__ == '__main__':
    app.run(debug = True, ssl_context = ('credentials/ssl.crt', 'credentials/ssl.key'))
