*** This is a work in progress ***

# Simons-Trilobot
## Simons @pimoroni Trilobot robot

### Loaded with:
- I2C [PA1010D GPS Module](https://shop.pimoroni.com/products/pa1010d-gps-breakout?variant=32257258881107)
- I2C [LSM303D accelerometer and compass](https://shop.pimoroni.com/products/lsm303d-6dof-motion-sensor-breakout?variant=12767623151699)
- I2C [vl53l5cx 8*8 TOF ranger](https://shop.pimoroni.com/products/vl53l5cx-time-of-flight-tof-sensor-breakout?variant=39972903059539)
- I2C [5*5 RGB LED Matrix Display](https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout?variant=21375941279827)
- I2C [11*7 LED Matrix Display](https://shop.pimoroni.com/products/11x7-led-matrix-breakout?variant=21791690752083)	
- I2C [BME680 Enviromental Monitor](https://shop.pimoroni.com/products/bme680-breakout?variant=12491552129107) 
- Rear facing SN-04 ultrasonic ranger (moved from front) under development
- Front Facing [8mp Camera](https://shop.pimoroni.com/products/raspberry-pi-camera-module-v2?variant=19833929735)
- Servo with **_spining Santa_**
 
### Using the following core software:
- Python 3
- Flask
- HTML5 + CSS
- Javascript
- MariaDB
- picamera2

### Providing the following key functions:
- **trilobotWebApp.py**
  - Web based 'Point of View' driving using camera and on page controls
    - Python, Flask, HTML5+CSS, Javascript, MariaDb
- **trilobotMot.py**
  - [8BitDo Zero Bluetooth Game Controller](https://shop.pimoroni.com/products/8bitdo-zero-2-bluetooth-gamepad?variant=31339051384915) driving
    - Python
- **trilobotEnv.py**
  - Enviromental and Posistional data collection and storage
    - Python, MariaDB
    - started at boot by cron
- **trilobotMJPEG-server.py**
  - Camera Streaming for web based driving 
    - picamera2
    - started at boot by cron

