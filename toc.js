// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><a href="introduction.html"><strong aria-hidden="true">1.</strong> 1. Введение</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">2. Требования (Requirements)</li><li class="chapter-item expanded "><a href="requirements/functional.html"><strong aria-hidden="true">2.</strong> 2.1. Функциональные требования</a></li><li class="chapter-item expanded "><a href="requirements/non-functional.html"><strong aria-hidden="true">3.</strong> 2.2. Нефункциональные требования</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">3. Архитектура системы (System Architecture)</li><li class="chapter-item expanded "><a href="architecture/c4-diagrams.html"><strong aria-hidden="true">4.</strong> 3.1.1. C4 Model</a></li><li class="chapter-item expanded "><a href="architecture/idef0.html"><strong aria-hidden="true">5.</strong> 3.1.2.1. IDEF0: Обзор</a></li><li class="chapter-item expanded "><a href="architecture/idef0-function1.html"><strong aria-hidden="true">6.</strong> 3.1.2.2. IDEF0: Функция A1 — Приём данных</a></li><li class="chapter-item expanded "><a href="architecture/idef0-function2.html"><strong aria-hidden="true">7.</strong> 3.1.2.3. IDEF0: Функция A2 — Препроцессинг</a></li><li class="chapter-item expanded "><a href="architecture/idef0-function3.html"><strong aria-hidden="true">8.</strong> 3.1.2.4. IDEF0: Функция A3 — ИИ-анализ</a></li><li class="chapter-item expanded "><a href="architecture/idef0-function4.html"><strong aria-hidden="true">9.</strong> 3.1.2.5. IDEF0: Функция A4 — Формирование отчёта</a></li><li class="chapter-item expanded "><a href="architecture/idef3.html"><strong aria-hidden="true">10.</strong> 3.1.3.1. IDEF3: Обзор</a></li><li class="chapter-item expanded "><a href="architecture/idef3-process1.html"><strong aria-hidden="true">11.</strong> 3.1.3.2. IDEF3: Процесс P1 — Регистрация</a></li><li class="chapter-item expanded "><a href="architecture/idef3-process2.html"><strong aria-hidden="true">12.</strong> 3.1.3.3. IDEF3: Процесс P2 — Загрузка данных</a></li><li class="chapter-item expanded "><a href="architecture/idef3-process3.html"><strong aria-hidden="true">13.</strong> 3.1.3.4. IDEF3: Процесс P3 — GPU-обработка</a></li><li class="chapter-item expanded "><a href="architecture/idef3-process4.html"><strong aria-hidden="true">14.</strong> 3.1.3.5. IDEF3: Процесс P4 — Логирование</a></li><li class="chapter-item expanded "><a href="architecture/dfd.html"><strong aria-hidden="true">15.</strong> 3.1.4.1. DFD: Обзор</a></li><li class="chapter-item expanded "><a href="architecture/dfd-process1.html"><strong aria-hidden="true">16.</strong> 3.1.4.2. DFD: Процесс P1 — Приём данных</a></li><li class="chapter-item expanded "><a href="architecture/dfd-process2.html"><strong aria-hidden="true">17.</strong> 3.1.4.3. DFD: Процесс P2 — Валидация</a></li><li class="chapter-item expanded "><a href="architecture/dfd-process3.html"><strong aria-hidden="true">18.</strong> 3.1.4.4. DFD: Процесс P3 — ИИ-анализ</a></li><li class="chapter-item expanded "><a href="architecture/dfd-process4.html"><strong aria-hidden="true">19.</strong> 3.1.4.5. DFD: Процесс P4 — Логирование</a></li><li class="chapter-item expanded "><a href="architecture/bpmn.html"><strong aria-hidden="true">20.</strong> 3.1.5.1. BPMN: Обзор</a></li><li class="chapter-item expanded "><a href="architecture/bpmn-scenario1.html"><strong aria-hidden="true">21.</strong> 3.1.5.2. BPMN Сценарий 1: Регистрация пациента</a></li><li class="chapter-item expanded "><a href="architecture/bpmn-scenario2.html"><strong aria-hidden="true">22.</strong> 3.1.5.3. BPMN Сценарий 2: Загрузка данных</a></li><li class="chapter-item expanded "><a href="architecture/bpmn-scenario3.html"><strong aria-hidden="true">23.</strong> 3.1.5.4. BPMN Сценарий 3: ИИ-анализ</a></li><li class="chapter-item expanded "><a href="architecture/bpmn-scenario4.html"><strong aria-hidden="true">24.</strong> 3.1.5.5. BPMN Сценарий 4: Интеграция с MIS</a></li><li class="chapter-item expanded "><a href="architecture/uml/registration.html"><strong aria-hidden="true">25.</strong> 3.1.6.1. Функция 1: Регистрация пользователя</a></li><li class="chapter-item expanded "><a href="architecture/uml/data-upload.html"><strong aria-hidden="true">26.</strong> 3.1.6.2. Функция 2: Загрузка данных</a></li><li class="chapter-item expanded "><a href="architecture/uml/image-processing.html"><strong aria-hidden="true">27.</strong> 3.1.6.3. Функция 3: Обработка изображений</a></li><li class="chapter-item expanded "><a href="architecture/uml/text-analysis.html"><strong aria-hidden="true">28.</strong> 3.1.6.4. Функция 4: Анализ текста</a></li><li class="chapter-item expanded "><a href="architecture/component-schema.html"><strong aria-hidden="true">29.</strong> 3.1.7.1. Компонентная схема системы</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">4. Архитектурные решения (Architecture Decision Records)</li><li class="chapter-item expanded "><a href="adr/adr-001-resnet50.html"><strong aria-hidden="true">30.</strong> 4.1. ADR-001: Выбор ResNet-50</a></li><li class="chapter-item expanded "><a href="adr/adr-002-postgresql-redis.html"><strong aria-hidden="true">31.</strong> 4.2. ADR-002: PostgreSQL + Redis</a></li><li class="chapter-item expanded "><a href="adr/adr-003-rabbitmq.html"><strong aria-hidden="true">32.</strong> 4.3. ADR-003: RabbitMQ</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">5. Интерфейсы (Interfaces)</li><li class="chapter-item expanded "><a href="api-documentation.html"><strong aria-hidden="true">33.</strong> 5.1. Публичный API</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">6. Инфраструктура (Infrastructure)</li><li class="chapter-item expanded "><a href="infrastructure.html"><strong aria-hidden="true">34.</strong> 6.1. Инфраструктура и деплой</a></li><li class="chapter-item expanded "><a href="customer-journey.html"><strong aria-hidden="true">35.</strong> 6.2. Customer Journey Map</a></li><li class="chapter-item expanded affix "><li class="spacer"></li><li class="chapter-item expanded affix "><li class="part-title">7. Приложения (Appendices)</li><li class="chapter-item expanded "><a href="drawio.html"><strong aria-hidden="true">36.</strong> 7.1. Примеры: DrawIO</a></li><li class="chapter-item expanded "><a href="md.html"><strong aria-hidden="true">37.</strong> 7.2. Примеры: Markdown</a></li><li class="chapter-item expanded "><a href="swagger.html"><strong aria-hidden="true">38.</strong> 7.3. Swagger Example</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
