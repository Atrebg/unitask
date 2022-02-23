from website import create_app  # min 10

app = create_app()
# SQLALCHEMY_TRACK_MODIFICATIONS = False

if __name__ == '__main__':
    app.run(debug=True)  # run a flask application.
