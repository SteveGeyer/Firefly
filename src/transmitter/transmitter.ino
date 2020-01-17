// A transmitter translation layer. It takes commands coming from a
// computer over its USB serial port and translates them into
// appropriate FrSky commands to drive the 4-in-1 2.4G Mutlti-Protocol
// Transmitter Module which in turn drives the quadcopter.
//
// While this version is wired for FrSky, with a little work it could
// be parameterized to allow it to communicate with anything the
// 4-in-1 2.4G Mutlti-Protocol Transmitter Module is capable with.

#include "Arduino.h"
#include <stdint.h>

const int msBetweenUpdates = 9;   // Number of updates per second.
const int setupFrameCount = 1000; // How often to send setupFrame data.

const int channelBits   = 11;     // Bit size of data in channel.

const uint16_t minValue = 0x0CC; // Minimum value supported.
const uint16_t midValue = 0x400; // Middle value supported.
const uint16_t maxValue = 0x733; // Maximum value supported.

const int basicTimeout = 100;   // Basic number to use for timeout.

const int bindTimeOut   = basicTimeout; // Number of ticks in bind.
const int disarmTimeOut = basicTimeout; // Number of ticks in disarm.
const int armTimeOut    = basicTimeout; // Number of ticks in arm.

typedef enum {
    BIND,                       // Binding the transmitter to receiver.
    DISARM_BEFORE_ARM,          // Disarming before arming.
    ARM,                        // Arming the drone.
    RUN,                        // Fly the drone.
    DISARM                      // Disarm the drone.
} runState_t;

const int throttleIndex  = 0;   // Throttle offset in data.
const int directionIndex = 1;   // Left/Right offset in data.
const int forwardIndex   = 2;   // Forward/Backward offset in data.
const int spinIndex      = 3;   // Spin Clockwise/CounterClockwise offset.
const int armIndex       = 4;   // Arm offset in data.

const int numChannels   = 16;   // Total number of channels.

const int paramDelta    = 50;   // How much to change parameter.

const int START_STOP = 0x7e;    // Telemetry start and stop byte.
const int BYTESTUFF  = 0x7d;    // Prefix for byte stuffing.
const int STUFF_MASK = 0x20;    // Stuff mask after prefix.

const int BETAFLIGHT_ID = 0x1B; // Betaflight Physical ID.

const int FRSKY_SPORT_PACKET_SIZE = 9;

const int ACCX_FIRST_ID = 0x700;
const int ACCY_FIRST_ID = 0x710;
const int ACCZ_FIRST_ID = 0x720;

enum {
	STATE_DATA_IDLE,
	STATE_DATA_START,
	STATE_DATA_IN_FRAME,
	STATE_DATA_XOR
} dataState;                    // Deframing state machine.

const int MAX_BUFFER = 32;

enum {
    FIRST_CHAR,                 // Standard first char processing.
    ARROW_1,                    // Saw 0x1B in arrow sequence.
    ARROW_2,                    // Saw 0x5B in arrow sequence.
    BUF_COMMAND                 // Saw '!' and not capturing line.
} charState;

static runState_t runState;

static char buffer[MAX_BUFFER];
static int bufIndex = 0;

static uint8_t rxBuf[FRSKY_SPORT_PACKET_SIZE];
static int rxBufCount;

static uint32_t packetCount;    // Count of packets sent.
static uint32_t startTime;      // Start time.
static uint32_t nextSampleTime; // Next time to output sample.
static int      timeoutTicks;   // How long to wait until armed.

static uint16_t throttle;       // Throttle parameter.
static uint16_t direction;      // Left/Right parameter.
static uint16_t forward;        // Forward/Backward parameter.
static uint16_t spin;           // Clockwise/CounterClockwise parameter.

static uint16_t data[numChannels]; // Data channels.

const int debugSize = 100;
static char lastOutput[debugSize];
static bool debugOutput = false;

static void     setDefaultParams();
static void     processCommand();
static void     processSingleChar(char ch);
static void     processBuffer(char *buffer);
static void     startBindAndArm();
static void     processTelemetryByte(uint8_t data);
static void     dumpTelemetry();
static uint16_t limit(uint16_t val);
static void     sendByte(uint8_t b);
static void     sendData();
static void     sendChannelUpdate();
static void     sendPacket();
static bool     nextSample();
static void     help();
static void     debug();

void setup() {
    Serial.begin(115200);

    // We need two stop bits for the 4-in-1 module.
    Serial1.begin(100000, SERIAL_8E2);

    while (!Serial) {
    }
    while (!Serial1) {
    }

    // Serial.println("Running");

    for (int i = 0; i < numChannels; i++) {
        data[i] = 0x0400;
    }

    runState = DISARM;
    startTime = -1;
    packetCount = 0;
    dataState = STATE_DATA_IDLE;
    rxBufCount = 0;
    setDefaultParams();
}

void loop() {
    if (Serial.available()) {
        processCommand();
    }
//    if (Serial1.available()) {
//        processTelemetryByte(Serial1.read());
//    }
    if (nextSample()) {
        if ((packetCount % setupFrameCount) == 0) {
            sendChannelUpdate();
        } else {
            sendPacket();
        }
        packetCount++;
    }
}

static void setDefaultParams() {
    throttle = minValue;
    direction = midValue;
    spin = midValue;
    forward = midValue;
}

static void processCommand() {
    char ch = Serial.read();
    switch (charState) {
        case FIRST_CHAR:
            if (ch == 0x1B) {
                charState = ARROW_1;
            } else if (ch == '!') {
                bufIndex = 0;
                charState = BUF_COMMAND;
            } else {
                processSingleChar(ch);
            }
            break;
        case ARROW_1:
            if (ch == 0x5B) {
                charState = ARROW_2;
            } else {
                charState = FIRST_CHAR;
            break;
        case ARROW_2:
            if (ch == 0x41) {
                processSingleChar('f');
            } else if (ch == 0x42) {
                processSingleChar('b');
            } else if (ch == 0x43) {
                processSingleChar('r');
            } else if (ch == 0x44) {
                processSingleChar('l');
            }
            charState = FIRST_CHAR;
            break;
        case BUF_COMMAND:
            if (ch == '\r' || ch == '\n') {
                buffer[bufIndex++] = '\0';
                processBuffer(buffer);
                charState = FIRST_CHAR;
            } else if (bufIndex < (MAX_BUFFER-1)) {
                buffer[bufIndex++] = ch;
            }
            break;
        }
    }
}

static void processSingleChar(char ch) {
    if (ch == '?') {
        help();
    } else if (ch == 'a') {
        startBindAndArm();
    } else if (ch == 'd') {
        runState = DISARM;
    } else if (ch == 'u') {
        throttle += paramDelta;
    } else if (ch == 'i') {
        throttle -= paramDelta;
    } else if (ch == 'l') {
        direction -= paramDelta;
    } else if (ch == 'r') {
        direction += paramDelta;
    } else if (ch == 'f') {
        forward += paramDelta;
    } else if (ch == 'b') {
        forward -= paramDelta;
    } else if (ch == 'c') {
        spin += paramDelta;
    } else if (ch == 'v') {
        spin -= paramDelta;
    } else if ((ch == '\r') || (ch == '\n')) {
        // Do nothing.
    } else if (ch == 'D') {
        debugOutput = !debugOutput;
    } else {
        Serial.print("Unknown command: '");
        Serial.print(ch);
        Serial.print("' - ");
        Serial.print((ch >> 4) & 0xF, HEX);
        Serial.println(ch & 0xF, HEX);
    }
}

static void processBuffer(char *buffer) {
    char *p;
    throttle = (uint16_t)strtol(buffer, &p, 10);
    direction = (uint16_t)strtol(p, &p, 10);
    forward = (uint16_t)strtol(p, &p, 10);
    spin = (uint16_t)strtol(p, &p, 10);
}

static void startBindAndArm() {
    runState = BIND;
    timeoutTicks = bindTimeOut;
}

static void processTelemetryByte(uint8_t data) {
	switch (dataState) {
	case STATE_DATA_START:
		if (data == START_STOP) {
			dataState = STATE_DATA_IN_FRAME;
			rxBufCount = 0;
		}
        break;
	case STATE_DATA_IN_FRAME:
		if (data == BYTESTUFF) {
			dataState = STATE_DATA_XOR;
		} else if (data == START_STOP) {
                rxBufCount = 0;
		} else if (rxBufCount < FRSKY_SPORT_PACKET_SIZE) {
			rxBuf[rxBufCount] = data;
			rxBufCount += 1;
		}
        break;
	case STATE_DATA_XOR:
		if (rxBufCount < FRSKY_SPORT_PACKET_SIZE) {
			rxBuf[rxBufCount] = data ^ STUFF_MASK;
			rxBufCount += 1;
		}
		dataState = STATE_DATA_IN_FRAME;
        break;
	case STATE_DATA_IDLE:
		if (data == START_STOP) {
			dataState = STATE_DATA_START;
			rxBufCount = 0;
		}
        break;
	}
	if (rxBufCount >= FRSKY_SPORT_PACKET_SIZE) {
		sportProcessPacket();
		dataState = STATE_DATA_IDLE;
		rxBufCount = 0;
	}
}


static void sportProcessPacket() {
    uint8_t physicalID = rxBuf[0];
    if (physicalID != BETAFLIGHT_ID) {
        return;
    }

    uint16_t sensorID = ((uint16_t)rxBuf[3]) << 8 | ((uint16_t)rxBuf[2]);
    int32_t value =
        (((uint32_t)rxBuf[7]) << 24) |
        (((uint32_t)rxBuf[6]) << 16) |
        (((uint32_t)rxBuf[5]) << 8) |
        ((uint32_t)rxBuf[4]);

    if ((sensorID != ACCX_FIRST_ID) &&
        (sensorID != ACCY_FIRST_ID) &&
        (sensorID != ACCZ_FIRST_ID)) {
        return;
    }

    const char* name = "";
    switch (sensorID) {
        case ACCX_FIRST_ID: name = "X"; break;
        case ACCY_FIRST_ID: name = "Y"; break;
        case ACCZ_FIRST_ID: name = "Z"; break;
    }

    Serial.print(millis());
    Serial.print(": ");
    Serial.print(name);
    Serial.print(" ");
    Serial.println(value);
}

static void dumpTelemetry() {
    static int count = 0;

    char ch = Serial1.read();
    Serial.print((ch >> 4) & 0xF, HEX);
    Serial.print(ch & 0xF, HEX);
    Serial.print(" ");
    if ((++count % 16) == 0) {
        Serial.println();
    }
}

static uint16_t limit(uint16_t val) {
    if (val < minValue) {
        val = minValue;
    }
    if (val > maxValue) {
        val = maxValue;
    }
    return val;
}

static void sendByte(uint8_t b) {
    Serial1.write(b);
}

static void sendData() {
    uint32_t bits = 0;
    uint8_t avail = 0;
    for (int channel = 0; channel < numChannels; channel++) {
        uint32_t value = limit(data[channel]);
        bits |= value << avail;
        avail += channelBits;
        while (avail >= 8) {
            sendByte(bits & 0xFF);
            bits >>= 8;
            avail -= 8;
        }
    }
}

static void sendChannelUpdate() {
    sendByte(0x4D);
    sendByte(0x50);
    sendByte(0x80);
    sendByte(0x01);
    sendByte(0x07);
}

static void sendPacket() {
    uint8_t config = 0x4f;
    uint16_t armValue = minValue;
    runState_t nextState = runState;

    switch (runState) {
        default:
        case BIND:
            config |= 0x80;
            armValue = minValue;
            setDefaultParams();
            if (--timeoutTicks < 0) {
                nextState = DISARM_BEFORE_ARM;
                timeoutTicks = disarmTimeOut;
            }
            break;
        case DISARM_BEFORE_ARM:
            armValue = minValue;
            setDefaultParams();
            if (--timeoutTicks < 0) {
                nextState = ARM;
                timeoutTicks = armTimeOut;
            }
            break;
        case ARM:
            armValue = maxValue;
            setDefaultParams();
            if (--timeoutTicks < 0) {
                nextState = RUN;
            }
            break;
        case RUN:
            armValue = maxValue;
            break;
        case DISARM:
            armValue = minValue;
            setDefaultParams();
            break;
    }

    throttle = limit(throttle);
    data[throttleIndex] = throttle;
    direction = limit(direction);
    data[directionIndex] = direction;
    forward = limit(forward);
    data[forwardIndex] = forward;
    spin = limit(spin);
    data[spinIndex] = spin;
    data[armIndex] = armValue;

    sendByte(0x55);
    sendByte(config);
    sendByte(0x03);
    sendByte(0x00);
    sendData();
    if (debugOutput) {
        debug();
    }
    runState = nextState;
}

static bool nextSample() {
    unsigned long now = millis();
    if ((long)startTime < 0) {
        startTime = now;
        nextSampleTime = now;
    }
    if (nextSampleTime <= now) {
        nextSampleTime += msBetweenUpdates;
        return true;
    }
    return false;
}

static void help() {
    Serial.println("Commands:");
    Serial.println(" a -- arm to flight");
    Serial.println(" d -- disarm and stop");
    Serial.println();
    Serial.println(" u    -- up");
    Serial.println(" i    -- down");
    Serial.println(" l, ◀ -- left");
    Serial.println(" r, ▶ -- right");
    Serial.println(" f, ▲ -- forward");
    Serial.println(" b, ▼ -- backward");
    Serial.println(" c    -- clockwise");
    Serial.println(" v    -- counter-clockwise");
    Serial.println();
    Serial.println(" !<throttle> <left/right> <forward/back> <rotation> -- "
                   "command all parameters with values (204 to 1907)");
    Serial.println();
    Serial.println(" D -- toggle debugging output");
    Serial.println();
}

static void debug() {
    const char *stateStr = "";
    switch (runState) {
        default:
        case BIND:              stateStr = "BIND";              break;
        case DISARM_BEFORE_ARM: stateStr = "DISARM_BEFORE_ARM"; break;
        case ARM:               stateStr = "ARM";               break;
        case RUN:               stateStr = "RUN";               break;
        case DISARM:            stateStr = "DISARM";            break;
    }

    char buf[debugSize];
    sprintf(buf, "%s arm:%d throttle:%d direction:%d forward:%d spin:%d",
            stateStr, data[armIndex], data[throttleIndex],
            data[directionIndex], data[forwardIndex], data[spinIndex]);
    if (strcmp(buf, lastOutput) != 0) {
        Serial.println(buf);
        strcpy(lastOutput, buf);
    }
}
