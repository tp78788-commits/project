import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Input
from keras.callbacks import ModelCheckpoint # <--  THƯ VIỆN BẢO HIỂM 

# 1. Đọc dữ liệu từ file CSV 6 cử chỉ
df = pd.read_csv("data_6_cuchi.csv", header=None)

# Tách biến độc lập X (63 tọa độ) và nhãn Y (cột cuối cùng)
X = df.iloc[:, :-1].values
Y = df.iloc[:, -1].values

# Chia dữ liệu thành 80% để Train và 20% để Test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 2. Xây dựng cấu trúc mạng DNN
model = Sequential([
    Input(shape=(63,)),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(6, activation='softmax') 
])

# 3. Biên dịch mô hình
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 4. Huấn luyện mô hình (CÓ BẢO HIỂM)
print("Bắt đầu huấn luyện mạng DNN 6 Cử chỉ...")

# Tạo chốt chặn: Chỉ lưu mô hình khi độ chính xác kiểm tra (val_accuracy) tăng lên
checkpoint = ModelCheckpoint(r"F:\code\mo_hinh_dnn_6_cuchi.h5", 
                             monitor='val_accuracy', 
                             save_best_only=True, 
                             mode='max', 
                             verbose=1)

history = model.fit(
    X_train, Y_train,
    epochs=40,               
    batch_size=64,           
    validation_data=(X_test, Y_test),
    callbacks=[checkpoint]  #Gắn chốt chặn vào quá trình học
)

# 5. Đánh giá kiểm tra sai số trên tập Test
test_loss, test_acc = model.evaluate(X_test, Y_test)
print(f"\nĐộ chính xác trung bình trên tập Test: {test_acc * 100:.2f}%")
print("Quá trình huấn luyện hoàn tất! File 'mo_hinh_dnn_6_cuchi.h5' đã sẵn sàng.")