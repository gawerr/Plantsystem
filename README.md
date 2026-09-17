Plant watering system with Raspberry PI

Enable SPI on Raspberry Pi:

Prep Raspberry PI
  sudo raspi-config
  
  Interfacing Options → SPI → Yes
  
  Reboot (sudo reboot)
  
Description

This plant watering system automates plant care by monitoring soil moisture and supplying water only when it is needed. Moisture sensors measure the condition of the soil, while a Raspberry Pi processes the readings and determines when watering should begin or stop. The system also records sensor data and watering activity, creating a useful log for tracking plant conditions, reviewing water use, and improving care over time.
