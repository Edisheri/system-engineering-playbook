# Draw.io диаграммы

### Создание диаграммы

1. Создайте диаграмму используя [draw.io](https://app.diagrams.net/)
2. Сохраните файл в формате `.drawio` в директорию `diagrams-codes/`
3. Добавьте файл в индексацию git и отправьте в GitHub репозиторий

### Добавление диаграммы в документацию

Для вставки диаграммы используйте синтаксис `@drawio{}` с указанием полного URL файла в GitHub репозитории:

```markdown
@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/IDEF0_A0.drawio}
```

**Пример:**
@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/IDEF0_A0.drawio}

**Примечание:** Диаграммы будут отображаться как интерактивные iframe в собранной книге. Убедитесь, что файл `.drawio` загружен в репозиторий.