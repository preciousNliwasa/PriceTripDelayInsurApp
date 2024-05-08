from flask import Flask,request,url_for,redirect
from dashapp import create_dash_application

app = Flask(__name__)
create_dash_application(app)

@app.route('/',methods = ["GET","POST"])
def home():
    
    if request.method == 'GET':
    
        return redirect('/')

    else:
    
        return redirect('/')  
            
    

if __name__ == '__main__':
    app.run(debug=False)
