# B&S-Server-Manager

https://raw.githubusercontent.com/war100ck/BNS-Server-Manager-v03/main/screen/logo.png

A powerful GUI tool for managing Blade & Soul game servers with multi-language support and advanced features.

https://raw.githubusercontent.com/war100ck/BNS-Server-Manager-v03/main/screen/bsm.png
---

## Features

- **Multi-language Interface:** Russian, English, Portuguese (Brazil)
- **Daemon Management:** Add, edit, delete, and reorder server daemons
- **Smart Auto-detection:** Automatically detects server daemons in correct startup order
- **Window Management:** Minimize/show server windows (requires pywin32)
- **Start Minimized:** Option to start daemons minimized
- **Batch Operations:** Start/stop all daemons or selected ones
- **Status Monitoring:** Real-time status checking
- **Configuration Saving:** All settings saved in `bns_config.json`
- **Execution Log:** Detailed log of all operations

---

## Installation

### Option 1: Using Pre-built EXE

1. Download the latest release  
2. Place `BNS_Server_Manager.exe` and `bns_config.json` in the same folder  
3. Run `BNS_Server_Manager.exe`

### Option 2: Build from Source

1. Install **Python 3.8 or higher**
2. Install dependencies:

```bash
pip install pyinstaller
pip install pywin32  # Optional, for window management features
```

3. Build the executable:

```bash
pyinstaller --onefile --windowed --name "BNS Server Manager" --icon=icon.ico bns_manager.py --add-data "bns_config.json;."
```

The executable will be in the **dist** folder.

---

## First Run Setup

- **Set Server Path:** On first run, you'll be prompted to select your BNS server folder
- **Configure Daemons:**  
  - Add manually via **Add Daemon**  
  - Or use **Auto-detect** to automatically add daemons in correct order
- **Adjust Settings:** Configure delays, minimization preferences, etc.

---

## Recommended Startup Order

```
CacheDaemon
CacheGate
AccountInventoryDaemon
RankingDaemon
PostOfficeDaemon
LobbyDaemon
MarketDealerDaemon
MarketAgent
ArenaLobby
AchievementDaemon
DuelBotDaemon
GameDaemon (with 5-second delay)
```

---

## Keyboard Shortcuts

- **Double-click daemon:** Start selected daemon  
- **Right-click daemon:** Context menu  
- **F5:** Refresh daemon list  

---

## Context Menu Options

- ▶ Start / ⏹ Stop / 🔄 Restart  
- ✏️ Edit / 🗑️ Delete  
- ↑ Move Up / ↓ Move Down  
- 🔽 Minimize / 🔼 Show (with pywin32)  
- 📋 Copy path  

---

## Window Management Features

Requires **pywin32**:

- Minimize/show all daemon windows  
- Minimize/show selected daemon windows  
- Start daemons minimized  
- Control window visibility via toolbar buttons  

---

## Configuration

All settings are stored in **bns_config.json**:

- Server path  
- Daemon configurations  
- Interface language  
- Window positions  
- Minimization preferences  

---

## Troubleshooting

### "File not found" errors

- Verify server path is correctly set  
- Ensure .exe files exist in specified paths  

### Window management not working

- Install pywin32  
- Run as administrator if required  

### Daemons not starting

- Check antivirus restrictions  
- Verify working directory permissions  

---

## Requirements

- Windows 7/10/11  
- Python 3.8+ (for building from source)  
- BNS server files  
- Optional: pywin32  

---

## Building from Source

1. Clone or download the repository  
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Build:

```bash
pyinstaller --onefile --windowed --name "BNS Server Manager" --icon=icon.ico bns_manager.py --add-data "bns_config.json;."
```

---

## Files Structure

```
BNS Server Manager/
├── BNS_Server_Manager.exe  # Main executable
├── bns_config.json         # Configuration file
├── icon.ico                # Application icon
└── README.md               # This file
```

---

## Support

- Check execution log for error details  
- Verify all file paths  
- Ensure you have necessary permissions  

---

## License

Free to use for BNS server management.

---

## Credits

Created by **WAR100CK**

---

**Note:** This tool is for managing BNS private servers only. Ensure you have proper rights to run the server files.
