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
PWM server initialization
"""
import argparse
import os
import socket
from logging.config import fileConfig

from setproctitle import setproctitle

fileConfig("pwm/logging_config.ini")

setproctitle("PWM")

parser = argparse.ArgumentParser()
parser.add_argument("--duty", type=int, choices=range(0, 101), default=75)
parser.add_argument("--pwm-pin", type=int, default=27)
args = parser.parse_args()

PWM_PIN = args.pwm_pin
DUTY = args.duty

PIPE = "/var/run/pwm_pipe"
if os.path.exists(PIPE):
	os.remove(PIPE)

SERVER = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
SERVER.bind(PIPE)
os.chmod(PIPE, 0o666)
