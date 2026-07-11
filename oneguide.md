ESP8266 Practical Activities
This file has simple, easy to understand codes for basic ESP8266 activities.
Covers: `digitalWrite()`, `digitalRead()`, and `analogRead()` / `analogWrite()` functions.
---
Activity 1: Single LED Blinking
Description:
This is the most basic program. We are just turning one LED ON and OFF with some delay in between. This uses `digitalWrite()` function.
```cpp
#define LED 2   // GPIO2 (D4 on NodeMCU)

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, LOW);   // LED ON (active low)
  delay(1000);
  digitalWrite(LED, HIGH);  // LED OFF
  delay(1000);
}
```
---
Activity 2: Two LED Blinking (Alternate)
Description:
Here we take two LEDs and make them blink alternately, means when one is ON the other is OFF. Both are controlled using `digitalWrite()`.
```cpp
#define LED1 4   // D2
#define LED2 5   // D1

void setup() {
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
}

void loop() {
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, LOW);
  delay(1000);

  digitalWrite(LED1, LOW);
  digitalWrite(LED2, HIGH);
  delay(1000);
}
```
---
Activity 3: Single LED Blinking 10 Times Faster
Description:
This is same as activity 1, but delay time is reduced to 1/10th, so LED blinks 10 times faster than normal.
```cpp
#define LED 4   // D2

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(100);     // 1000/10 = 100 ms
  digitalWrite(LED, LOW);
  delay(100);
}
```
---
Activity 4: Unlimited Time Slow Blinking
Description:
This LED blinks very slowly and keeps running forever (unlimited) since it is inside `loop()`. We just increase the delay value to make it slow.
```cpp
#define LED 4   // D2

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(5000);    // 5 seconds ON
  digitalWrite(LED, LOW);
  delay(5000);    // 5 seconds OFF
}
```
---
Activity 5: IR Sensor with ESP8266 (Print 0/1 and Control LED)
Description:
IR sensor gives digital output, either HIGH or LOW, depending on whether it detects an object or not. We read this value using `digitalRead()` and print it on Serial Monitor as 0 or 1. Based on this value, the LED will glow or stop.
```cpp
#define IR_SENSOR 5   // D1
#define LED 4         // D2

void setup() {
  pinMode(IR_SENSOR, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int irValue = digitalRead(IR_SENSOR);

  Serial.println(irValue);   // prints 0 or 1

  if (irValue == 1) {
    digitalWrite(LED, HIGH);  // object detected, LED ON
  } else {
    digitalWrite(LED, LOW);   // no object, LED OFF
  }

  delay(500);
}
```
Note: Some IR sensor modules give the opposite logic (0 when object detected, 1 when not). If your LED behaves opposite to what you expect, just swap `HIGH` and `LOW` in the if condition.
---
Activity 6: LDR Values in Serial Monitor (with LED Brightness Control)
Description:
LDR (Light Dependent Resistor) gives analog values depending on the amount of light falling on it. We read this using `analogRead()` (ESP8266 has only one analog pin, `A0`) and print the value on Serial Monitor.
As a bonus, we also use `analogWrite()` to control the brightness of an LED based on the LDR reading, so it covers both analog read and analog write in one activity.
```cpp
#define LDR A0
#define LED 4   // D2

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int ldrValue = analogRead(LDR);   // value ranges 0 to 1023

  Serial.print("LDR Value: ");
  Serial.println(ldrValue);

  int brightness = map(ldrValue, 0, 1023, 0, 255);
  analogWrite(LED, brightness);     // LED brightness changes with light

  delay(500);
}
```
Note: In dark condition LDR value will be low, in bright light it will be high (or opposite, depending on how your LDR is wired with resistor). Adjust the `map()` values as per your reading if needed.
---
Activity 7: 3-Wheel Robot with L298N Motor Driver (Forward, Backward, Left, Right, Stop)
Description:
Here we control a robot using the L298N motor driver. The driver has 4 direction pins (IN1, IN2, IN3, IN4) which we control using `digitalWrite()`. By changing HIGH/LOW combination on these pins, the robot moves forward, backward, turns left, turns right, or stops.
```cpp
#define IN1 D0
#define IN2 D1
#define IN3 D2
#define IN4 D3

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopRobot() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void loop() {
  forward();
  delay(2000);
  stopRobot();
  delay(1000);

  backward();
  delay(2000);
  stopRobot();
  delay(1000);

  turnLeft();
  delay(2000);
  stopRobot();
  delay(1000);

  turnRight();
  delay(2000);
  stopRobot();
  delay(1000);
}
```
Note: Pins used here (D0, D1, D2, D3) are just examples, connect them to the IN1/IN2/IN3/IN4 pins of your L298N as per your wiring, and change the pin numbers in code accordingly.
---
Activity 8: Controlling the Robot Using Access Point (AP) Mode + Basic HTML
Description:
Instead of writing fixed movements, now we control the robot live from a mobile/laptop browser. The ESP8266 creates its own WiFi network (Access Point), and it also runs a small web server. When you open the ESP's IP address in a browser, you get a page with buttons (Forward, Backward, Left, Right, Stop). Clicking a button sends a request to the ESP8266, which then moves the robot.
```cpp
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define IN1 D0
#define IN2 D1
#define IN3 D2
#define IN4 D3

ESP8266WebServer server(80);

const char* ssid = "Robot_Car";
const char* password = "12345678";   // minimum 8 characters

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopRobot() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

// simple webpage with buttons
String webpage = R"(
<!DOCTYPE html>
<html>
<body style="text-align:center;">
  <h2>ESP8266 Robot Control</h2>
  <button onclick="location.href='/forward'">Forward</button><br><br>
  <button onclick="location.href='/left'">Left</button>
  <button onclick="location.href='/stop'">Stop</button>
  <button onclick="location.href='/right'">Right</button><br><br>
  <button onclick="location.href='/backward'">Backward</button>
</body>
</html>
)";

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());   // usually 192.168.4.1

  server.on("/", []() {
    server.send(200, "text/html", webpage);
  });

  server.on("/forward", []() {
    forward();
    server.send(200, "text/html", webpage);
  });

  server.on("/backward", []() {
    backward();
    server.send(200, "text/html", webpage);
  });

  server.on("/left", []() {
    turnLeft();
    server.send(200, "text/html", webpage);
  });

  server.on("/right", []() {
    turnRight();
    server.send(200, "text/html", webpage);
  });

  server.on("/stop", []() {
    stopRobot();
    server.send(200, "text/html", webpage);
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
```
How to use:
Upload the code, open Serial Monitor, and power the robot.
On your phone/laptop, connect to WiFi named `Robot_Car` (password `12345678`).
Open a browser and go to `192.168.4.1` (or whatever IP printed in Serial Monitor).
You will see buttons, tap them to move the robot.
---
Activity 9: Same Access Point Code + Speed Control Slider (D4, D5)
Description:
This builds on Activity 8. We connect the L298N's speed pins (ENA and ENB) to D4 and D5 on the ESP8266. Since these support PWM, we use `analogWrite()` to control motor speed. A slider is added on the same webpage — moving the slider sends the speed value to the ESP8266, which then updates the motor speed live.
```cpp
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define IN1 D0
#define IN2 D1
#define IN3 D2
#define IN4 D3
#define ENA D4
#define ENB D5

ESP8266WebServer server(80);

const char* ssid = "Robot_Car";
const char* password = "12345678";

int motorSpeed = 200;   // default speed, range 0 - 1023

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopRobot() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void setSpeed(int speed) {
  motorSpeed = speed;
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}

// webpage with buttons + speed slider
String webpage = R"(
<!DOCTYPE html>
<html>
<body style="text-align:center;">
  <h2>ESP8266 Robot Control</h2>
  <button onclick="location.href='/forward'">Forward</button><br><br>
  <button onclick="location.href='/left'">Left</button>
  <button onclick="location.href='/stop'">Stop</button>
  <button onclick="location.href='/right'">Right</button><br><br>
  <button onclick="location.href='/backward'">Backward</button><br><br>

  <p>Speed Control</p>
  <input type="range" min="0" max="255" value="200"
         onchange="fetch('/speed?value=' + this.value)">
</body>
</html>
)";

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());

  setSpeed(motorSpeed);   // apply default speed at start

  server.on("/", []() {
    server.send(200, "text/html", webpage);
  });

  server.on("/forward", []() {
    forward();
    server.send(200, "text/html", webpage);
  });

  server.on("/backward", []() {
    backward();
    server.send(200, "text/html", webpage);
  });

  server.on("/left", []() {
    turnLeft();
    server.send(200, "text/html", webpage);
  });

  server.on("/right", []() {
    turnRight();
    server.send(200, "text/html", webpage);
  });

  server.on("/stop", []() {
    stopRobot();
    server.send(200, "text/html", webpage);
  });

  server.on("/speed", []() {
    if (server.hasArg("value")) {
      int val = server.arg("value").toInt();
      setSpeed(val);
    }
    server.send(200, "text/plain", "OK");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
```
Note: `ENA` and `ENB` are connected to `D4` and `D5` as you mentioned. The slider sends values from 0 to 1023 (since ESP8266 PWM range is 0-1023 by default), and the motor speed updates instantly without reloading the page.
---
Quick Recap of Functions Used
Function	Used For	Activity
`digitalWrite()`	Turning LED ON/OFF, controlling motor direction	1, 2, 3, 4, 5, 7, 8, 9
`digitalRead()`	Reading IR sensor value (0 or 1)	5
`analogRead()`	Reading LDR value (0 to 1023)	6
`analogWrite()`	Controlling LED brightness (PWM), motor speed	6, 9
`WiFi.softAP()`	Creating ESP8266 Access Point	8, 9
`server.on()` / `server.handleClient()`	Handling web page requests	8, 9
