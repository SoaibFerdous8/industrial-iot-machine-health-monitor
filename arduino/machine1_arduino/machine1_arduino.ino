#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <DHT.h>

// ── Change these three lines ──────────────────────
const char* WIFI_SSID     = "Vodafone-32B0";
const char* WIFI_PASSWORD = "x9GPNyLJ2NXY3kC9";
const char* MQTT_SERVER   = "192.168.0.134";
// ─────────────────────────────────────────────────

#define DHT_PIN  7
#define DHT_TYPE DHT11
#define MQ2_PIN  A0

DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

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
    if (mqtt.connect("Arduino_Machine1")) {
      Serial.println(" Connected!");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  dht.begin();
  connectWiFi();
  mqtt.setServer(MQTT_SERVER, 1883);
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();
  int   gas  = analogRead(MQ2_PIN);

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT11 read failed!");
    delay(2000);
    return;
  }

  char tempStr[8], humStr[8], gasStr[6];
  dtostrf(temp, 5, 1, tempStr);
  dtostrf(hum,  5, 1, humStr);
  itoa(gas, gasStr, 10);

  mqtt.publish("factory/machine1/temperature", tempStr);
  mqtt.publish("factory/machine1/humidity",    humStr);
  mqtt.publish("factory/machine1/gas",         gasStr);

  Serial.print("Temp: "); Serial.print(tempStr);
  Serial.print(" | Hum: "); Serial.print(humStr);
  Serial.print(" | Gas: "); Serial.println(gasStr);

  delay(5000);
}