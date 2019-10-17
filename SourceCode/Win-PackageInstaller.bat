@echo  -- make sure you have --
@echo 	- python 3 (3.7 prefered)
@echo.
@echo off
SET /p confirm="Please Confirm that you have python 3 installed (y/n)? "
IF /i "%confirm%" == "y" (
python -m pip install --upgrade pip
pip3 install -U PySide2 --user
pip3 install -U mysql-connector-python --user
PAUSE
) ELSE IF /i "%confirm%" == "n" (
@echo Canceling Setup...
SET /p msg = "Please Hit Enter To Finish Cancel..."
)
if 1 == 2 (
setx "%path%;%userprofile%\AppData\Roaming\Python\Python37\Scripts\"
)