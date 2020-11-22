#include <ESP8266WiFi.h>                                                // esp8266 library
#include <FirebaseArduino.h>                                             // firebase library

// Set these to run example.
#define FIREBASE_HOST "smarttraffic-c88f7.firebaseio.com"
#define FIREBASE_AUTH "ijLC1thkSIFi4xfdFNMhpkwIi25nd19T2IGMDClJ"
#define WIFI_SSID "saiprasad"
#define WIFI_PASSWORD "password123"
int fireStatus = 0;
int count1 = 0;
int count2 = 0;
// led status received from firebase
int red = D2;   
int yellow = D1;  
int green = D0; 
int red2 = D7;   
int yellow2 = D6;  
int green2 = D5; 


// for external led
void setup() {
  Serial.begin(9600);
  delay(1000);
  pinMode(green, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green2, OUTPUT);
  pinMode(red2, OUTPUT);
  pinMode(yellow2, OUTPUT);                 
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                      //try to connect with wifi
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  } 
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());                                                   //print local IP address
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);                                                                      // connect to firebase                                         //send initial string of led status
}

void loop() {
  
  fireStatus = Firebase.getInt("LED_Status/timer");
  count1 = Firebase.getInt("LED_Status/count1");
  count2 = Firebase.getInt("LED_Status/count2");
  Serial.println(fireStatus);
  if(Firebase.failed())
  {
    Serial.println("failed");
    Serial.println(Firebase.error());
  }
  if(count1 >= count2){
    digitalWrite(red, HIGH);
    Serial.println("Red Led Turned ON");
    digitalWrite(green2, HIGH);
    Serial.println("Green2 Led Turned ON");
    delay(500);
    digitalWrite(green2, LOW);    
    Serial.println("Green2 Led Turned OFF");
    digitalWrite(yellow2, HIGH);
    Serial.println("Yellow2 Led Turned ON");
    delay(500);
    digitalWrite(yellow2, LOW);
    Serial.println("Yellow2 Led Turned OFF");
    digitalWrite(red2, HIGH);
    Serial.println("Red2 Led Turned ON");
    digitalWrite(red, LOW);
    Serial.println("Red Led Turned OFF");
    digitalWrite(yellow, HIGH);
    Serial.println("Yellow Led Turned ON");
    delay(1000);
    digitalWrite(yellow, LOW);
    Serial.println("Yellow Led Turned OFF");
    digitalWrite(green, HIGH);
    Serial.println("Green Led Turned ON");                                                
    delay(fireStatus);
    digitalWrite(green, LOW);    
    Serial.println("Green Led Turned OFF");
    digitalWrite(red2, LOW);    
    Serial.println("Red2 Led Turned OFF");
  }
  else{
    digitalWrite(red2, HIGH);
    Serial.println("Red2 Led Turned ON");
    digitalWrite(green, HIGH);
    Serial.println("Green Led Turned ON");
    delay(500);
    digitalWrite(green, LOW);    
    Serial.println("Green Led Turned OFF");
    digitalWrite(yellow, HIGH);
    Serial.println("Yellow Led Turned ON");
    delay(500);
    digitalWrite(yellow, LOW);
    Serial.println("Yellow Led Turned OFF");
    digitalWrite(red, HIGH);
    Serial.println("Red Led Turned ON");
    digitalWrite(red2, LOW);
    Serial.println("Red Led Turned OFF");
    digitalWrite(yellow2, HIGH);
    Serial.println("Yellow2 Led Turned ON");
    delay(1000);
    digitalWrite(yellow2, LOW);
    Serial.println("Yellow2 Led Turned OFF");
    digitalWrite(green2, HIGH);
    Serial.println("Green2 Led Turned ON");                                                
    delay(fireStatus);
    digitalWrite(green2, LOW);    
    Serial.println("Green2 Led Turned OFF");
    digitalWrite(red, LOW);    
    Serial.println("Red Led Turned OFF");
  }
  /*if (fireStatus.equals("ON")) {                                                          // compare the input of led status received from firebase
    Serial.println("Led Turned ON");                                                
    digitalWrite(led, HIGH);                                                         // make external led ON
  } 
  else if (fireStatus.equals("OFF")) {                                                  // compare the input of led status received from firebase
    Serial.println("Led Turned OFF");
    digitalWrite(led, LOW);                                                         // make external led OFF
  }
  else {
    Serial.println("Wrong Credential! Please send ON/OFF");
  }*/
}
