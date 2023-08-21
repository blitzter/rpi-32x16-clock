#!/usr/bin/env python
import datetime
import os
import time
import board
import adafruit_dht

try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics

from samplebase import SampleBase


class RGB32x16MatrixClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RGB32x16MatrixClock, self).__init__(*args, **kwargs)
        try:
            self.dht_device = adafruit_dht.DHT22(board.D4)
            self.dht_device_enabled = True
        except:
            self.dht_device_enabled = False
        self.time = datetime.datetime.now()
        self.hours = self.time.hour
        self.minutes = self.time.minute
        self.second_line_1_1 = ''
        self.second_line_2 = ''
        self.second_line_3 = ''
        if self.dht_device_enabled:
            self.second_line_1_2 = '{:.1f}c'.format(self.dht_device.temperature)
            self.second_line_1_3 = '{:.1f}%'.format(self.dht_device.humidity)
        else:
            self.second_line_1_2 = '00c'
            self.second_line_1_3 = '00%'
        self.second_line_mode = int(self.time.second/20)
        self.changed = True
        self.update_time()

    def run(self):
        double_buffer = self.matrix.CreateFrameCanvas()
        base_dir = os.path.dirname(__file__)
        font = graphics.Font()
        font.LoadFont(base_dir + "/fonts/7x13.bdf")
        second_line_font = graphics.Font()
        second_line_font.LoadFont(base_dir + "/fonts/4x6.bdf")

        clock_color = graphics.Color(50, 50, 150)
        second_line_color_1 = graphics.Color(50, 90, 90)
        second_line_color_2 = graphics.Color(80, 80, 80)

        while 1 == 1:
            if self.changed is True:
                double_buffer.Clear()
                self.print_clock_to_buffer(double_buffer, font, clock_color)
                self.print_second_line_to_buffer(double_buffer, second_line_font, second_line_color_1,
                                                 second_line_color_2)

                double_buffer = self.matrix.SwapOnVSync(double_buffer)
                self.changed = False
            time.sleep(1 / 4)
            self.update_time()

    def update_time(self):
        self.time = datetime.datetime.now()
        hours = '{:02d}'.format(self.time.hour)
        minutes = '{:02d}'.format(self.time.minute)
        second_line_mode = int(self.time.second/20)
        if hours == self.hours and minutes == self.minutes and second_line_mode == self.second_line_mode:
            pass
        else:
            if self.dht_device_enabled:
                self.second_line_1_2 = '{:.1f}c'.format(self.dht_device.temperature)
                self.second_line_1_3 = '{:.1f}%'.format(self.dht_device.humidity)
            self.hours = hours
            self.minutes = minutes
            self.second_line_1_1 = str.upper(self.time.strftime("%a"))
            self.second_line_2 = self.time.strftime("%-d")
            self.second_line_3 = str.upper(self.time.strftime("%b"))
            self.second_line_mode = second_line_mode
            self.changed = True

    def print_clock_to_buffer(self, double_buffer, font, clock_color):
        graphics.DrawText(double_buffer, font, 13, 8, clock_color, ':')
        graphics.DrawText(double_buffer, font, 0, 9, clock_color, self.hours)
        graphics.DrawText(double_buffer, font, 19, 9, clock_color, self.minutes)

    def print_second_line_to_buffer(self, double_buffer, second_line_font, second_line_color_1, second_line_color_2):
        if self.second_line_mode == 0:
            graphics.DrawText(double_buffer, second_line_font, 0, 15, second_line_color_1, self.second_line_1_1)
        if self.second_line_mode == 1:
            graphics.DrawText(double_buffer, second_line_font, 0, 15, second_line_color_1, self.second_line_1_2)
        if self.second_line_mode == 2:
            graphics.DrawText(double_buffer, second_line_font, 0, 15, second_line_color_1, self.second_line_1_3)
        graphics.DrawText(double_buffer, second_line_font, 13, 15, second_line_color_2, self.second_line_2)
        graphics.DrawText(double_buffer, second_line_font, 21, 15, second_line_color_2, self.second_line_3)


# Main function
if __name__ == "__main__":
    clock = RGB32x16MatrixClock()
    clock.process()
