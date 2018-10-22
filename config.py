# Pipboy 2600: A quick solution to my last minute halloween idea.
#   Tayor W Oliver, 2018
#
# RasPipBoy: A Pip-Boy 3000 implementation for Raspberry Pi
#   Neal D Corbett, 2013
#
# Configuration data

# Device options
#  (These will be automatically be set to 'False' if unavailable)
USE_INTERNET = True     # Download map/place data via internet connection
USE_GPS = True          # Use GPS module, accessed via GPSD daemon
USE_SOUND = True        # Play sounds via RasPi's current sound-source
USE_CAMERA = True       # Use RasPi camera-module as V.A.T.S
USE_SERIAL = True       # Communicate with custom serial-port controller

QUICKLOAD = False       # If true, commandline-startup bits aren't rendered
FORCE_DOWNLOAD = False  # Don't use cached map-data, if online

# Render screen-objects at this size - smaller is faster
WIDTH = 320
HEIGHT = 240

#Original display resolution:
# OUTPUT_WIDTH = 480
# OUTPUT_HEIGHT = 360

# Address for map's default position:
#   (used if GPS is inactive)
defaultPlace = "San Diego CA"

#LOCATION
#San Diego, CA
MAP_FOCUS = (-117.1611, 32.7157)

# Player data:
PLAYERNAME = 'Taylor'
PLAYERLEVEL = 32

#Somewhereland from the originall author...
#MAP_FOCUS = (-5.9347681, 54.5889076)
FPS = 15

import pygame

# My Google-API key:
gKey = '<api-key-here>'

# Teensy USB serial: symbolic link set up by creating:
#   /etc/udev/rules.d/99-usb-serial.rules
# With line:
#   SUBSYSTEM=="tty", ATTRS{manufacturer}=="Teensyduino", SYMLINK+="teensy"
SERIALPORT = '/dev/teensy'
# Pi GPIO serial:
# SERIALPORT = '/dev/ttyAMA0'

# Test serial-controller:
if USE_SERIAL:
    # Load libraries used by serial device, if present:
    def loadSerial():
        try:
            print("Importing Serial libraries...")
            global serial
            import serial
        except:
            # Deactivate serial-related systems if load failed:
            print("SERIAL LIBRARY NOT FOUND!")
            USE_SERIAL = False
    loadSerial()
if USE_SERIAL:
    try:
        print("Init serial: %s" % (SERIALPORT))
        ser = serial.Serial(SERIALPORT, 9600)
        ser.timeout = 1

        print("  Requesting device identity...")
        ser.write("\nidentify\n")

        ident = ser.readline()
        ident = ident.strip()
        print("    Value: %s" % (str(ident)))

        if ident != "PIPBOY":
            print("  Pip-Boy controls not found on serial-port!")
            # config.USE_SERIAL = False

    except:
        print("* Failed to access serial! Ignoring serial port")
        USE_SERIAL = False
print("SERIAL: %s" % (USE_SERIAL))

# Test camera:
if USE_CAMERA:
    # Is there a camera module connected?
    def hasCamera():
        try:
            import picamera
            camera = picamera.PiCamera()
            camera.close()
            return True
        except:
            return False

    USE_CAMERA = hasCamera()
print("CAMERA: %s" % (USE_CAMERA))

# Downloaded/auto-generated data will be put here:
CACHEPATH = 'cache'
if not os.path.exists(CACHEPATH):
    os.makedirs(CACHEPATH)

DRAWCOLOUR = pygame.Color(255, 255, 255)
TINTCOLOUR = pygame.Color(33, 255, 156)
SELBOXGREY = 50

EVENTS = {
    'SONG_END': pygame.USEREVENT + 1
}

print("Loading images...")
IMAGES = {
    "background":pygame.image.load('images/pipboy_back.png'),
    "scanline":pygame.image.load('images/pipboyscanlines.png'),
    "distort":pygame.image.load('images/pipboydistorteffectmap.png'),
    "statusboy":pygame.image.load('images/pipboy_statusboy.png'),
}

print("(done)")

# Test internet connection:
if USE_INTERNET:
    import urllib2

    def internet_on():
        try:
            # Can we access this Google address?
            response = urllib2.urlopen('http://74.125.228.100', timeout=1)
            return True
        except urllib2.URLError as err:
            pass
        return False

    USE_INTERNET = internet_on()
print("INTERNET: %s" % (USE_INTERNET))

# Test and set up sounds::
MINHUMVOL = 0.7
MAXHUMVOL = 1.0
if USE_SOUND:
    try:
        print("Loading sounds...")
        pygame.mixer.init(44100, -16, 2, 2048)

        SOUNDS = {
            "start":    pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_up.wav'),
            "end":      pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_down.wav'),
            "hum":      pygame.mixer.Sound('sounds/pipboy/ui_pipboy_hum_lp.wav'),
            "scroll":   pygame.mixer.Sound('sounds/pipboy/ui_pipboy_scroll.wav'),
            "changetab":    pygame.mixer.Sound('sounds/pipboy/ui_pipboy_tab.wav'),
            "changemode":   pygame.mixer.Sound('sounds/pipboy/ui_pipboy_mode.wav'),
            "static":       pygame.mixer.Sound('sounds/radio/ui_radio_static_lp.wav'),
            "tapestart":    pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_start.wav'),
            "tapestop":     pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_stop.wav'),
            "lighton":      pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_on.wav'),
            "lightoff":     pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_off.wav'),
            "beacon":       pygame.mixer.Sound('sounds/radio/beacon/ui_radio_beacon_header.wav'),
            "camerastart":  pygame.mixer.Sound('sounds/vats/ui_vats_enter.wav'),
            # "cameraexit":  pygame.mixer.Sound('sounds/vats/ui_vats_exit.wav'),
        }
        SOUNDS["hum"].set_volume(MINHUMVOL)
        print("(done)")
    except:
        USE_SOUND = False
print("SOUND: %s" % (USE_SOUND))

# Set up fonts:
pygame.font.init()
kernedFontName = 'fonts/monofonto-kerned.ttf'
monoFontName = 'fonts/monofonto.ttf'

# Scale font-sizes to chosen resolution:
FONT_SML = pygame.font.Font(kernedFontName, int(HEIGHT * (12.0 / 360)))
FONT_MED = pygame.font.Font(kernedFontName, int(HEIGHT * (16.0 / 360.0)))
FONT_LRG = pygame.font.Font(kernedFontName, int(HEIGHT * (18.0 / 360.0)))
MONOFONT = pygame.font.Font(monoFontName, int(HEIGHT * (16.0 / 360.0)))

# Find monofont's character-size:
tempImg = MONOFONT.render("X", True, DRAWCOLOUR, (0, 0, 0))
charHeight = tempImg.get_height()
charWidth = tempImg.get_width()
del tempImg

#Alternate Font code
#pygame.font.init()
#FONTS = {}
#for x in range(10, 28):
#	FONTS[x] = pygame.font.Font('monofonto.ttf', x)

#####
#
#####

EVENTS = {
	'SONG_END': pygame.USEREVENT + 1
}

#KNOBS ACTIONS
ACTIONS = {
	pygame.K_F1: "module_stats",
	pygame.K_F2: "module_items",
	pygame.K_F3: "module_data",
	pygame.K_1:	"knob_1",
	pygame.K_2: "knob_2",
	pygame.K_3: "knob_3",
	pygame.K_4: "knob_4",
	pygame.K_5: "knob_5",
	pygame.K_UP: "dial_up",
	pygame.K_DOWN: "dial_down"
}

# LINK KNOBS TO GPIO PINS
# Using GPIO.BOARD as mode
GPIO_ACTIONS = {
	22: "module_stats",
	24: "module_items",
	26: "module_data",
	13:	"knob_1",
	11: "knob_2",
	7: "knob_3",
	5: "knob_4",
	3: "knob_5",
#	8: "dial_up",
#	7: "dial_down"
}

# LINK KNOBS TO GPIO PINS (ALT)
## Using GPIO.BCM as mode
#GPIO_ACTIONS = {
#    4: "module_stats", #GPIO 4
#	14: "module_items", #GPIO 14
#	15: "module_data", #GPIO 15
#	17:	"knob_1", #GPIO 17
#	18: "knob_2", #GPIO 18
#	7: "knob_3", #GPIO 7
#	22: "knob_4", #GPIO 22
#	23: "knob_5", #GPIO 27
##	31: "dial_up", #GPIO 23
#	27: "dial_down" #GPIO 7

MAP_ICONS = {
	"camp": 		pygame.image.load('images/map_icons/camp.png'),
	"factory": 		pygame.image.load('images/map_icons/factory.png'),
	"metro": 		pygame.image.load('images/map_icons/metro.png'),
	"misc": 		pygame.image.load('images/map_icons/misc.png'),
	"monument": 	pygame.image.load('images/map_icons/monument.png'),
	"vault": 		pygame.image.load('images/map_icons/vault.png'),
	"settlement": 	pygame.image.load('images/map_icons/settlement.png'),
	"ruin": 		pygame.image.load('images/map_icons/ruin.png'),
	"cave": 		pygame.image.load('images/map_icons/cave.png'),
	"landmark": 	pygame.image.load('images/map_icons/landmark.png'),
	"city": 		pygame.image.load('images/map_icons/city.png'),
	"office": 		pygame.image.load('images/map_icons/office.png'),
	"sewer": 		pygame.image.load('images/map_icons/sewer.png'),
}

AMENITIES = {
	'pub': 				MAP_ICONS['vault'],
	'nightclub': 		MAP_ICONS['vault'],
	'bar': 				MAP_ICONS['vault'],
	'fast_food': 		MAP_ICONS['sewer'],
	'cafe': 			MAP_ICONS['sewer'],
	'drinking_water': 	MAP_ICONS['sewer'],
	'restaurant': 		MAP_ICONS['settlement'],
	'cinema': 			MAP_ICONS['office'],
	'pharmacy': 		MAP_ICONS['office'],
	'school': 			MAP_ICONS['office'],
	'bank': 			MAP_ICONS['monument'],
	'townhall': 		MAP_ICONS['monument'],
	'bicycle_parking': 	MAP_ICONS['misc'],
	'place_of_worship': MAP_ICONS['misc'],
	'theatre': 			MAP_ICONS['misc'],
	'bus_station': 		MAP_ICONS['misc'],
	'parking': 			MAP_ICONS['misc'],
	'fountain': 		MAP_ICONS['misc'],
	'marketplace': 		MAP_ICONS['misc'],
	'atm': 				MAP_ICONS['misc'],
}