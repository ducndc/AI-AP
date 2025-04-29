import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Dữ liệu giả lập
data = {
    'RSSI': [-65, -70, -55, -60, -75, -68, -66, -72, -59, -63],
    'Clients_on_AP': [5, 12, 3, 8, 15, 7, 6, 11, 4, 9],
    'LinkRate': [300, 150, 400, 350, 120, 180, 250, 130, 370, 340],
    'Latency': [10, 20, 5, 8, 30, 15, 9, 25, 6, 10],
    'Loss': [1, 5, 0, 2, 10, 3, 2, 6, 1, 2],
    'Band': [5, 5, 5, 5, 2, 5, 5, 2, 5, 5], # 2.4GHz or 5GHz
    'AP_CPU_Load': [30, 50, 25, 40, 70, 45, 35, 60, 28, 38],
    'AP_Mem_Load': [40, 60, 30, 50, 80, 55, 45, 65, 35, 48],
    'Suitability_Score': [0.9, 0.6, 0.95, 0.85, 0.4, 0.7, 0.88, 0.5, 0.92, 0.87]
}

df = pd.DataFrame(data)

# 2. Chuẩn bị dữ liệu
X = df[['RSSI', 'Clients_on_AP', 'LinkRate', 'Latency', 'Loss', 'Band', 'AP_CPU_Load', 'AP_Mem_Load']]
y = df['Suitability_Score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. Tạo mô hình MLP
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(8,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)  # Output suitability score
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=8, validation_data=(X_test, y_test))

# 4. Convert sang TFLite quantized
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('client_steering_model_quantized.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ Mô hình client steering đã lưu thành công!")

