"""Snow Globe for Adafruit Circuit Playground express with CircuitPython """

import math
import time
import random

from adafruit_circuitplayground.express import cpx

ROLL_THRESHOLD = 30  # Total acceleration
cpx.pixels.brightness = 0.1  # set brightness value

WHITE = (65, 65, 65)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
SKYBLUE = (0, 20, 200)
BLACK = (0, 0, 0)

# Initialize the global states
new_roll = False
rolling = False

# Set number of songs here for randomization
song_numbers = [1, 2, 3]
resting_colors = [WHITE, RED, GREEN, BLUE, SKYBLUE]

## =====================================
## We are defining ALL of our music here
## =====================================

# set up time signature
whole_note = 1.5  # adjust this to change tempo of everything
# other notes are fractions of the whole note
half_note = whole_note / 2
quarter_note = whole_note / 4
dotted_quarter_note = quarter_note * 1.5
eighth_note = whole_note / 8

# set up note values
C3 = 131
G3 = 196
A3 = 220
Bb3 = 233
B3 = 247
C4 = 262
Db4 = 277
D4 = 294
Eb4 = 311
E4 = 330
F4 = 349
Gb4 = 370
G4 = 392
Ab4 = 415
A4 = 440
Bb4 = 466
B4 = 494
C5 = 523
D5 = 587
E5 = 659

# Jingle Bells
jingle_bells_song = [
        [E4, quarter_note],
        [E4, quarter_note],
        [E4, half_note],
        [E4, quarter_note],
        [E4, quarter_note],
        [E4, half_note],
        [E4, quarter_note],
        [G4, quarter_note],
        [C4, dotted_quarter_note],
        [D4, eighth_note],
        [E4, whole_note],
    ]

# Let It Snow
let_it_snow_song = [
    [B4, eighth_note],
    [A4, eighth_note],
    [G4, quarter_note],
    [G4, eighth_note],
    [F4, eighth_note],
    [E4, quarter_note],
    [E4, eighth_note],
    [D4, eighth_note],
    [C4, whole_note],
    [G3, eighth_note],
    [G3, eighth_note],
    [G4, eighth_note],
    [G4, eighth_note],
    [F4, quarter_note],
    [E4, quarter_note],
    [D4, eighth_note],
    [C4, quarter_note],
    [G3, whole_note],

]

# Linus & Lucy (A Peanuts Christmas song)
linus_and_lucy_song = [
    [C3, eighth_note],
    [G3, eighth_note],
    [C4, eighth_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [C4, dotted_quarter_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [A3, eighth_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [A3, dotted_quarter_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [C4, eighth_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [C4, dotted_quarter_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [A3, eighth_note],
    [C3, eighth_note],
    [G3, eighth_note],
    [A3, dotted_quarter_note],
    [C5, quarter_note],
    [D5, eighth_note],
    [E5, quarter_note],
    [E5, eighth_note],
    [D5, eighth_note],
    [C5, quarter_note],
    [D5, dotted_quarter_note],
    [C5, half_note],
    [C5, quarter_note],
    [D5, eighth_note],
    [E5, whole_note],
]

# pylint: disable=too-many-locals
def play_song(song_number):
    # Preloaded with...
    # 1: Jingle bells
    # 2: Let It Snow
    # 3: Linus & Lucy

    # Choose to play a single song
    if song_number == 1:
        # Choose to play Jingle Bells
        song = jingle_bells_song
    # pylint: disable=consider-using-enumerate

    elif song_number == 2:
        # Choose to play Let it Snow
        song = let_it_snow_song
    
    elif song_number == 3:
        # Choose to play Linus & Lucy
        song = linus_and_lucy_song

    for n in range(len(song)):
        cpx.start_tone(song[n][0])
        time.sleep(song[n][1])
        cpx.stop_tone()

# Fade pixels in and out (once)
def fade_pixels(fade_color):
    # fade up
    for j in range(25):
        pixel_brightness = (j * 0.01)
        cpx.pixels.brightness = pixel_brightness
        for i in range(10):
            cpx.pixels[i] = fade_color

    # fade down
    for k in range(25):
        pixel_brightness = (0.25 - (k * 0.01))
        cpx.pixels.brightness = pixel_brightness
        for i in range(10):
            cpx.pixels[i] = fade_color

## ==========================================================
## Code below here is what initiates our snow globe activity!
## ==========================================================

# fade in the pixels on start
fade_pixels(GREEN)
# play music on start - choose what song number you want to hear on startup!
play_song(1)

# Loop forever
while True:
    # check for shaking
    # Compute total acceleration
    x_total = 0
    y_total = 0
    z_total = 0
    for count in range(10):
        x, y, z = cpx.acceleration
        x_total = x_total + x
        y_total = y_total + y
        z_total = z_total + z
        time.sleep(0.001)
    x_total = x_total / 10
    y_total = y_total / 10
    z_total = z_total / 10

    total_accel = math.sqrt(x_total * x_total + y_total *
                            y_total + z_total * z_total)

    # Check for rolling
    if total_accel > ROLL_THRESHOLD:
        roll_start_time = time.monotonic()
        new_roll = True
        rolling = True
        print('shaken')

    # Rolling momentum
    # Keep rolling for a period of time even after shaking stops
    if new_roll:
        if time.monotonic() - roll_start_time > 2:  # seconds to run
            rolling = False

    # Light show
    if rolling:
        fade_pixels(SKYBLUE)
        fade_pixels(WHITE)
        cpx.pixels.brightness = 0.8
        roll_color = random.choice(resting_colors)
        cpx.pixels.fill(roll_color)

    elif new_roll:
        new_roll = False
        song_number = random.choice(song_numbers)
        # play a song!
        play_song(song_number)
        # return to resting color
        fade_pixels(roll_color)
        cpx.pixels.brightness = 0.05
        cpx.pixels.fill(roll_color)
