@echo off
echo This will compose the ocr-frontend Docker image on your local machine.
echo Do you want to compose the docker image? (Y/N)
echo.
set /p userinput=
echo.

if /I "%userinput%"=="Y" (
    echo YES: Docker image will now compose.
    echo.
    
    docker-compose up --build -d

    echo.
    echo =================================================
    echo If no errors, Docker image composed successfully.
    echo.
    echo Container 'ocr-frontend' should now be running. If not, manually start/run 'ocr-frontend'.
    echo.
    echo Access frontend via http://localhost:9001 or http://127.0.0.1:9001
    echo Installer will now quit.
    echo.
    pause
    exit /b

) else if /I "%userinput%"=="N" (
    echo NO: You chose to quit.
    echo.
    pause
    exit /b
) else (
    echo Invalid choice. Please run the script again and choose Y or N.
    echo.
    pause
    exit /b
)

echo.
pause