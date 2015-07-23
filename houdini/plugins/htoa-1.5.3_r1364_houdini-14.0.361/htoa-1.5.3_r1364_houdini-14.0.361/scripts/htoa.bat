REM Sample batch script to lauch Houdini with HtoA enabled


REM Edit these to suit your environment
SET HOME=C:\projects\HTOA\local\
SET ARNOLD_ROOT=C:\SolidAngle\Arnold-4.0.3.0-win64
SET HOUDINI_ROOT="C:\Program Files\Side Effects Software\Houdini 12.0.558"
SET PATH="%PATH%;%ARNOLD_ROOT%\bin
SET PYTHONPATH=%PYTHONPATH%;%ARNOLD_ROOT%\python
REM Launch Houdini
SET HOUDINI_CONSOLE_LINES=4000
%HOUDINI_ROOT%\bin\hmaster.exe