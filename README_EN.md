# SNNU Campus Network Authentication Script

This project is a Windows script for SNNU campus network login.  
It first disconnects the current session, then sends a new login request.  
It can avoid the trouble caused by manual login every time.

## Notes First

1. The account and password are written in `connect.py`.
2. Change your own account info before you test it.
3. If the school login address changes, update the address in the script too.  
   In most cases, the address does not change. Only the port may change, for example `8601` to `8602`.

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
password = '''xxxxxxxx'''
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

## Auto Start After Windows Login

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
5. If your system supports `Delay task for`, you can turn it on
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

### 3. I want to move the folder

You only need to update these two paths:

1. The `connect.py` path in `run.bat`
2. The `run.bat` path in Task Scheduler

## Note

This script is small.  
It is good for basic authentication.  
If the school portal changes, you may need to update the script again.
