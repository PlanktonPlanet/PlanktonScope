# Logger library compatible with multiprocessing
from loguru import logger

import datetime
import os

import Adafruit_SSD1306

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

logger.info("planktoscope.display is loading")

import planktoscope.uuidName


class Display(object):
    def __init__(self):
        # Raspberry Pi pin configuration:
        RST = None  # on the PiOLED this pin isnt used

        # 128x32 display with hardware I2C:
        self.__disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

        # Initialize library.
        self.__disp.begin()

        self.display_machine_name()
        logger.success("planktoscope.display is ready!")

    def display_machine_name(self):
        self.__clear()
        machineName = planktoscope.uuidName.machineName(
            machine=planktoscope.uuidName.getSerial()
        )
        self.display_text(machineName.replace(" ", "\n"))

    def display_text(self, message):
        logger.info(f"Displaying message {message}")

        # Clear display.
        self.__clear()
        width = self.__disp.width
        height = self.__disp.height

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.

        image = PIL.Image.new("1", (width, height))

        # Get drawing object to draw on image.
        draw = PIL.ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Load default font.
        font = PIL.ImageFont.truetype(
            font="truetype/dejavu/DejaVuSansMono.ttf", size=15
        )

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        text_size = font.getsize_multiline(message)
        x = width / 2 - text_size[0] / 2

        draw.text((x, 0), message, font=font, fill=255, align="center")

        # draw.text((0, top + 15), "READY", font=font, fill=255)
        # now = datetime.datetime.isoformat(datetime.datetime.now())[:-16]
        # draw.text(
        #    (68, 0),
        #    now,
        #    font=PIL.ImageFont.truetype(font="truetype/dejavu/DejaVuSansMono.ttf", size=10),
        #    fill=255,
        # )
        #    draw.text((x, top + 16), str(Disk), font=font, fill=255)
        #    draw.text((x, top + 24), "wlan0:" + str(IP), font=font, fill=255)

        # Display image.
        self.__disp.image(image)
        self.__disp.display()

    def __clear(self):
        logger.trace("Clear the display")
        # Clear display.
        self.__disp.clear()
        self.__disp.display()

    def stop(self):
        logger.info("Display is out!")
        self.__clear()


if __name__ == "__main__":
    import time

    display = Display()
    time.sleep(5)
    display.display_text("Nice hat you have")
    time.sleep(5)
    display.display_text("Bye!")
    time.sleep(5)
    display.stop()