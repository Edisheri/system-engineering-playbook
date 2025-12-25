# UML Диаграммы: Анализ текста

## Функция 4: Анализ текстовых симптомов (BERT)

Эта функция отвечает за обработку и анализ текстовых симптомов пациентов с использованием BERT (Bidirectional Encoder Representations from Transformers) для классификации заболеваний.

---

>  1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-text-analysis-usecase.html"></iframe>

**Актёры:**
- **ML Service** (система) - автоматическая обработка текстов
- **Врач** (Doctor) - валидация медицинской терминологии
- **ML Engineer** (инженер машинного обучения) - fine-tuning модели

**Связи:**
- `<<include>>`: Обязательные зависимости между use cases
- `<<extend>>`: Опциональные расширения функциональности

---

>  2. Activity Diagram (Диаграмма активностей)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-text-analysis-activity.html"></iframe>

**Процесс анализа текста:**
---

>  3. Sequence Diagram (Диаграмма последовательности)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-text-analysis-sequence.html"></iframe>

---

>  4. Class Diagram (Диаграмма классов)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-text-analysis-class.html"></iframe>

---

>  5. State Diagram (Диаграмма состояний)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-text-analysis-state.html"></iframe>

**Состояния обработки текстовых симптомов:**

---

>  6. Component Diagram (Диаграмма компонентов)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-text-analysis-component.html"></iframe>

---
