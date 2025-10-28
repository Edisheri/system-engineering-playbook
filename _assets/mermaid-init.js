// Mermaid initialization script
(function() {
    'use strict';
    
    function initMermaid() {
        if (typeof mermaid === 'undefined') {
            console.warn('Mermaid library not loaded, retrying in 1 second...');
            setTimeout(initMermaid, 1000);
            return;
        }
        
        try {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'default',
                securityLevel: 'loose',
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: 'basis'
                },
                sequence: {
                    diagramMarginX: 50,
                    diagramMarginY: 10,
                    actorMargin: 50,
                    width: 150,
                    height: 65,
                    boxMargin: 10,
                    boxTextMargin: 5,
                    noteMargin: 10,
                    messageMargin: 35,
                    messageAlign: 'center',
                    mirrorActors: true,
                    bottomMarginAdj: 1,
                    useMaxWidth: true,
                    rightAngles: false,
                    showSequenceNumbers: false
                },
                gantt: {
                    titleTopMargin: 25,
                    barHeight: 20,
                    barGap: 4,
                    topPadding: 50,
                    leftPadding: 75,
                    gridLineStartPadding: 35,
                    fontSize: 11,
                    fontFamily: '"Open-Sans", "sans-serif"',
                    sectionFontSize: 24,
                    numberSectionStyles: 4
                }
            });
            
            // Find and render all mermaid diagrams
            const mermaidElements = document.querySelectorAll('.mermaid, pre.language-mermaid, pre code.language-mermaid');
            mermaidElements.forEach((element, index) => {
                try {
                    const content = element.textContent || element.innerText;
                    if (content.trim()) {
                        const id = 'mermaid-' + index + '-' + Date.now();
                        element.id = id;
                        element.innerHTML = content;
                        mermaid.init(undefined, element);
                    }
                } catch (error) {
                    console.error('Error rendering mermaid diagram:', error);
                    element.innerHTML = '<div style="color: red; padding: 10px; border: 1px solid red; border-radius: 4px;">Ошибка отображения диаграммы: ' + error.message + '</div>';
                }
            });
            
            console.log('Mermaid initialized successfully, rendered', mermaidElements.length, 'diagrams');
        } catch (error) {
            console.error('Error initializing Mermaid:', error);
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMermaid);
    } else {
        initMermaid();
    }
})();
