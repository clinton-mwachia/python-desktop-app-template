# Desktop Application Template

This is a Python-based desktop application template using Tkinter for the GUI and MongoDB for data storage. The application includes user authentication, a dashboard, and features to manage tasks (todos) and users.

## Features

- User Authentication: Register, login, and manage user sessions securely.
- Dashboard: A user-friendly dashboard displaying tasks and user information.
- Task Management: Create, view, edit, and delete tasks. Tasks are associated with users, ensuring each user sees only their own tasks.
- User Profile: View and update user profiles, including the ability to change the password with confirmation of the old password.
- Notifications: The GUI is designed to be display notifications to the user when CRUD operations are done to the tasks.
- Settings: The GUI provides a section for updating settings of the app.

## Project Structure

```
├── auth/
│   ├── auth.py          # Handles user authentication (login, registration, etc.)
├── utils/
│   ├── database.py      # MongoDB connection and operations
│   └── logger.py        # Logger setup for the
├── models/
|   |── todo.py          # Todo models
|   └── user.py          # User models
├── views/
│   ├── login.py         # Login view
│   ├── register.py      # Register view
│   ├── dashboard.py     # Dashboard view
│   ├── todo.py          # Todo view
│   ├── user.py          # User view
│   ├── notification.py  # Notification view
│   ├── logs.py          # logs view
│   └── profile.py       # User profile view
├── main.py              # Entry point for the application
└── README.md            # This file

```

## Installation

### Prerequisites

- Python 3.8+
- MongoDB

### Setup

1. Clone the repository:

```bash
git clone https://github.com/clinton-mwachia/desktop-app-template.git
cd desktop-app-template
```

## NOTE

- If you are running the code using cmd on vscode, use _py_ followed by other commands.
- Use _python_ follwed by other commands on CMD.

2. Install the required packages:

```bash
py pip install -r requirements.txt
```

3. Start the MongoDB server (if not already running).

4. Run the application:

```bash
py main.py
```

## Compiling to an Executable

You can compile the Python application into a standalone executable using `PyInstaller`. This allows the app to run on machines without Python installed.

### Steps to Compile

1. Navigate to the project directory and run the following command to create a standalone executable:

```bash
py -m pyInstaller --onefile --windowed main.py
```

- `--onefile`: Packages the application into a single executable file.
- `--windowed`: Suppresses the console window (useful for GUI applications).

3. After running the command, you’ll find the executable in the `dist` folder inside your project directory.

### Additional Tips

- You can customize the executable by adding an icon with the `--icon` option:

```bash
py -m pyInstaller --onefile --windowed --icon=path_to_icon.ico main.py
```

- If your application requires external files (e.g., images, configuration files), you may need to adjust the `PyInstaller` spec file or manually copy these files to the appropriate directory after building the executable.

# Make the app installable on windows

## Step 1: Prepare Your Application

Make sure your application is working correctly and all dependencies are working

## Step 2: Use PyInstaller to Create an Executable

### 1. Install PyInstaller

First, you need to install PyInstaller if you haven't already:

```bash
py -m pip install pyinstaller
```

### 2. Create a PyInstaller Spec File

PyInstaller uses a spec file to know how to build your executable. You can customize this file to include additional files or directories.

Run PyInstaller to generate an initial spec file and executable:

```bash
py -m pyinstaller --onefile --noconsole main.py
```

This will generate the following files and folders:

- dist/: Contains the final executable.
- build/: Contains build files used by PyInstaller.
- main.spec: The spec file describing the build.

You might want to customize the `.spec` file if you need to include extra data files, icons, or need special startup scripts.

### 3. Customize the Spec File

Here is custom `main.spec`

```
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

To add additional data files like images, themes, or text files, you can modify the `datas` section:

```python
datas=[
    ('position.txt', '.'),  # Include position.txt file
    ('themes/', 'themes/'),  # Include a themes folder
]
```

### 4. Run PyInstaller with Spec File

After customizing your `.spec` file, run PyInstaller again:

```bash
py -m pyinstaller main.spec
```

This will create the executable in the `dist/main.exe` folder.

## Create a Windows Installer with Inno Setup

Inno Setup is a free installer for Windows programs. It’s easy to use and widely supported.

### 1. Download and Install Inno Setup

You can download Inno Setup from the official website: [Inno Setup](https://jrsoftware.org/isinfo.php)

### 2. Create an Inno Setup Script

Create a new script file (`main.iss`) for your installer with the following content:

```ini
; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "main"
#define MyAppVersion "1.0"
#define MyAppPublisher "Clinton Moshe"
#define MyAppURL "http://example.com"
#define MyAppExeName "main.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{8B5D708F-9E7B-4C53-AC1A-9C83AFAF7B5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename=mainSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram, {#MyAppName}}"; Flags: nowait postinstall skipifsilent
```

### 3. Customize the Script

You can customize the script to suit your application’s needs:

- AppName: Set to the name of your application.
- AppVersion: Set to your application's version.
- AppPublisher: Your name or organization.
- AppExeName: The name of the executable file (`main.exe`).
- OutputBaseFilename: The name of the setup file.

### 4. Compile the Installer

1. Open Inno Setup and load your script (`main.iss`).
2. Click the Compile button (or press F9).

This will generate a `mainSetup.exe` file in the `Output` directory specified in the script. This setup file is the installer for your application.

## Step 4: Test the Installer

1. Run the Installer: Double-click the `mainSetup.exe` file to run the installer.
2. Follow the Setup Wizard: Follow the steps in the wizard to install your application.
3. Verify Installation: After installation, ensure that your application launches correctly and the shortcuts are created as expected.

## Advanced Features

Inno Setup allows you to add advanced features such as:

- Custom Icons: Use custom icons for your installer and shortcuts.
- Registry Entries: Modify or add registry entries.
- Auto-Start: Automatically start the application after installation.
- Uninstaller: Include an uninstaller to remove the application.
- License Agreement: Display a license agreement during installation.

### how you can add a license agreement:

```ini
[License]
LicenseFile=license.txt
```

## Usage

### Registering a User

Upon starting the application, the user will be prompted to register. After successful registration, the application will automatically transition to the login view.

### Logging In

Existing users can log in using their credentials. Upon successful login, the application will display the dashboard.

### Managing Tasks

From the dashboard, users can create, view, edit, and delete their tasks. The tasks are displayed in a table, with the most recent tasks appearing at the top.

### Profile Management

Users can view their profile, update details, and change their password. The profile view is centered, with the user’s image on the left and details on the right.

## Customization

- Database Configuration: Modify the `utils/database.py` file to configure MongoDB settings.
- UI Adjustments: Adjust the Tkinter UI components in the `views/` directory to match your design preferences.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the Appache License. See the `LICENSE` file for more details.

_Happy coding!_
