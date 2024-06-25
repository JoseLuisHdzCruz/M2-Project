# from flask import Flask, request, render_template, jsonify
# import joblib
# import pandas as pd
# import logging
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense

# app = Flask(__name__)

# # Configurar el registro
# logging.basicConfig(level=logging.DEBUG)

# # Definir la función create_model
# def create_model():
#     model = Sequential()
#     model.add(Dense(64, input_dim=4, activation='relu'))  # Ajusta input_dim según tus datos
#     model.add(Dense(32, activation='relu'))
#     model.add(Dense(1, activation='linear'))
#     model.compile(optimizer='adam', loss='mse', metrics=['mae'])
#     return model

# # Cargar el modelo entrenado y el escalador
# model = joblib.load('model_nl.pkl')
# scaler = joblib.load('scaler.pkl')  # Cargar el escalador
# app.logger.debug('Modelo y escalador cargados correctamente.')

# @app.route('/')
# def home():
#     return render_template('formulario.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Obtener los datos enviados en el request
#         data = request.get_json()
#         app.logger.debug(f'Datos recibidos: {data}')
        
#         # Extraer y convertir los datos recibidos
#         Download_speed = float(data['Download_speed'])
#         Upload_speed = float(data['Upload_speed'])
#         Connection_type_Fiber = float(data['Connection_type_Fiber'])
#         Signal_strength = float(data['Signal_strength'])
        
#         # Crear un DataFrame con los datos
#         data_df = pd.DataFrame([[Download_speed, Upload_speed, Connection_type_Fiber, Signal_strength]], columns=['Download_speed', 'Upload_speed', 'Connection_type_Fiber', 'Signal_strength'])
#         app.logger.debug(f'DataFrame creado: {data_df}')
        
#         # Aplicar escalado a los datos
#         data_df_scaled = scaler.transform(data_df)
#         app.logger.debug(f'DataFrame escalado: {data_df_scaled}')
        
#         # Realizar predicciones
#         prediction = model.predict(data_df_scaled)
#         app.logger.debug(f'Predicción: {prediction[0]}')
        
#         # Devolver las predicciones como respuesta JSON
#         return jsonify({'Internet_speed': int(prediction[0])})
#     except Exception as e:
#         app.logger.error(f'Error en la predicción: {str(e)}')
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
import logging
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

app = Flask(__name__)

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

# Definir la función create_model (esto es solo un ejemplo)
def create_model():
    model = Sequential()
    model.add(Input(shape=([5])))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


# Cargar el modelo entrenado
model = joblib.load('model_nl.pkl')
app.logger.debug('Modelo cargado correctamente.')

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos enviados en el request
        data = request.get_json()
        app.logger.debug(f'Datos recibidos: {data}')
        
        # Extraer y convertir los datos recibidos
        Download_speed = float(data['Download_speed'])
        Upload_speed = float(data['Upload_speed'])
        Connection_type_Fiber = float(data['Connection_type_Fiber'])
        Signal_strength = float(data['Signal_strength'])
        # isMale = float(data['isMale'])
        # isBlack = float(data['isBlack'])
        # isHypertensive = float(data['isHypertensive'])
        # Cholesterol = float(data['Cholesterol'])
        # HDL = float(data['HDL'])
        
        # Crear un DataFrame con los datos
        data_df = pd.DataFrame([[Download_speed, Upload_speed, Connection_type_Fiber, Signal_strength]], columns=['Download_speed', 'Upload_speed', 'Connection_type_Fiber', 'Signal_strength'])

        # data_df = pd.DataFrame([[Age, Systolic, isDiabetic, isSmoker, isMale, isBlack, isHypertensive, Cholesterol, HDL]], columns=['Age', 'Systolic', 'isDiabetic', 'isSmoker', 'isMale', 'isBlack', 'isHypertensive', 'Cholesterol', 'HDL'])
        app.logger.debug(f'DataFrame creado: {data_df}')
        
        # Realizar predicciones
        prediction = model.predict(data_df)
        app.logger.debug(f'Predicción: {prediction[0]}')
        
        # Devolver las predicciones como respuesta JSON
        return jsonify({'Internet_speed': int(prediction[0])})
    except Exception as e:
        app.logger.error(f'Error en la predicción: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

