import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # bus = 0, device = 0 (using CE0)
spi.max_speed_hz = 1350000  # 1.35 MHz

def read_adc(channel):
    assert 0 <= channel <= 7, 'Channel must be between 0 and 7.'
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        adc_value = read_adc(0)  # Read from channel 0
        print(f'ADC Value: {adc_value}')
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
