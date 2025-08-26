from flask import Flask, request, jsonify
from models.diet import Diet
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3306/diet-crud-api"
db.init_app(app)

@app.route('/diet', methods=['POST'])
def create_diet():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    is_diet = data.get('is_diet')
    
    if name and description and date:
        diet = Diet(name=name, description=description, date=date, is_diet=is_diet)
        db.session.add(diet)
        db.session.commit()
        return jsonify({"message":"Refeição cadastrada com sucesso"})
    
    return jsonify({"message":"Credenciais inválidas"})

@app.route('/diet/<int:id>', methods=['PUT'])
def update_diet(id):
    data = request.get_json()
    diet = Diet.query.get(id)

    if diet:
        if 'name' in data:
            diet.name = data['name']
        if 'description' in data:
            diet.description = data['description']
        if 'date' in data:
            diet.date = data['date']
        if 'is_diet' in data:
            diet.is_diet = data['is_diet']

        db.session.commit()

        return jsonify({"message":"Refeição alterada com sucesso"})
    
    return jsonify({"message":"Refeição não encontrada"}), 404  

@app.route('/diet/<int:id>', methods=['DELETE'])
def delete_diet(id):
    diet = Diet.query.get(id)

    if diet:
        db.session.delete(diet)
        db.session.commit()
        return jsonify({"message":"Refeição deletada com sucesso"})

    return jsonify({"message":"Refeição não encontrada"}), 404  

@app.route('/diet', methods=['GET'])
def get_diet():
    diets = Diet.query.all()
    result = []
    if diets:
        for diet in diets:
            result.append(
                {
                    "id": diet.id,
                    "refeição": {
                        "name": diet.name,
                        "description": diet.description,
                        "date": diet.date,
                        "is_diet": diet.is_diet
                    }
                }
            )
        return jsonify(result)
    return jsonify({"message":"Nenhuma refeição cadastrada"})

@app.route('/diet/<int:id>', methods=['GET'])
def get_diet_by_id(id):
    diet = Diet.query.get(id)

    if diet:
        return {
            "name": diet.name,
            "description": diet.description,
            "date": diet.date,
            "is_diet": diet.is_diet
        }
    return jsonify({"message":"Refeição não encontrada"})

if __name__ == '__main__':
    app.run(debug=True)