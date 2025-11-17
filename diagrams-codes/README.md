# Коды диаграмм для Draw.io и PlantUML

## 📁 Структура файлов

### IDEF0 (Draw.io XML)
- `IDEF0_A0.drawio` - Контекстная диаграмма A0
- `IDEF0_DECOMPOSITION.drawio` - Декомпозиция A0 → A1-A4
- `IDEF0_A1.drawio` - Функция A1: Приём данных
- `IDEF0_A2.drawio` - Функция A2: Препроцессинг
- `IDEF0_A3.drawio` - Функция A3: ИИ-анализ
- `IDEF0_A4.drawio` - Функция A4: Формирование отчёта

### IDEF3 (Draw.io XML)
- `IDEF3_OVERVIEW.drawio` - Обзор процесса
- `IDEF3_P1.drawio` - Процесс P1: Регистрация
- `IDEF3_P2.drawio` - Процесс P2: Загрузка данных
- `IDEF3_P3.drawio` - Процесс P3: GPU-обработка
- `IDEF3_P4.drawio` - Процесс P4: Логирование

### DFD (Draw.io XML)
- `DFD_OVERVIEW.drawio` - Обзор потоков данных
- `DFD_P1.drawio` - Процесс P1: Приём данных
- `DFD_P2.drawio` - Процесс P2: Валидация
- `DFD_P3.drawio` - Процесс P3: ИИ-анализ
- `DFD_P4.drawio` - Процесс P4: Логирование

### UML (PlantUML)
- `UML_REGISTRATION_*.puml` - 6 диаграмм для регистрации (1-6)
- `UML_DATA_UPLOAD_*.puml` - 6 диаграмм для загрузки данных (1-6)
- `UML_IMAGE_PROCESSING_*.puml` - 6 диаграмм для обработки изображений (1-6)
- `UML_TEXT_ANALYSIS_*.puml` - 6 диаграмм для анализа текста (1-6)

## 📝 Инструкция по использованию

### Draw.io
1. Откройте Draw.io (https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `.drawio`
4. Редактируйте при необходимости
5. File → Export as → PNG
6. Сохраните в `src/img/diagrams/` с указанным именем

### PlantUML
1. Установите PlantUML или используйте онлайн: http://www.plantuml.com/plantuml/uml/
2. Скопируйте код из файла `.puml`
3. Вставьте в редактор PlantUML
4. Экспортируйте как PNG
5. Сохраните в `src/img/diagrams/` с указанным именем

