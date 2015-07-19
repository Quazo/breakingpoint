Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c start_houdini_sandbox.bat"
oShell.Run strArgs, 0, false