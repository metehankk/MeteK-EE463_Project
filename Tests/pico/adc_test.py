from machine import ADC, Pin
import time

adc = machine.ADC(0)
while True:
    ADC_voltage = adc.read_u16()*(3.3/65535)
    ## temp_c = 27 - (ADC_voltage - 0.706)/0.001721
    current = -(2.5 - ADC_voltage)/0.0667
    print("ADC_v: {} V, Current: {} A".format(ADC_voltage, current))
    time.sleep_ms(100)