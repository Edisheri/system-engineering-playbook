# IDEF0 Диаграммы

## Описание методологии

IDEF0 (Integration Definition for Function Modeling) — методология функционального моделирования, описывающая процессы в виде иерархии функций с входами, выходами, управлением и механизмами.

![IDEF0 Диаграмма](img/img1.png)

### IDEF0 Context Diagram (Интерактивная версия)

```mermaid
graph LR
    subgraph Inputs["ВХОДЫ"]
        I1[Медицинские<br/>изображения<br/>JPEG/PNG]
        I2[Описание<br/>симптомов<br/>JSON/TXT]
    end
    
    subgraph Control["УПРАВЛЕНИЕ"]
        C1[Правила<br/>валидации]
        C2[Модели ИИ<br/>ResNet/BERT]
        C3[Стандарты<br/>медицины]
    end
    
    subgraph Process["A0"]
        A0[Диагностика<br/>заболеваний]
    end
    
    subgraph Mechanisms["МЕХАНИЗМЫ"]
        M1[GPU Кластер<br/>NVIDIA T4]
        M2[PostgreSQL<br/>Redis]
        M3[RabbitMQ]
        M4[TensorFlow<br/>Serving]
    end
    
    subgraph Outputs["ВЫХОДЫ"]
        O1[Диагнозы<br/>с вероятностями]
        O2[PDF/HTML<br/>отчёты]
        O3[Heatmap<br/>визуализация]
    end
    
    I1 --> A0
    I2 --> A0
    
    C1 -.-> A0
    C2 -.-> A0
    C3 -.-> A0
    
    M1 -.support.-> A0
    M2 -.support.-> A0
    M3 -.support.-> A0
    M4 -.support.-> A0
    
    A0 --> O1
    A0 --> O2
    A0 --> O3
    
    style A0 fill:#4a90e2,stroke:#2e5c8a,stroke-width:4px,color:#fff
    style I1 fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style I2 fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style O1 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style O2 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style O3 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
```

## Основная функция

**A0: Диагностика заболеваний**

## Декомпозиция на 4 функции

### A1: Приём данных

**Описание:** Получение медицинских данных от пациента

**Входы:**
- Изображения (JPEG/PNG)
- Текст (JSON)

**Выходы:**
- Сообщения в RabbitMQ

**Управление:**
- Правила валидации
- Ограничения размера файлов (10 МБ)

**Механизмы:**
- AWS S3 (хранилище)
- Nginx (балансировка нагрузки)

---

### A2: Препроцессинг

**Описание:** Подготовка данных для ИИ-анализа

**Входы:**
- Данные из очереди RabbitMQ

**Выходы:**
- Тензоры (224x224x3)
- Токены BERT

**Управление:**
- Параметры нормализации
- Правила токенизации

**Механизмы:**
- OpenCV (обработка изображений)
- HuggingFace Tokenizer (обработка текста)

---

### A3: ИИ-анализ

**Описание:** Классификация заболеваний

**Входы:**
- Тензоры изображений
- Токены текста

**Выходы:**
- JSON-результаты (вероятность заболевания)

**Управление:**
- Пороговые значения вероятности
- Версии моделей

**Механизмы:**
- ResNet-50 (анализ изображений)
- BERT (анализ симптомов)
- GPU кластер

---

### A4: Формирование отчёта

**Описание:** Генерация результатов диагностики

**Входы:**
- JSON-данные с результатами

**Выходы:**
- PDF/HTML-отчёты
- Данные для MIS

**Управление:**
- Шаблоны отчётов
- Требования к формату

**Механизмы:**
- PDFKit (генерация PDF)
- REST API (интеграция с MIS)

---

## Источники

- [IDEF0 для ПО](https://www.idef.com/idef0/)
- «Business Process Modeling» Laguna & Marklund

