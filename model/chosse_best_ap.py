import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib  # Dùng để load scaler nếu cần

# 1. Load mô hình đã quantized
interpreter = tf.lite.Interpreter(model_path="client_steering_model_quantized.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 2. Giả lập scaler (bạn thay bằng scaler đã lưu lúc train nếu cần)
# (Ở đây tôi giả lập bằng StandardScaler huấn luyện tay, bạn nên load scaler chuẩn)
scaler = StandardScaler()
# Fit giả lập scaler với các giá trị trung bình -65 RSSI, 200 linkrate, etc. cho khớp
scaler.mean_ = np.array([-65, 8, 250, 15, 3, 4, 40, 50])
scaler.scale_ = np.array([5, 3, 80, 5, 3, 1.5, 15, 20])

# 3. Tạo dữ liệu các AP khả dụng
ap_features = np.array([
    [-65, 5, 300, 10, 1, 5, 30, 40],  # AP1
    [-72, 8, 180, 20, 3, 5, 40, 55],  # AP2
    [-60, 10, 200, 15, 5, 2, 35, 45]  # AP3
], dtype=np.float32)

# 4. Chuẩn hóa dữ liệu đầu vào
ap_features_scaled = scaler.transform(ap_features)

# 5. Inference từng AP
scores = []
for ap in ap_features_scaled:
    input_data = np.expand_dims(ap, axis=0).astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    scores.append(output_data[0][0])

# 6. Chọn AP có score cao nhất
best_ap_index = np.argmax(scores)
print(f"✅ AP tốt nhất cho client: AP{best_ap_index + 1}")
print(f"Scores: {scores}")

