from flask import Flask, request, jsonify
from models.diet import Diet
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3307/diet-crud-api"
db.init_app(app)


@app.route('/diet', methods=['POST'])
def create_diet():
    data = request.json()
    name = data.get('name')
    description = data.get('description')
    date = data.get('description')
    is_diet = data.get('is_diet')

    if name and description and date and is_diet:
        diet = Diet(name, description, date, is_diet)
        db.session.add(diet)
        db.session.commit()
        return jsonify({"message":"Refeição cadastrada com sucesso"})
    
    return jsonify({"message":"Credenciais inválidas"})




if __name__ == '__main__':
    app.run(debug=True)