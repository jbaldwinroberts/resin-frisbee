#include <libs/Adafruit_NeoPixel/Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

enum STATE
{
  Initialising,
  Ready,
  Flying,
  Score
};

Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, 6, NEO_GRB + NEO_KHZ800);
STATE state = Initialising;
int frequency = 1;

void setup()
{
  strip.begin();
  strip.setBrightness(64);
  strip.show(); // Initialize all pixels to 'off'
}

void loop()
{
//  if (Serial.available()) {
//    Serial1.write(Serial.read());
//  }
//  if (Serial1.available()) {
//    Serial.write(Serial1.read());
//  }
  
  if(state == Initialising) flash(strip.Color(255, 0, 0));
  else if(state == Ready) flash(strip.Color(0, 255, 0));
  else if(state == Flying) flash(strip.Color(0, 0, 255));
  else if(state == Score)
  {
    theaterChase(strip.Color(255, 255, 255), 50);
    state = Ready;
  }

  if(Serial1.available() > 0)
  {
    String message;
    while(Serial1.available())
    {
      message += (char)Serial1.read();
    }

    Serial.println(message);

    if(message == "i")
    {
      state = Initialising;
      frequency = 1;
    }
    else if(message == "r")
    {
      state = Ready;
      frequency = 1;
    }
    else if(message == "s")
    {
      state = Score;
    }
    else
    {
      state = Flying;
      frequency = message.toInt();
    }
  }
}

void flash(uint32_t c)
{
  enable(c);
  delay(1000 / frequency);
  disable();
  delay(1000 / frequency);
}

void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<50; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();

      delay(wait);

      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

void enable(uint32_t c)
{
  for(uint16_t i=0; i < strip.numPixels(); i++) strip.setPixelColor(i, c);
  strip.show();
}

void disable()
{
  for(uint16_t i=0; i < strip.numPixels(); i++) strip.setPixelColor(i, strip.Color(0, 0, 0));
  strip.show();
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

