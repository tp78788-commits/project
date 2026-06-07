#include <WiFi.h>
#include <PubSubClient.h>

// --- CẤU HÌNH WIFI & MQTT ---
const char* ssid = "MERCUSYS_19F8";       // Điền tên WiFi
const char* password = "22324672";      // Điền mật khẩu WiFi
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_topic = "do_an_dung/dieukhien_den";

WiFiClient espClient;
PubSubClient client(espClient);

// --- KHAI BÁO CHÂN PHẦN CỨNG ---
const int DEN_PIN = 26;     
const int DONGCO_PIN = 27;   

// Hàm kết nối WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Dang ket noi vao WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi da ket noi thanh cong!");
}

// Hàm nhận lệnh từ MQTT 
void callback(char* topic, byte* payload, unsigned int length) {
  // Biến mảng byte thành chuỗi String 
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Nhan duoc lenh tu AI: [ ");
  Serial.print(message);
  Serial.println(" ]");

  // --- XỬ LÝ ĐÓNG CẮT PHẦN CỨNG THEO LỆNH ---
  if (message == "L1_ON") {
    digitalWrite(DEN_PIN, HIGH);   // Bật đèn
    Serial.println("=> Thuc thi: BAT DEN");
    
  } else if (message == "L1_OFF") {
    digitalWrite(DEN_PIN, LOW);    // Tắt đèn
    Serial.println("=> Thuc thi: TAT DEN");
    
  } else if (message == "M1_ON") {
    digitalWrite(DONGCO_PIN, HIGH); // Bật động cơ
    Serial.println("=> Thuc thi: BAT DONG CO");
    
  } else if (message == "M1_OFF") {
    digitalWrite(DONGCO_PIN, LOW);  // Tắt động cơ
    Serial.println("=> Thuc thi: TAT DONG CO");
    
  } else if (message == "OFF_ALL") {
    digitalWrite(DEN_PIN, LOW);     // Tắt hết
    digitalWrite(DONGCO_PIN, LOW);  
    Serial.println("=> Thuc thi: DUNG KHAN CAP - TAT TOAN BO");
    
  } else if (message == "WAIT") {
    // Chế độ chờ: Không làm gì cả hoặc bạn có thể nháy đèn LED nhỏ trên board để báo hiệu
    Serial.println("=> Thuc thi: CHE DO CHO");
  }
}

// Hàm tự động kết nối lại nếu rớt mạng
void reconnect() {
  while (!client.connected()) {
    Serial.print("Dang ket noi MQTT...");
    // Đặt tên bất kỳ cho Client ID, ví dụ "ESP32Client_Dung123"
    if (client.connect("ESP32Client_Dung123")) {
      Serial.println(" Da ket noi!");
      // Phải ĐĂNG KÝ hộp thư 
      client.subscribe(mqtt_topic);
    } else {
      Serial.print(" That bai, ma loi: ");
      Serial.print(client.state());
      Serial.println(" Thu lai sau 5 giay.");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // Cài đặt các chân tín hiệu là chân xuất (OUTPUT)
  pinMode(DEN_PIN, OUTPUT);
  pinMode(DONGCO_PIN, OUTPUT);
  
  // Trạng thái ban đầu: Tắt mọi thứ 
  digitalWrite(DEN_PIN, LOW);
  digitalWrite(DONGCO_PIN, LOW);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback); // Gắn hàm xử lý khi có thư đến
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  // Duy trì kết nối liên tục để hóng tin nhắn
  client.loop(); 
  
  // Cho CPU nghỉ ngơi 50 mili-giây sau mỗi vòng lặp để hạ nhiệt ESP32
  delay(50); 
}