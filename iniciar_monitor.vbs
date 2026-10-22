Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

WshShell.CurrentDirectory = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "python.exe monitor.py", 0, False