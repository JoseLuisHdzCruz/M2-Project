from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar el modelo entrenado y el escalador
model = joblib.load('modelo_speed_internet.pkl')
scaler = joblib.load('standard_scaler.pkl')

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos enviados en el request (JSON)
        data = request.get_json()

        Download_speed = float(data['Download_speed'])
        Network_congestion = float(data['Network_congestion'])
        Connection_type_Fiber = float(data['Connection_type_Fiber'])
        Connection_type_Cable = float(data['Connection_type_Cable'])
        # Connection_type_DSL = float(data['Connection_type_DSL'])

        # Escalar los datos de entrada
        input_data = [[Download_speed, Network_congestion, Connection_type_Fiber, Connection_type_Cable, ]]
        scaled_data = scaler.transform(input_data)
        
        # Crear un DataFrame con los datos escalados
        data_df = pd.DataFrame(scaled_data, columns=['Download_speed', 'Network_congestion', 'Connection_type_Fiber', 'Connection_type_Cable'])
        
        # Imprimir el DataFrame para verificar los datos
        print("Datos recibidos (escalados):")
        print(data_df)
        
        # Realizar la predicción
        prediction = model.predict(data_df)[0]
        
        # Devolver la predicción como respuesta JSON
        return jsonify({'Internet_speed': prediction})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
