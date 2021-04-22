from app import create_app

app = create_app()

if __name__=='__main__':
    
    # Start the webserver
    app.run(debug=True)