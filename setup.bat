@echo off
REM CloudMind AI Setup Script for Windows
REM This script helps set up the development environment on Windows

setlocal enabledelayedexpansion

echo ==================================
echo CloudMind AI Setup
echo ==================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo X Docker is not installed. Please install Docker Desktop first:
    echo    https://docs.docker.com/desktop/install/windows-install/
    exit /b 1
)

REM Check if Docker Compose is installed
docker compose version >nul 2>&1
if errorlevel 1 (
    echo X Docker Compose is not installed. Please install Docker Desktop first:
    echo    https://docs.docker.com/desktop/install/windows-install/
    exit /b 1
)

echo V Docker and Docker Compose are installed
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env >nul
    echo V .env file created
    echo.
    echo WARNING: Edit the .env file to add your cloud provider credentials
    echo    before running the application with actual cloud resources.
    echo.
) else (
    echo V .env file already exists
    echo.
)

REM Create credentials directory if it doesn't exist
if not exist credentials (
    echo Creating credentials directory...
    mkdir credentials
    echo V credentials directory created
    echo.
)

REM Ask user what they want to do
echo What would you like to do?
echo 1) Start in production mode (optimized, no hot-reload)
echo 2) Start in development mode (with hot-reload)
echo 3) Run tests
echo 4) Build Docker images only
echo 5) Stop all services
echo 6) Clean up (remove containers, images, volumes)
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Starting CloudMind AI in production mode...
    docker compose up -d --build
    echo.
    echo V CloudMind AI is running!
    echo   API: http://localhost:8000
    echo   API Docs: http://localhost:8000/docs
    echo.
    echo To view logs: docker compose logs -f
    echo To stop: docker compose down
) else if "%choice%"=="2" (
    echo.
    echo Starting CloudMind AI in development mode...
    docker compose -f docker-compose.dev.yml up --build
    echo.
    echo V CloudMind AI is running in development mode!
    echo   API: http://localhost:8000
    echo   API Docs: http://localhost:8000/docs
    echo   Changes to source code will trigger auto-reload
) else if "%choice%"=="3" (
    echo.
    echo Running tests...
    docker compose -f docker-compose.dev.yml up --build cloudmind-test
) else if "%choice%"=="4" (
    echo.
    echo Building Docker images...
    docker compose build
    docker compose -f docker-compose.dev.yml build
    echo V Docker images built successfully
) else if "%choice%"=="5" (
    echo.
    echo Stopping all services...
    docker compose down
    docker compose -f docker-compose.dev.yml down
    echo V All services stopped
) else if "%choice%"=="6" (
    echo.
    echo Cleaning up...
    set /p confirm="This will remove all containers, images, and volumes. Continue? (y/N): "
    if /i "!confirm!"=="y" (
        docker compose down -v --rmi all
        docker compose -f docker-compose.dev.yml down -v --rmi all
        echo V Cleanup complete
    ) else (
        echo Cleanup cancelled
    )
) else (
    echo Invalid choice. Exiting.
    exit /b 1
)

endlocal
