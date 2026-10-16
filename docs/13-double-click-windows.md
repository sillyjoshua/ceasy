# Windows setup

1. Download the latest **Ceasy Windows bundle** from the [releases page](https://github.com/sillyjoshua/ceasy/releases/latest).
2. Extract the ZIP to a temporary folder.
3. Double-click `install-windows.bat` once. You do not need to run it as Administrator.
4. The installer copies `ceasy.exe` to `%LOCALAPPDATA%\Programs\Ceasy`, adds that folder to your **user PATH**, and registers the `.ce` and `.ceasy` file associations.
5. Open a **new** Command Prompt or PowerShell window so it receives the updated PATH.

You can now run Ceasy from any folder:

```powershell
ceasy yourfile.ceasy
ceasy yourfile.ce
```

You can also double-click a `.ce` or `.ceasy` file. The installed executable is stored separately from the extracted ZIP, so you can delete the extracted folder after installation.

## PATH safety

The installer edits the current user's PATH using the Windows/.NET environment API. It does **not** use `setx PATH`, which can truncate long PATH values. Existing PATH entries are preserved, and the Ceasy folder is only added if it is not already present.

The installer is per-user and does not require administrator permissions. If you want to uninstall Ceasy, remove `%LOCALAPPDATA%\Programs\Ceasy` and remove that folder from your user PATH.
