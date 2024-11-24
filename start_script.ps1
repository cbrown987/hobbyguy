# Set variables
$PythonInstallerURL = "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"  # Update URL to latest Python version
$PythonInstallerPath = "$env:TEMP\python-installer.exe"
$ScriptPath = "C:\Path\To\YourScript.py"  # Update to the path of your script
$LogFile = "C:\Path\To\logfile.txt"       # Update to the path of your log file
$ShortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\YourScript.lnk"

# Step 1: Download and Install Python if not already installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Downloading and installing..."
    Invoke-WebRequest -Uri $PythonInstallerURL -OutFile $PythonInstallerPath
    Start-Process -FilePath $PythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item -Path $PythonInstallerPath
    Write-Host "Python installed."
} else {
    Write-Host "Python is already installed."
}

# Step 2: Install Required Python Packages
Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install pillow

# Step 3: Add Python Script to Startup
if (-not (Test-Path $ShortcutPath)) {
    Write-Host "Adding script to startup..."

    # Create a WScript.Shell COM object
    $WScriptShell = New-Object -ComObject WScript.Shell

    # Define the shortcut
    $Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = "cmd.exe"
    $Shortcut.Arguments = "/c start /b python $ScriptPath > $LogFile 2>&1"
    $Shortcut.WorkingDirectory = (Split-Path -Path $ScriptPath)
    $Shortcut.WindowStyle = 7  # Minimized window
    $Shortcut.Save()

    Write-Host "Startup shortcut created at $ShortcutPath."
} else {
    Write-Host "Startup shortcut already exists."
}

# Step 4: Start the Python Script Invisibly
Write-Host "Starting the script..."
$Command = "python $ScriptPath > $LogFile 2>&1"
Start-Process -FilePath "cmd.exe" -ArgumentList "/c start /b $Command" -WindowStyle Hidden

# Step 5: Close PowerShell
Write-Host "Script started and added to startup. Closing PowerShell."
exit
