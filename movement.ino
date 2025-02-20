// Motor Driver Pins
#define ENA 9
#define IN1 4
#define IN2 5
#define IN3 6
#define IN4 7
#define ENB 10

// Ultrasonic Sensor Pins
#define TRIG 11
#define ECHO 12

// Threshold distance to avoid obstacles (in cm)
#define OBSTACLE_THRESHOLD 20

void setup() {
    // Motor control pins as outputs
    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);

    // Ultrasonic sensor pins
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    // Start serial monitor
    Serial.begin(9600);

    // Start motors
    analogWrite(ENA, 70);  // Set motor speed
    analogWrite(ENB, 70);
}

// Function to measure distance using the ultrasonic sensor
int getDistance() {
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    
    long duration = pulseIn(ECHO, HIGH);
    int distance = duration * 0.034 / 2; // Convert to cm

    return distance;
}

// Functions for movement
void moveForward() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}

void moveBackward() {
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
    delay(500); // Small turn delay
}

void turnRight() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(500); // Small turn delay
}

void stopRobot() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void loop() {
    int distance = getDistance();
    Serial.print("Distance: ");
    Serial.println(distance);

    if (distance > OBSTACLE_THRESHOLD) {
        moveForward();
    } else {
        stopRobot();
        delay(1000);
    }

    delay(100);
}
