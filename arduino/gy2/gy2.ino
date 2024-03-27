#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
double pitch, roll;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  mpu.initialize();

  // Configura il sensore MPU6050 con il filtro passa-basso a 4Hz
  mpu.setDLPFMode(2);
}

void loop() {
  // Ottieni i dati grezzi da accelerometro e giroscopio
  int16_t accX = mpu.getAccelerationX();
  int16_t accY = mpu.getAccelerationY();
  int16_t accZ = mpu.getAccelerationZ();

  int16_t gyroX = mpu.getRotationX();
  int16_t gyroY = mpu.getRotationY();
  int16_t gyroZ = mpu.getRotationZ();
  

  getAngle(accX, accY, accZ);
  // Stampa i dati sulla porta seriale
  Serial.print(pitch);
  Serial.print(", ");
  Serial.print(roll);
  Serial.print(", ");
  Serial.print(accX);
  Serial.print(", ");
  Serial.print(accY);
  Serial.print(", ");
  Serial.print(accZ);
  Serial.print(" , ");
  Serial.print(gyroX);
  Serial.print(", ");
  Serial.print(gyroY);
  Serial.print(", ");
  Serial.println(gyroZ);
}

void getAngle(int Ax, int Ay, int Az) {
  double x = Ax;
  double y = Ay;
  double z = Az;
  pitch = atan(x / sqrt((y * y) + (z * z)));
  roll = atan(y / sqrt((x * x) + (z * z)));
  pitch = pitch * (180.0 / 3.14);
  roll = roll * (180.0 / 3.14);
}
