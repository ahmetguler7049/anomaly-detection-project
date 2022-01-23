#include<LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
//                RS   E  4  3  2  1
int kledbir = 7;

 void hayvan(){
    lcd.clear();
    digitalWrite(kledbir,HIGH);
    lcd.print("     DIKKAT");
    lcd.setCursor(0,1);
    lcd.print("  Vahsi Hayvan");
    delay(4000);
    digitalWrite(kledbir,LOW);
  }

 void robot(){
    lcd.clear();
    digitalWrite(kledbir,HIGH);
    lcd.print("     DIKKAT");
    lcd.setCursor(0,1);
    lcd.print(" UZAYLI ISTILASI");
    delay(4000);
    digitalWrite(kledbir,LOW);
  }

  void araba(){
    lcd.clear();
    digitalWrite(kledbir,HIGH);
    lcd.print("     DIKKAT");
    lcd.setCursor(0,1);
    lcd.print("    TERS YON");
    delay(4000);
    digitalWrite(kledbir,LOW);
  }
 
/* void uyari(int sinyal){
  if(sinyal==1){
    buzlanma();
  }
  else if(sinyal==2){
    yangin();
  }
  else if(sinyal==3){
    kaza(); 
  }
}*/
void setup() {
  lcd.begin(16,2);
  lcd.clear();
  lcd.print("Iyi yolculuklar");
  pinMode(kledbir,OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(1);
  

}
void loop() {
   while (Serial.available() > 0){
    int x = Serial.readString().toInt();
     if(x==0){
      lcd.clear();
      lcd.print("Iyi yolculuklar");
      }
      
     else if(x==1){
      robot();
      x = 0;
     }
     
     else if(x==2){
      hayvan();
      x = 0;
     }
      
     else if(x==3){
      araba();
      x = 0;
     }

     else {
      lcd.clear();
      lcd.print("Iyi yolculuklar");
     }
      
     
   }
}
