@ECHO OFF

SET /p startDate= "Enter daily download date yyyy-mm-dd :"

cd C:\Users\FRED\Desktop\OnePortfolio\src\scripts\
C:\Python34\python.exe feedDailyPrice.py %startDate%



