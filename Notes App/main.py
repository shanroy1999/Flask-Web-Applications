from website import create_app

app = create_app()

# only run the web server when the main.py file runs
if __name__=='__main__':
    app.run(debug=True)             # if changes done in python code => automatically refresh server
