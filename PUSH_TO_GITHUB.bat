@echo off
chcp 65001 >nul
echo ========================================
echo FORCE PUSH В GITHUB РЕПОЗИТОРИЙ
echo ========================================
echo.

cd /d "c:\Users\umys1\Music\инженерия\system-engineering-playbook"

echo Шаг 1: Проверка remote...
git remote -v
echo.

echo Шаг 2: Добавление всех файлов...
git add -A
echo.

echo Шаг 3: Создание коммита...
git commit -m "Initial commit: полный репозиторий" --allow-empty
echo.

echo Шаг 4: Force push в GitHub...
git push -u origin main --force
echo.

echo ========================================
echo ПРОВЕРЬТЕ РЕЗУЛЬТАТ НА GITHUB
echo https://github.com/Edisheri/syst
echo ========================================
pause
