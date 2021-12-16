from website import create_app  # min 10

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # run a flask application.
