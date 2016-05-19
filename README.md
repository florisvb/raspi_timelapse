# raspi_timelapse

1. Set up the camera with raspi-config
2. Build a touch switch, connect it to GPIO 21 and ground
3. Install this codebase (git clone) into ~/Documents for everything to work out of the box

4. Set up a mount point for the USB drive:
sudo mkdir /media/usb
sudo chown -R pi:pi /media/usb

5. Move startup to: /etc/init.d
6. Run: sudo update-rc.d startup defaults
This adds the script to the startup routine

Now, whenthe raspberry pi turns on, it will start taking a picture every 10 secodns, and saves it to the USB drive. To shut down, hit the button.

