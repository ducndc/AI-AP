# 1. Import thư viện
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 2. Tạo dữ liệu giả lập (bạn thay bằng dữ liệu thực nếu có)
data = {
    'RSSI': [-65, -70, -55, -60, -75, -68, -66, -72, -59, -63],
    'TX_Rate': [150, 120, 200, 180, 100, 130, 140, 110, 190, 170],
    'RX_Rate': [140, 110, 180, 170, 90, 125, 135, 105, 175, 165],
    'Packet_Loss': [2, 5, 0, 1, 10, 3, 2, 6, 1, 2],
    'Latency': [10.5, 12.0, 8.0, 9.0, 15.0, 11.0, 10.0, 13.0, 8.5, 9.5],
    'Link_Quality': [85, 75, 90, 80, 60, 78, 82, 70, 88, 83]
}

df = pd.DataFrame(data)

# 3. Tách input (X) và output (y)
X = df[['RSSI', 'TX_Rate', 'RX_Rate', 'Packet_Loss', 'Latency']]
y = df['Link_Quality']

# 4. Chia train/test và chuẩn hóa dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 5. Xây dựng mô hình MLP đơn giản
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)  # Hồi quy 1 giá trị Link_Quality
])

# 6. Compile và huấn luyện mô hình
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=100, batch_size=8, validation_data=(X_test, y_test))

# 7. Đánh giá mô hình
loss = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}')

# 8. Chuyển mô hình sang TensorFlow Lite + Quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Áp dụng quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Chuyển đổi mô hình
tflite_quant_model = converter.convert()

# 9. Lưu file .tflite
with open('mesh_link_quality_model_quantized.tflite', 'wb') as f:
    f.write(tflite_quant_model)

print("✅ Đã lưu mô hình TFLite (quantized) thành công!")

# 10. (Optional) Kiểm tra mô hình TFLite sau khi convert
interpreter = tf.lite.Interpreter(model_path="mesh_link_quality_model_quantized.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test dữ liệu mới (dữ liệu chuẩn hóa như lúc train)
sample_input = np.array([[-65, 150, 140, 2, 10.5]])
sample_input = scaler.transform(sample_input).astype(np.float32)

interpreter.set_tensor(input_details[0]['index'], sample_input)
interpreter.invoke()
predicted_output = interpreter.get_tensor(output_details[0]['index'])

print(f'Predicted Link Quality (quantized model): {predicted_output[0]}')

