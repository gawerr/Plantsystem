import time
import busio
import digitalio
import board
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# NOTE this needs the venv envirmonent

# Initialize SPI, CS, MCP3008, and Analog Channel 0
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP3008(spi, cs)
chan0 = AnalogIn(mcp, 0) # P0 or 0 for CH0

print("Reading MCP3008 (CH0), press Ctrl-C to quit...")

while True:
    # Print 16-bit mapped raw value and 3.3V voltage
    print(f"Raw: {chan0.value:>5d} | Voltage: {chan0.voltage:.2f}V")
    time.sleep(0.5)
