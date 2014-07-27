#include "mh-utils.c"


int main (void)
  {
  DDRB = 255;		// Data Direction Register for port B

  for(;;)
    {
    PORTB = 255;	
    delay_ms(5000);
    PORTB = 0;
    delay_ms(7000);
  }
return 0;
}
