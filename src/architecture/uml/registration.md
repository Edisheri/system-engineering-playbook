# UML Диаграммы: Система медицинской диагностики с ИИ

## Полный набор UML диаграмм для AI Medical Diagnosis System

Система использует машинное обучение (ResNet-50 и BERT) для анализа медицинских изображений и текстовых симптомов, предоставляя врачам автоматическую диагностику с объяснениями (Grad-CAM, SHAP).

---

>  1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-medical-usecase.html"></iframe>

**Актёры:**
- **Пациент** - загружает медицинские данные, просматривает результаты
- **Врач** - просматривает диагнозы, подтверждает/редактирует заключения (наследует от Пациента)
- **Администратор** - управляет пользователями, настройками, метриками (наследует от Врача)
- **ML Engineer** - обновляет ML модели, проводит A/B тестирование
---

>  2. Activity Diagram (Диаграмма активностей)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-medical-activity.html"></iframe>

**Процесс медицинской диагностики:**

---

>  3. Sequence Diagram (Диаграмма последовательности)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-medical-sequence.html"></iframe>
**Основные потоки:**

**1. Авторизация:**
**2. Загрузка данных:**
**3. Препроцессинг (параллельно):**
**4. ML Inference:**
**5. Формирование отчёта:**
**6. Просмотр:**

---

>  4. Class Diagram (Диаграмма классов)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-medical-class.html"></iframe>

**Основные классы:**
---

>  5. State Diagram (Диаграмма состояний)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-medical-state.html"></iframe>

**Состояния обработки медицинского файла:**
---
