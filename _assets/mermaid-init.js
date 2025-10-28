// Mermaid initialization script
(function() {
    'use strict';
    
    function initMermaid() {
        if (typeof mermaid !== 'undefined') {
            console.log('Initializing Mermaid...');
            
            mermaid.initialize({
                startOnLoad: false,
                theme: 'default',
                securityLevel: 'loose',
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true
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
            
            // Render all mermaid diagrams
            const mermaidElements = document.querySelectorAll('pre.language-mermaid, code.language-mermaid');
            console.log('Found ' + mermaidElements.length + ' Mermaid diagrams');
            
            mermaidElements.forEach((element, index) => {
                try {
                    const graphDefinition = element.textContent;
                    const id = 'mermaid-' + index + '-' + Math.random().toString(36).substr(2, 9);
                    
                    // Create a div to hold the diagram
                    const diagramDiv = document.createElement('div');
                    diagramDiv.id = id;
                    diagramDiv.className = 'mermaid';
                    
                    // Replace the code block with the diagram
                    element.parentNode.replaceChild(diagramDiv, element);
                    
                    // Render the diagram
                    mermaid.render(id, graphDefinition).then(({svg}) => {
                        diagramDiv.innerHTML = svg;
                    }).catch((error) => {
                        console.error('Error rendering Mermaid diagram:', error);
                        diagramDiv.innerHTML = '<p style="color: red;">Error rendering diagram: ' + error.message + '</p>';
                    });
                } catch (error) {
                    console.error('Error processing Mermaid element:', error);
                }
            });
        } else {
            console.warn('Mermaid library not loaded, retrying in 100ms...');
            setTimeout(initMermaid, 100);
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMermaid);
    } else {
        initMermaid();
    }
})();
