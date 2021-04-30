# clock-in

Clock-in script for JD.com.

## Environment

```bash
pip install -r requirements.txt
```

## Usage

**Instant mode**

```bash
python clock-in.py --username='USERNAME' --password='PASSWORD'
```

**Delay mode**

```bash
# Delay 0.5h and then clock-in
python alive.py --delay=0.5 && python clock-in.py --username='USERNAME' --password='PASSWORD'
```

> Note the first time you running the script, phone authentication (scanning the QR code with JD ME app) is needed.
