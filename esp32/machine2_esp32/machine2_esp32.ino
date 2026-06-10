#include <WiFi.h>
#include <PubSubClient.h>

// ── Change these three lines ──────────────────────
const char* WIFI_SSID     = "Vodafone-32B0";
const char* WIFI_PASSWORD = "x9GPNyLJ2NXY3kC9";
const char* MQTT_SERVER   = "192.168.0.134";
// ─────────────────────────────────────────────────

#define KY038_PIN  34
#define KY002_PIN  27

WiFiClient espClient;
PubSubClient mqtt(espClient);

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect("ESP32_Machine2")) {
      Serial.println(" Connected!");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(KY002_PIN, INPUT);
  connectWiFi();
  mqtt.setServer(MQTT_SERVER, 1883);
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  int sound     = analogRead(KY038_PIN);
  int vibration = digitalRead(KY002_PIN);
  int shock     = (vibration == LOW) ? 1 : 0;

  char soundStr[10], vibStr[4];
  itoa(sound, soundStr, 10);
  itoa(shock, vibStr, 10);

  mqtt.publish("factory/machine2/sound",     soundStr);
  mqtt.publish("factory/machine2/vibration", vibStr);

  Serial.print("Sound: "); Serial.print(sound);
  Serial.print(" | Vibration: ");
  Serial.println(shock ? "SHOCK DETECTED" : "stable");

  delay(2000);
}