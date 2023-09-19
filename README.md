## pwm control for rpi nas fan

This is a simple script to control a pwm fan my raspberry pi nas.

The initial value is set to 75% and located in `pwm.env` file.
PWM pin is set to 27 and can be changed in `pwm.env` file.

You can control fan speed with `pwmctl`

```shell
pwmctl 75
```

### Installation

1. Clone this repository

```shell
cd /opt
git clone https://github.com/cagdasbas/pwm-ctrl.git pwm
```

2. Create a virtual environment and install requirements

```shell
cd /opt/pwm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Copy the service file to systemd and copy env file

```shell
cp service/pwm.service /etc/systemd/system/
cp service/pwm.env /etc/sysconfig/
```

5. Copy ctrl script to /usr/local/bin

```shell
cp scripts/pwmctl /usr/local/bin/
```

4. Enable and start the service

```shell
systemctl enable --now pwm.service
```