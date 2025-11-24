# Draw.io диаграммы

### Создание диаграммы

1. Создайте диаграмму используя [draw.io](https://app.diagrams.net/)
2. Сохраните файл в формате `.drawio` в директорию `diagrams-codes/`
3. Добавьте файл в индексацию git и отправьте в GitHub репозиторий

### Добавление диаграммы в документацию

Для вставки диаграммы используйте синтаксис `@drawio{}` с указанием полного URL файла в GitHub репозитории:

```markdown
<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/IDEF0_A0.drawio"></iframe>
```

**Пример:**
<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/IDEF0_A0.drawio"></iframe>

**Примечание:** Диаграммы будут отображаться как интерактивные iframe в собранной книге. Убедитесь, что файл `.drawio` загружен в репозиторий.