import cv2
import mediapipe as mp
import csv

# Khởi tạo thư viện nhận diện bàn tay MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# File nạp dữ 
csv_file = r"F:\code\data_6_cuchi.csv"

print("--- HƯỚNG DẪN THU THẬP DỮ LIỆU 6 CỬ CHỈ ---")
print("Giơ tay vào khung hình và bấm giữ các phím số sau để lưu tọa độ:")
print("[ 0 ] - Tắt toàn bộ hệ thống (Nắm đấm)")
print("[ 1 ] - Bật đèn (Giơ 1 ngón)")
print("[ 2 ] - Tắt đèn (Giơ 2 ngón)")
print("[ 3 ] - Bật động cơ (Giơ 3 ngón)")
print("[ 4 ] - Tắt động cơ (Giơ 4 ngón)")
print("[ 5 ] - Chế độ chờ / Chuyển đổi (Giơ 5 ngón)")
print("[ Q ] - Thoát chương trình")
print("--------------------------------------------")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Lật ảnh cho giống gương và chuyển hệ màu
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Đọc phím bấm từ bàn phím
    key = cv2.waitKey(1) & 0xFF
    
    # Thoát nếu bấm phím 'q'
    if key == ord('q'): 
        break

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Vẽ khung xương tay lên màn hình
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # khai báo các phím 
            if key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                label = int(chr(key)) # Chuyển phím bấm thành số nhãn (0 -> 5)
                
                # Rút trích 63 tọa độ (x, y, z của 21 khớp)
                data_row = []
                for lm in hand_landmarks.landmark:
                    data_row.extend([lm.x, lm.y, lm.z])
                
                # Thêm nhãn vào cột cuối cùng và ghi vào file CSV
                data_row.append(label)
                with open(csv_file, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_row)
                
                print(f"Đã lưu tọa độ cho cử chỉ: {label}")

    # Hiển thị lên màn hình camera
    cv2.putText(frame, "GIO TAY VA BAM CAC PHIM: 0,1,2,3,4,5", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, "BAM 'Q' DE THOAT", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow("Thu thap du lieu (6 Cu chi)", frame)

cap.release()
cv2.destroyAllWindows()
