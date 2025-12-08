# Инструкция для ручного push в GitHub

## Проблема
Автоматический push не работает из-за необходимости аутентификации GitHub.

## Решение - выполните команды вручную:

### 1. Откройте PowerShell или CMD в папке проекта:
```powershell
cd "c:\Users\umys1\Music\инженерия\system-engineering-playbook"
```

### 2. Проверьте настройки remote:
```powershell
git remote -v
```
Должно показать: `origin  https://github.com/Edisheri/syst.git`

### 3. Добавьте все файлы и создайте коммит:
```powershell
git add -A
git commit -m "Initial commit: полный репозиторий system-engineering-playbook"
```

### 4. Выполните push:
```powershell
git push -u origin main --force
```

### 5. При запросе аутентификации:
- Если используете HTTPS: введите ваш GitHub username и Personal Access Token (не пароль!)
- Если используете SSH: убедитесь, что SSH ключ добавлен в GitHub

### Альтернатива: Используйте GitHub Desktop или другой GUI клиент

## Создание Personal Access Token (если нужно):
1. Зайдите на GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Создайте новый token с правами `repo`
3. Используйте этот token вместо пароля при push
