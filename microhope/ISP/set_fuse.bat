echo "Setting fuses for ATmega16: 8Mhz External Crystal, disable JTAG"
uisp -dprog=dapa -dpart=atmega16 -dlpt=0x378 --erase
uisp -dprog=dapa -dpart=atmega16 -dlpt=0x378 --wr_fuse_l=0xff
uisp -dprog=dapa -dpart=atmega16 -dlpt=0x378 --wr_fuse_h=0xda 
uisp -dprog=dapa -dpart=atmega16 -dlpt=0x378 --rd_fuses 
