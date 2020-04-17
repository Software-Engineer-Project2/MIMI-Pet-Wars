from hospitalapp import app
if __name__ == '__main__':
    app.debug = True
    app.run(port='1234',debug = True)