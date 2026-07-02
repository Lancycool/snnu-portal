# SNNU Campus Network Authentication Script

[中文](README.md) | English

This project is a Windows and Ubuntu script for SNNU campus network login.  
It first disconnects the current session, then sends a new login request.  
It can avoid the trouble caused by manual login every time.

## Quick Links

1. [Wired Network Auto Start](#wired-network)
2. [Laptop WiFi Auto Start](#wifi-network)
3. [Ubuntu Auto Start After Login](#ubuntu-autostart)

## Notes First

1. The account and password are written in `connect.py`.
2. Change your own account info before you test it.
3. If the school login address changes, update the address in the script too.  
   In most cases, the address does not change. Only the port may change, for example `8601` to `8602`.
4. This script is mainly designed for a desktop PC or a wired network. After Windows login, the wired network is usually ready, so the `At log on` trigger is enough.
5. If you use a laptop with SNNU WiFi, you should add another trigger. This trigger runs the script after Windows connects to WiFi.
6. If you use Ubuntu, do not use `run.bat`. You need to run the script with `python3` and use `systemd` for auto start after login.

## Requirements

You need to install:

1. Python 3
2. The `requests` package

Install `requests` with:

```bash
pip install requests
```

If you have more than one Python installation, use:

```bash
python -m pip install requests
```

## Script Setup

Open `connect.py` and change these parts:

### 1. Account

```python
account = 'xxxxxxxx'
```

Replace it with your student ID or network account.

### 2. Password

```python
password = 'xxxxxxxx'
```

Replace it with your campus network password.

### 3. Connection Type

```python
method = ''
```

Set this value by network provider:

1. Leave it blank for the default campus network
2. Use `unicom` for China Unicom
3. Use `mobile` for China Mobile
4. Use `telecom` for China Telecom
(Fill in between the two single quotes)

### 4. Campus Network Address

The login address is already in the script.  
If the port is not working, try changing `8601` to `8602`.  
You may need to update these two values:

```python
url = 'http://202.117.144.205:8601/snnuportal/login'
end_url = 'http://202.117.144.205:8601/snnuportal/logoff'
```

## BAT File Setup

The current `run.bat` file is:

```bat
@echo off
start/min "" pythonw "E:\Projects\Portal\connect.py"
```

The path is an absolute path to `connect.py`.  
If you move the project to another folder, change this path to your own real path.

Example:

```bat
start/min "" pythonw "D:\mycode\Portal\connect.py"
```

### Why `pythonw`

`pythonw` runs without opening a black command window.  
That makes the login process quieter after Windows starts.

## Manual Run

You can double-click `run.bat` first.  
If the script works, it will try to disconnect and connect again.

You can also run the Python file directly:

```bash
python connect.py
```

<a id="wired-network"></a>

## Auto Start After Windows Login: Wired Network

The most stable method is Windows Task Scheduler.  
This lets the script run automatically after you log in to Windows.

### Goal

1. Run automatically after Windows login
2. Start after a short delay of about 2 to 4 seconds
3. No need to click the BAT file by hand

### Step 1: Open Task Scheduler

1. Press `Win + S`
2. Search for `Task Scheduler`
3. Open it

### Step 2: Create a New Task

1. Click `Create Task` on the right side
2. Do not click `Create Basic Task`
3. `Create Task` gives you more control

### Step 3: Fill in the General Tab

1. Set the name to something like `AutoConnect`
2. Add a note in the description if you want
3. Select `Run only when user is logged on`
4. Check `Run with highest privileges`

If this is your own computer, these settings are enough.  
If you do not want a window to stay open, you can keep the default options.

### Step 4: Set the Trigger

1. Open the `Triggers` tab
2. Click `New`
3. Set `Begin the task` to `At log on`
4. Choose your Windows user
5. If your system supports `Delay task for`, you can turn it on, fill in 2 to 4 seconds (manually change after selecting 30 seconds)
6. Many computers only support minute-level delay here, so do not rely on this alone

If you want the script to run about 2 to 4 seconds after login, the safest way is to let `run.bat` wait for 3 seconds first.  
Then Task Scheduler only starts the batch file after login, and the batch file controls the exact wait time.

7. Click `OK`

### Step 5: Set the Action

1. Open the `Actions` tab
2. Click `New`
3. Set `Action` to `Start a program`
4. In `Program/script`, enter `cmd.exe`
5. In `Add arguments`, enter:

```bat
/c "E:\Projects\Portal\run.bat"
```

If your `run.bat` is in another folder, change it to your own absolute path.  
If the path contains spaces, keep the quotes.

6. Click `OK`

Or you can directly click "Browse" in step 4 to select the 'run.bat' and click "OK" directly

### Step 6: Set Conditions

You can keep this tab as it is.  
If you want better stability on a laptop, you can clear these options:

1. `Start the task only if the computer is on AC power`
2. `Stop if the computer switches to battery power`

If you use a laptop, this can help avoid power-related issues.

### Step 7: Set Settings

You can keep the default values here.  
Useful optional options are:

1. `Allow task to be run on demand`
2. `If the task fails, restart every`

If you do not want to change much, leave it alone.

### Step 8: Save and Test

1. Click `OK` to save the task
2. If Windows asks for a password, enter your current Windows account password
3. Go back to Task Scheduler and find the task you just created
4. Right-click it
5. Click `Run`

If everything is correct, the script will run.  
You can also sign out and sign in again to see whether it starts by itself.

<a id="wifi-network"></a>

## Auto Start on Laptop WiFi

If you use a laptop with SNNU WiFi, Windows may not connect to WiFi immediately after login.  
If you only use the `At log on` trigger, the script may run too early.  
You can add another trigger that runs after WiFi is connected.

### When to Use This

1. You use a laptop
2. You mainly use SNNU WiFi
3. You want the script to run after WiFi is connected

### Step 1: Let Windows Connect to SNNU WiFi Automatically

1. Click the network icon in the bottom-right corner
2. Find the school WiFi, such as `SNNU`
3. Check `Connect automatically`
4. Connect to the WiFi once by hand

Then Windows can connect to WiFi by itself next time.  
After that, Task Scheduler can start the script when WiFi is connected.

### Step 2: Open Task Scheduler

1. Press `Win + S`
2. Search for `Task Scheduler`
3. Open it

### Step 3: Edit the Existing Task

If you already created the task for wired network login, edit that task.  
If you have not created it yet, create a new task.  
The `General` and `Actions` settings can stay the same as the wired network setup above.

### Step 4: Create a WiFi Trigger

1. Open the `Triggers` tab
2. Click `New`
3. Set `Begin the task` to `On an event`
4. In `Settings`, choose `Custom`
5. Click `New Event Filter`
6. Open the `XML` tab
7. Check `Edit query manually`
8. If Windows shows a warning, click `Yes`

Paste this XML:

```xml
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
    <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
      *[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and (EventID=8001)]]
    </Select>
  </Query>
</QueryList>
```

This event means Windows has connected to a WiFi network.  
The script will run after the wireless connection is ready.

### Step 5: Run Only After Connecting to SNNU WiFi

If you do not want the script to run after connecting to any WiFi, use this version.  
Change `SNNU` to your real school WiFi name.

```xml
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
    <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
      *[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and (EventID=8001)]]
      and
      *[EventData[Data[@Name='SSID']='SNNU']]
    </Select>
  </Query>
</QueryList>
```

If you are not sure whether the WiFi name is exactly `SNNU`, use the first version without SSID filtering first.  
It is easier to make it work.

### Step 6: Set the Action

The `Actions` tab still uses the same setting:

```bat
/c "E:\Projects\Portal\run.bat"
```

If your `run.bat` is in another folder, change it to your own absolute path.

### Step 7: Save and Test

1. Save the task
2. Disconnect WiFi
3. Connect to SNNU WiFi again
4. Wait about 2 to 4 seconds
5. Check whether the script runs automatically

If it does not run, check the WLAN event log first.

The path is:

```text
Right-click the window icon -> Event Viewer -> Applications and Services Logs -> Microsoft -> Windows -> WLAN-AutoConfig -> Operational
```

The event ID should be `8001`.  
If this log has no records, right-click `Operational` and choose `Enable Log`.

<a id="ubuntu-autostart"></a>

## Ubuntu Auto Start After Login

Do not use `run.bat` on Ubuntu.  
You need to run `connect.py` directly.  
The recommended method is `systemd --user`. It runs the script after the user logs in to Ubuntu.

### Step 1: Install Requirements

Install Python and `requests` first:

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 -m pip install requests
```

If the system does not allow direct `pip` installation, use:

```bash
sudo apt install python3-requests
```

### Step 2: Confirm the Script Path

Assume you put this project here:

```bash
/home/yourname/Portal
```

Then the full path of `connect.py` is:

```bash
/home/yourname/Portal/connect.py
```

Change `yourname` in the examples to your real Ubuntu username.

### Step 3: Test Manually

Enter the project folder first:

```bash
cd /home/yourname/Portal
```

Run the script:

```bash
python3 connect.py
```

If the script works, continue with the auto start setup.

### Step 4: Create a systemd User Service

Create the user service folder:

```bash
mkdir -p ~/.config/systemd/user
```

Create the service file:

```bash
nano ~/.config/systemd/user/snnu-portal.service
```

Write this content into the file:

```ini
[Unit]
Description=SNNU Campus Network Auto Login
After=network-online.target

[Service]
Type=oneshot
ExecStartPre=/bin/sleep 5
ExecStart=/usr/bin/python3 /home/yourname/Portal/connect.py

[Install]
WantedBy=default.target
```

You must change `/home/yourname/Portal/connect.py` to your real path.  
`ExecStartPre=/bin/sleep 5` means the service waits 5 seconds after login.  
If your network connects slowly, change `5` to `10`.

Press `Ctrl + O`, then press Enter to save.  
Press `Ctrl + X` to exit.

### Step 5: Enable Auto Start

Reload user services:

```bash
systemctl --user daemon-reload
```

Enable the service:

```bash
systemctl --user enable snnu-portal.service
```

Test it now:

```bash
systemctl --user start snnu-portal.service
```

Check the status:

```bash
systemctl --user status snnu-portal.service
```

If there is no clear error in the status output, the service can run.

### Step 6: Reboot and Test

You can reboot Ubuntu:

```bash
reboot
```

After you log in, the service will run the script once.

### If Ubuntu Uses WiFi

If you use WiFi, the network may not be ready right after login.  
You can increase the wait time:

```ini
ExecStartPre=/bin/sleep 10
```

If you want the script to run every time the network connects, you can use NetworkManager dispatcher.  
That method is better for WiFi, but it is more system-level.  
For a personal computer, `systemd --user` with a longer wait time is usually enough.

## Let It Wait a Few Seconds

If you want a more stable 3-second delay, change `run.bat` to this:

```bat
@echo off
timeout /t 3 /nobreak >nul
start "" /min pythonw "E:\Projects\Portal\connect.py"
```

The `3` means 3 seconds.  
You can change it to `2`, `3`, or `4`.

This is more accurate than relying only on Task Scheduler.

## Common Problems

### 1. Nothing happens

Check these first:

1. Python is installed
2. `requests` is installed
3. The path in `run.bat` is correct
4. The account and password in `connect.py` are correct

### 2. It does not start after login

Check these in Task Scheduler:

1. The trigger is `At log on`
2. The delay is set correctly
3. The action points to the correct `run.bat`
4. The task was saved successfully

If you use laptop WiFi, also check these:

1. Windows has connected to SNNU WiFi automatically
2. The WiFi trigger uses event ID `8001`
3. The `WLAN-AutoConfig/Operational` log is enabled

### 3. I want to move the folder

You only need to update these two paths:

1. The `connect.py` path in `run.bat`
2. The `run.bat` path in Task Scheduler

## Note

This script is small.  
It is good for basic authentication.  
If the school portal changes, you may need to update the script again.
