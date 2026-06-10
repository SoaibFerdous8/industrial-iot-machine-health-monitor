# Industrial IoT Machine Health Monitoring System

A real-time machine health monitoring system built on Raspberry Pi 3, implementing predictive maintenance using industrial communication protocols and ML-based anomaly detection.

## Tech Stack
- **Protocols:** MQTT, OPC UA
- **Database:** InfluxDB 2.x (time-series)
- **Visualization:** Grafana (5-panel live dashboard)
- **ML:** Isolation Forest (scikit-learn) — unsupervised anomaly detection
- **Hardware:** Raspberry Pi 3, Arduino UNO WiFi Rev-2, ESP-32 DevKitC
- **Sensors:** DHT11, MQ-2, KY-038, KY-002

## Services (all auto-start on boot)
| Service | Description |
|---|---|
| mosquitto | MQTT broker on port 1883 |
| mqtt_bridge | Python MQTT to InfluxDB bridge |
| opcua_server | OPC UA server on port 4840 |
| anomaly_detection | Isolation Forest ML detection |
| grafana-server | Dashboard on port 3000 |
| influxdb | Time-series database |

## MQTT Topics
| Topic | Sensor | Machine |
|---|---|---|
| factory/machine1/temperature | DHT11 | Arduino |
| factory/machine1/humidity | DHT11 | Arduino |
| factory/machine1/gas | MQ-2 | Arduino |
| factory/machine2/sound | KY-038 | ESP-32 |
| factory/machine2/vibration | KY-002 | ESP-32 |

## Course Context
Advanced Embedded Systems Lab — Industrial Communications Standards
Bachelor of Engineering, Semester 6
