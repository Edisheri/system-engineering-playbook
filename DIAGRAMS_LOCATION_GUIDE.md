# 📍 Справочник по расположению диаграмм

Этот документ поможет вам найти и отредактировать все диаграммы в проекте.

---

## 📁 Структура папок

```
system-engineering-playbook/
├── diagrams-codes/          ← ИСХОДНИКИ диаграмм (редактируйте здесь!)
│   ├── *.drawio            ← Draw.io файлы (XML формат)
│   └── *.puml              ← PlantUML файлы (текстовый формат)
│
├── img/diagrams/           ← PNG изображения (экспортированные)
│   └── *.png               ← Статические изображения
│
└── src/architecture/       ← Markdown файлы (где диаграммы отображаются)
    ├── c4-diagrams.md
    ├── idef0.md
    ├── idef3.md
    ├── dfd.md
    ├── bpmn.md
    └── component-schema.md
```

---

## 🎨 1. C4 Модель (Context, Container, Component)

### ❌ Исходников НЕТ (только PNG)

**PNG изображения:**
- `img/diagrams/c4-context.png` - Контекстная диаграмма
- `img/diagrams/c4-container.png` - Диаграмма контейнеров
- `img/diagrams/c4-component.png` - Диаграмма компонентов

**Где отображается:**
- `src/architecture/c4-diagrams.md`

**Как редактировать:**
1. Откройте PNG в любом графическом редакторе (Photoshop, GIMP, Figma)
2. Или создайте новые C4 диаграммы на [Structurizr](https://structurizr.com/) или [draw.io](https://app.diagrams.net/)
3. Экспортируйте как PNG
4. Сохраните в `img/diagrams/`

---

## 📊 2. IDEF0 Диаграммы

### ✅ Исходники: `.drawio` файлы

**Расположение:** `diagrams-codes/`

| Файл | Описание |
|------|----------|
| `IDEF0_A0.drawio` | Контекстная диаграмма A0 |
| `IDEF0_DECOMPOSITION.drawio` | Декомпозиция A0 → A1, A2, A3, A4 |
| `IDEF0_A1.drawio` | Функция A1: Приём данных |
| `IDEF0_A1_DECOMPOSITION.drawio` | Декомпозиция A1 |
| `IDEF0_A2.drawio` | Функция A2: Препроцессинг |
| `IDEF0_A2_DECOMPOSITION.drawio` | Декомпозиция A2 |
| `IDEF0_A3.drawio` | Функция A3: ИИ-анализ |
| `IDEF0_A3_DECOMPOSITION.drawio` | Декомпозиция A3 |
| `IDEF0_A4.drawio` | Функция A4: Формирование отчёта |
| `IDEF0_A4_DECOMPOSITION.drawio` | Декомпозиция A4 |

**Где отображается:**
- `src/architecture/idef0.md` - Обзор
- `src/architecture/idef0-function1.md` - A1
- `src/architecture/idef0-function2.md` - A2
- `src/architecture/idef0-function3.md` - A3
- `src/architecture/idef0-function4.md` - A4

**Как редактировать:**
1. Откройте [app.diagrams.net](https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `IDEF0_*.drawio` из `diagrams-codes/`
4. Редактируйте
5. File → Save (сохраняется в XML формате)

---

## 🔄 3. IDEF3 Диаграммы (Процессы)

### ✅ Исходники: `.drawio` файлы

**Расположение:** `diagrams-codes/`

| Файл | Описание |
|------|----------|
| `IDEF3_OVERVIEW.drawio` | Обзор всех процессов |
| `IDEF3_P1.drawio` | Процесс P1: Регистрация |
| `IDEF3_P2.drawio` | Процесс P2: Загрузка данных |
| `IDEF3_P3.drawio` | Процесс P3: GPU-обработка |
| `IDEF3_P4.drawio` | Процесс P4: Логирование |

**Где отображается:**
- `src/architecture/idef3.md` - Обзор
- `src/architecture/idef3-process1.md` - P1
- `src/architecture/idef3-process2.md` - P2
- `src/architecture/idef3-process3.md` - P3
- `src/architecture/idef3-process4.md` - P4

**Как редактировать:**
1. Откройте [app.diagrams.net](https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `IDEF3_*.drawio` из `diagrams-codes/`
4. Редактируйте
5. File → Save

---

## 📈 4. DFD Диаграммы (Потоки данных)

### ✅ Исходники: `.drawio` файлы

**Расположение:** `diagrams-codes/`

| Файл | Описание |
|------|----------|
| `DFD_OVERVIEW.drawio` | Обзор потоков данных |
| `DFD_P1.drawio` | Процесс P1: Приём данных |
| `DFD_P1_DECOMPOSITION.drawio` | Декомпозиция P1 |
| `DFD_P2.drawio` | Процесс P2: Валидация |
| `DFD_P2_DECOMPOSITION.drawio` | Декомпозиция P2 |
| `DFD_P3.drawio` | Процесс P3: ИИ-анализ |
| `DFD_P3_DECOMPOSITION.drawio` | Декомпозиция P3 |
| `DFD_P4.drawio` | Процесс P4: Логирование |
| `DFD_P4_DECOMPOSITION.drawio` | Декомпозиция P4 |

**Где отображается:**
- `src/architecture/dfd.md` - Обзор
- `src/architecture/dfd-process1.md` - P1
- `src/architecture/dfd-process2.md` - P2
- `src/architecture/dfd-process3.md` - P3
- `src/architecture/dfd-process4.md` - P4

**Как редактировать:**
1. Откройте [app.diagrams.net](https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `DFD_*.drawio` из `diagrams-codes/`
4. Редактируйте
5. File → Save

---

## 🔀 5. BPMN Диаграммы (Бизнес-процессы)

### ✅ Исходники: `.drawio` файлы

**Расположение:** `diagrams-codes/`

| Файл | Описание |
|------|----------|
| `BPMN_SCENARIO1.drawio` | Сценарий 1: Загрузка и обработка |
| `BPMN_SCENARIO2.drawio` | Сценарий 2: Регистрация пользователя |
| `BPMN_SCENARIO3.drawio` | Сценарий 3: Генерация отчёта |
| `BPMN_SCENARIO4.drawio` | Сценарий 4: Обработка ошибок |

**Где отображается:**
- `src/architecture/bpmn.md`

**Как редактировать:**
1. Откройте [app.diagrams.net](https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `BPMN_*.drawio` из `diagrams-codes/`
4. Редактируйте
5. File → Save

---

## 🧩 6. Компонентная схема

### ✅ Исходник: `.drawio` файл

**Расположение:** `diagrams-codes/`

| Файл | Описание |
|------|----------|
| `COMPONENT_SCHEMA.drawio` | Полная компонентная схема (40+ компонентов, 8 слоёв) |

**Где отображается:**
- `src/architecture/component-schema.md`

**Как редактировать:**
1. Откройте [app.diagrams.net](https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `COMPONENT_SCHEMA.drawio` из `diagrams-codes/`
4. Редактируйте
5. File → Save

**⚠️ ВАЖНО:** После сохранения файл автоматически отобразится на GitHub Pages через iframe!

---

## 📐 7. UML Диаграммы

### ✅ Исходники: `.drawio` и `.puml` файлы

**Расположение:** `diagrams-codes/`

### 7.1. Регистрация (Registration)

| Файл | Тип | Описание |
|------|-----|----------|
| `UML_REGISTRATION_1_UseCase.drawio` | Draw.io | Use Case |
| `UML_REGISTRATION_2_Activity.drawio` | Draw.io | Activity |
| `UML_REGISTRATION_3_Sequence.drawio` | Draw.io | Sequence |
| `UML_REGISTRATION_4_Class.drawio` | Draw.io | Class |
| `UML_REGISTRATION_5_State.drawio` | Draw.io | State |
| `UML_REGISTRATION_6_Component.drawio` | Draw.io | Component |
| `Registration_*.puml` | PlantUML | Альтернативные версии |

### 7.2. Загрузка данных (Data Upload)

| Файл | Тип | Описание |
|------|-----|----------|
| `UML_DATA_UPLOAD_1_UseCase.drawio` | Draw.io | Use Case |
| `UML_DATA_UPLOAD_2_Activity.drawio` | Draw.io | Activity |
| `UML_DATA_UPLOAD_3_Sequence.drawio` | Draw.io | Sequence |
| `UML_DATA_UPLOAD_4_Class.drawio` | Draw.io | Class |
| `UML_DATA_UPLOAD_5_State.drawio` | Draw.io | State |
| `UML_DATA_UPLOAD_6_Component.drawio` | Draw.io | Component |
| `DataUpload_*.puml` | PlantUML | Альтернативные версии |

### 7.3. Обработка изображений (Image Processing)

| Файл | Тип | Описание |
|------|-----|----------|
| `UML_IMAGE_PROCESSING_1_UseCase.drawio` | Draw.io | Use Case |
| `UML_IMAGE_PROCESSING_2_Activity.drawio` | Draw.io | Activity |
| `UML_IMAGE_PROCESSING_3_Sequence.drawio` | Draw.io | Sequence |
| `UML_IMAGE_PROCESSING_4_Class.drawio` | Draw.io | Class |
| `UML_IMAGE_PROCESSING_5_State.drawio` | Draw.io | State |
| `UML_IMAGE_PROCESSING_6_Component.drawio` | Draw.io | Component |
| `ImageProcessing_*.puml` | PlantUML | Альтернативные версии |

### 7.4. Анализ текста (Text Analysis)

| Файл | Тип | Описание |
|------|-----|----------|
| `UML_TEXT_ANALYSIS_1_UseCase.drawio` | Draw.io | Use Case |
| `UML_TEXT_ANALYSIS_2_Activity.drawio` | Draw.io | Activity |
| `UML_TEXT_ANALYSIS_3_Sequence.drawio` | Draw.io | Sequence |
| `UML_TEXT_ANALYSIS_4_Class.drawio` | Draw.io | Class |
| `UML_TEXT_ANALYSIS_5_State.drawio` | Draw.io | State |
| `UML_TEXT_ANALYSIS_6_Component.drawio` | Draw.io | Component |
| `TextAnalysis_*.puml` | PlantUML | Альтернативные версии |

**Где отображается:**
- `src/architecture/uml/registration.md`
- `src/architecture/uml/data-upload.md`
- `src/architecture/uml/image-processing.md`
- `src/architecture/uml/text-analysis.md`

**Как редактировать:**

#### Draw.io файлы:
1. Откройте [app.diagrams.net](https://app.diagrams.net/)
2. File → Open from → Device
3. Выберите файл `UML_*.drawio` из `diagrams-codes/`
4. Редактируйте
5. File → Save

#### PlantUML файлы:
1. Откройте [plantuml.com/plantuml/uml/](http://www.plantuml.com/plantuml/uml/)
2. Скопируйте код из файла `*.puml`
3. Вставьте в редактор
4. Редактируйте
5. Сохраните обратно в файл `.puml`

---

## 🛠️ Инструменты для редактирования

### Draw.io (рекомендуется для .drawio файлов)
- **Онлайн:** [app.diagrams.net](https://app.diagrams.net/)
- **Desktop:** [github.com/jgraph/drawio-desktop/releases](https://github.com/jgraph/drawio-desktop/releases)
- **VS Code Extension:** "Draw.io Integration"

### PlantUML (для .puml файлов)
- **Онлайн:** [plantuml.com/plantuml/uml/](http://www.plantuml.com/plantuml/uml/)
- **VS Code Extension:** "PlantUML"
- **IntelliJ Plugin:** "PlantUML integration"

---

## 📝 Как обновить диаграмму на сайте

### Шаг 1: Отредактируйте исходник
1. Откройте файл `.drawio` или `.puml` в соответствующем редакторе
2. Внесите изменения
3. Сохраните файл

### Шаг 2: Закоммитьте изменения
```bash
git add diagrams-codes/ВАШ_ФАЙЛ.drawio
git commit -m "Update diagram: описание изменений"
git push origin main
```

### Шаг 3: Дождитесь деплоя
- GitHub Actions автоматически соберёт книгу
- Через 2-3 минуты изменения появятся на GitHub Pages
- Обновите страницу (Ctrl+F5) для очистки кэша

---

## 🔍 Быстрый поиск диаграмм

### По типу:
- **IDEF0:** `diagrams-codes/IDEF0_*.drawio`
- **IDEF3:** `diagrams-codes/IDEF3_*.drawio`
- **DFD:** `diagrams-codes/DFD_*.drawio`
- **BPMN:** `diagrams-codes/BPMN_*.drawio`
- **UML:** `diagrams-codes/UML_*.drawio` или `*.puml`
- **Component:** `diagrams-codes/COMPONENT_SCHEMA.drawio`

### По функции:
- **Регистрация:** `*REGISTRATION*` или `*Registration*`
- **Загрузка данных:** `*DATA_UPLOAD*` или `*DataUpload*`
- **Обработка изображений:** `*IMAGE_PROCESSING*` или `*ImageProcessing*`
- **Анализ текста:** `*TEXT_ANALYSIS*` или `*TextAnalysis*`

---

## ⚠️ Важные замечания

1. **Не редактируйте PNG напрямую** - они генерируются из исходников
2. **Всегда редактируйте `.drawio` или `.puml` файлы** в `diagrams-codes/`
3. **После изменений делайте commit и push** - иначе изменения не появятся на сайте
4. **C4 диаграммы** - только PNG, исходников нет (можно создать новые в draw.io)

---

## 📞 Нужна помощь?

Если не можете найти нужную диаграмму:
1. Проверьте этот файл (`DIAGRAMS_LOCATION_GUIDE.md`)
2. Посмотрите в `diagrams-codes/README.md`
3. Проверьте структуру в `src/architecture/*.md` файлах

---

**Последнее обновление:** 2025-01-25

