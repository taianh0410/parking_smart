Smart Parking System

This IoT project uses a Raspberry Pi 3 B+ to manage an automated parking lot with a mechanism to prevent miscounting.

Features

- Automatic gate opening/closing upon card swipe
- Ultrasonic vehicle detection
- **State Machine (Anti-false counting)** - Vehicles must pass completely before being counted
- Real-time monitoring of available spaces
- LED indicator for full parking status
- Web Dashboard displaying status

GPIO Connection Diagram

Device - GPIO Pin
Servo (Barrier) - GPIO 6
Ultrasonic TRIGGER - GPIO 15
Ultrasonic ECHO - GPIO 4
IR Sensor - GPIO 22
Status LED - GPIO 13
Push Button - GPIO 21

Code Architecture (OOP)

SmartParkingSystem
├── GateController ├── ParkingLotManager ├── ParkingSlot └── WebDashboard ```

State Machine (Anti-false counting) Incorrect)
IDLE → GATE_OPENING → WAITING_ENTRY → VEHICLE_IN_ZONE → WAITING_EXIT → GATE_CLOSING → IDLE

**Logic to prevent incorrect counting:**
1. The vehicle must enter the sensor area (WAITING_ENTRY → VEHICLE_IN_ZONE)
2. Then exit the sensor area (VEHICLE_IN_ZONE → WAITING_EXIT)

3. Only then will it be counted as a valid entry.

**Cases NOT counted:**

- Vehicle enters and then reverses out → NO increase in vehicle count

Student Project

- Project: Smart Parking Lot

- Platform: Raspberry Pi 3 B+

- Language: Python 3

- Libraries: gpiozero, Flask

## License

Learning Project - Free for educational purposes
