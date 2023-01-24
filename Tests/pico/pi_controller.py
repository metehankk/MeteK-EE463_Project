from machine import ADC, Pin, PWM
import utime

adc_in = ADC(0)
set_button = Pin(3, Pin.IN, Pin.PULL_DOWN)
pwm = PWM(Pin(0))
pwm.freq(25000)
current_ref = 3
Ki = 10
Kp = 80
t = 1/25000
current = 0

last = 0
lasterror = 0
err_I = 1
limMax = 5
limMin = -5
while True:
        
    now = utime.time()
    dt = now - last
    if set_button.value() > 0.5:
        current_ref = 15
    
    elif set_button.value() < 0.5:
        current_ref = 3
    
    ADC_voltage = adc_in.read_u16()*(3.3/65535)
    
    current = -(2.5 - ADC_voltage)/0.0667    
    
    if dt >= t:
        error = current_ref - current        
        
        err_I = err_I + 0.5 * Ki * dt * (error + lasterror)
        if err_I > limMax:
            err_I = limMax
        elif err_I < limMin:
            err_I = limMin
        
        err_PI = Kp * error + err_I
                
        if err_PI > 1 and current < 25 :
            pwm.duty_u16(65536)
        elif err_PI > 0 and err_PI < 1 and current < 25:
            pwm.duty_u16(int(err_out*65536))
        else :
            pwm.duty_u16(0)
        
        last = now
        lasterror = error
    print("error: {} , current: {}, current_ref: {}".format(err_PI, current, current_ref))
    utime.sleep_us(int(t*1000000))
    
        