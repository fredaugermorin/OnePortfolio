@ECHO OFF
SET /p action=Daily download(1) or batch(2):

IF %action% == 1 (
SET /p startDate=Enter daily download date yyyy-mm-dd :
python "C:\Users\FRED\Desktop\OnePortfolio\src\scripts\feedDailyPrice.py" %startDate%
)
IF %action% == 2 (
SET /p startDate=Enter download start date yyyy-mm-dd :
SET /p endDate=Enter download end date yyyy-mm-dd :
python "C:\Users\FRED\Desktop\OnePortfolio\src\scripts\feedDailyPrice.py" %startDate% %endDate%
)




