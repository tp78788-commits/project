Đồ án: Hệ thống điều khiển thiết bị điện IoT qua nhận dạng cử chỉ bàn tay 

Sinh viên thực hiện: Phạm Sỹ Dũng
Chuyên ngành: Kỹ thuật Robot và Trí tuệ nhân tạo - Trường Đại học Mỏ - Địa chất

  Giới thiệu (Introduction)
Dự án ứng dụng Machine Learning (Deep Neural Network - DNN) kết hợp với thư viện MediaPipe để nhận dạng 6 trạng thái cử chỉ bàn tay theo thời gian thực (Real-time). Thông qua giao thức mạng không dây MQTT, hệ thống truyền lệnh từ trạm AI (Máy tính) xuống vi điều khiển ESP32 để đóng ngắt các thiết bị vật lý (Đèn LED, Động cơ DC) một cách tự động mà không cần chạm vật lý.

Dự án cũng tích hợp tính năng Điều khiển bằng giọng nói (Voice Control) để tạo ra một hệ thống giao tiếp đa phương thức (Multimodal HMI).

 Yêu cầu hệ thống & Cài đặt thư viện (Requirements)
Để chạy được mã nguồn của dự án này, máy tính cần cài đặt Python và các thư viện hỗ trợ xử lý ảnh, AI và IoT. 
Mở Terminal / Command Prompt và chạy lệnh sau để cài đặt toàn bộ:
Thư viện cần cài đặt là : paho-mqtt,pandas,numpy,opencv-python,mediapipe,tensorflow
