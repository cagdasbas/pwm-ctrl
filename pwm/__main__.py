#!/bin/env python3
#  Copyright (c) 2023.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""
PWM server main
"""
import logging
import os
import signal
import socket
import threading

from RPi import GPIO

from pwm import DUTY, PWM_PIN, SERVER, PIPE

logging.info("initial duty will be set to %d", DUTY)

stop_bit = threading.Event()


def exit_gracefully(signum, _):
	"""
	Exit gracefully when a signal is received.
	:param signum: The signal number
	:param _: The stack frame
	"""
	logging.info("Received signal %s, exiting gracefully", signal.strsignal(signum))
	stop_bit.set()


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

GPIO.setmode(GPIO.BCM)

GPIO.setup(PWM_PIN, GPIO.OUT)

GPIO.setwarnings(False)
pwm = GPIO.PWM(PWM_PIN, 25000)
pwm.start(0)

pwm.ChangeDutyCycle(DUTY)

SERVER.settimeout(2)
SERVER.listen(1)

logging.info("Listening on %s", PIPE)
while not stop_bit.is_set():
	try:
		connection, _ = SERVER.accept()
	except socket.timeout:
		continue

	try:
		data = connection.recv(1024).decode('utf-8').strip()
		logging.debug("Received data: %s", data)
		if data:
			try:
				value = int(data)
				if 0 <= value <= 100:
					logging.info("Setting duty cycle to %d", value)
					pwm.ChangeDutyCycle(value)
			except ValueError:
				logging.debug("Received invalid value: %s", data)
	finally:
		logging.debug("Closing connection")
		connection.close()

logging.info("Stopping PWM")
pwm.stop()
GPIO.cleanup()
SERVER.close()
os.remove(PIPE)
logging.info("Exiting")
