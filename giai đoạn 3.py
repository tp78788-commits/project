import cv2
import mediapipe as mp
import numpy as np
from keras.models import load_model
import paho.mqtt.client as mqtt 

# --- 1. CẤU HÌNH TRẠM BƯU ĐIÊN MQTT ---
MQTT_BROKER = "broker.hivemq.com"   
MQTT_PORT = 1883
MQTT_TOPIC = "do_an_dung/dieukhien_den" # Hộp thư riêng 

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start() 
print("Đã kết nối thành công tới trạm trung chuyển HiveMQ!")

# --- 2. NẠP MÔ HÌNH AI & QUY ƯỚC LỆNH ---
model = load_model(r"F:\code\mo_hinh_dnn_6_cuchi.h5")

# Ánh xạ nhãn hiển thị trên màn hình
labels_mapping = {
    0: "TAT HE THONG", 1: "BAT DEN", 2: "TAT DEN", 
    3: "BAT DONG CO", 4: "TAT DONG CO", 5: "CHE DO CHO"
}

# Quy ước mã lệnh để gửi xuống ESP32 
payload_mapping = {
    0: "OFF_ALL", 1: "L1_ON", 2: "L1_OFF", 
    3: "M1_ON", 4: "M1_OFF", 5: "WAIT"
}

# --- 3. KHỞI TẠO CAMERA & MEDIAPIPE ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
current_state = "" # Biến nhớ trạng thái cũ để không gửi lệnh trùng liên tục

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
        
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            data_row = []
            for lm in hand_landmarks.landmark:
                data_row.extend([lm.x, lm.y, lm.z])
            
            input_data = np.array([data_row])
            prediction = model.predict(input_data, verbose=0)
            class_id = np.argmax(prediction)
            confidence = prediction[0][class_id]
            
            if confidence > 0.85:
                gesture = labels_mapping[class_id]
                payload = payload_mapping[class_id]
                
                # NẾU TRẠNG THÁI THAY ĐỔI -> MỚI BẮN LỆNH LÊN MQTT
                if gesture != current_state:
                    current_state = gesture
                    mqtt_client.publish(MQTT_TOPIC, payload)
                    print(f"-> Đã gửi lệnh: [ {payload} ] lên MQTT")
                        
                cv2.putText(frame, f"{gesture} ({confidence*100:.1f}%)", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Khong ro cu chi...", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
    cv2.imshow("He thong dieu khien (Co MQTT)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
mqtt_client.loop_stop()