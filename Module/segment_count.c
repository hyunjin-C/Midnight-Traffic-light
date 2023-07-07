#include <stdio.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>

#define _CTR_SECUR_NI_WARNINGS

#define LED_R_C 9
#define LED_Y_C 0
#define LED_G_C 2

#define LED_R_P 3
#define LED_G_P 1

int ct;


char FND_DB[8] = {27, 26, 25, 24, 23, 22, 21, 30};
char FND_DATA[10] = {0x7b, 0x7f, 0x72, 0x5f, 0x5b, 0x33, 0x79, 0x6d, 0x30, 0x7e};

char FND_DATA_dot[10] = {0xfb, 0xff, 0xf2, 0xdf, 0xdb, 0xb3, 0xf9, 0xed, 0xb0, 0xfe};
char FND_IN[2] = {29, 28};
char FND_TEN[3] = {0x7e, 0x30, 0x6d};

int getBit(int num, int idx)
{
    return ((1 << idx) & num) >> idx;
}

void setting() {
	pinMode(LED_R_C,OUTPUT);
	pinMode(LED_Y_C,OUTPUT);
	pinMode(LED_G_C,OUTPUT);
  pinMode(LED_R_P,OUTPUT);
	pinMode(LED_G_P,OUTPUT);
}

void FndDisplay(char Data)
{
    int bitValue = 0;
    for (int j = 0; j < 8; j++)
    {
        bitValue = getBit(Data, j);
        if (bitValue)
            digitalWrite(FND_DB[j], HIGH);
        else
            digitalWrite(FND_DB[j], LOW);
    }
}

void leftright(int ten, int one)
{
    time_t t = time(NULL) + 1;
    while (time(NULL) < t)
    {
        pinMode(FND_IN[0], OUTPUT);
        pinMode(FND_IN[1], INPUT);
        FndDisplay(FND_TEN[ten]);
        delay(10);
        pinMode(FND_IN[1], OUTPUT);
        pinMode(FND_IN[0], INPUT);
        if (ct == 1)
            FndDisplay(FND_DATA[one]);
        else if (ct == 0)
            FndDisplay(FND_DATA_dot[one]);
        delay(10);
    }
}

void set()
{
    for (int i = 0; i < 8; i++)
    {
        pinMode(FND_DB[i], OUTPUT);
    }
}

void one(int t)
{
    if (ct == 0 && t == 2)
    {
        set();
        leftright(t, 9);
    }
    else if (ct == 1)
    {
        if (t == 1)
        {
            for (int z = 4; z < 10; z++)
            {
                set();
                leftright(t, z);
            }
        }
    }
    if ((ct == 0 && t == 1) || t == 0)
    {
        for (int z = 0; z < 10; z++)
        {
            set();
            leftright(t, z);
        }
    }
}

int count(void)
{

    for (int i = 1; i >= 0; i--)
    {
        one(i);
    }

    for (int i = 0; i < 8; i++)
    {
        pinMode(FND_DB[i], INPUT);
    }
    return 0;
}

void turnOffAll(){
	digitalWrite(LED_R_C,LOW);
	digitalWrite(LED_Y_C,LOW);
	digitalWrite(LED_G_C,LOW);
  digitalWrite(LED_R_P,LOW);
	digitalWrite(LED_G_P,LOW);
}

void sensePIR()
{
    turnOffAll();
    wiringPiSetup();
  	setting();
  	turnOffAll();
  	
  	digitalWrite(LED_G_C,HIGH);
    digitalWrite(LED_R_P,HIGH);
  	delay(3000);
  	turnOffAll();
   
    digitalWrite(LED_Y_C,HIGH);
    digitalWrite(LED_R_P,HIGH);
  	delay(3000);
  	turnOffAll();
  	
    digitalWrite(LED_R_P,HIGH);
    digitalWrite(LED_R_C,HIGH);
    delay(2000);//2sec delay
    digitalWrite(LED_R_P,LOW);
  	digitalWrite(LED_G_P,HIGH);
    count();
  	turnOffAll();
    ct = 0;
}

void blink()
{ // 한번에 1초 실행
    digitalWrite(LED_Y_C, HIGH);
    delay(500);
    digitalWrite(LED_Y_C, LOW);
    delay(500);
}

void *td1(void *arg)
{
    time_t t = time(NULL) + 20;
    while (time(NULL) < t)
    {
        blink();
    }
}
void *td2(void *arg)
{
    for (int i = 2; i >= 0; i--)
    {
        one(i);
    }
    for (int i = 0; i < 8; i++)
    {
        pinMode(FND_DB[i], INPUT);
    }
}

int main(int argc, char *argv[])
{
    wiringPiSetup();

    pthread_t traffic_light, count_dot, get_ct;

    turnOffAll();

    setting();
    
    if (argc > 1) {
      ct = atoi(argv[1]);
    }
    
    printf("%d\n", ct);
    
        
    
    blink();
    if (ct == 1)
    {
        sensePIR();
        pthread_create(&traffic_light, NULL, td1, NULL);
        pthread_create(&count_dot, NULL, td2, NULL);

        pthread_join(traffic_light, NULL);
        pthread_join(count_dot, NULL);
    }
    
    return 0;
}