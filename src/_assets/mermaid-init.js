// Mermaid initialization script for mdBook
// Load Mermaid from CDN first
(function() {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    script.onload = function() {
        // Initialize Mermaid
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
        
        // Find all mermaid code blocks and render them
        const mermaidBlocks = document.querySelectorAll('pre code.language-mermaid');
        mermaidBlocks.forEach(function(block) {
            const code = block.textContent;
            const parent = block.parentElement;
            const div = document.createElement('div');
            div.className = 'mermaid';
            div.textContent = code;
            parent.parentElement.replaceChild(div, parent);
        });
        
        // Also handle code blocks with mermaid content
        const allCodeBlocks = document.querySelectorAll('pre code');
        allCodeBlocks.forEach(function(block) {
            const text = block.textContent.trim();
            if (text.startsWith('flowchart') || text.startsWith('graph') || 
                text.startsWith('sequenceDiagram') || text.startsWith('classDiagram')) {
                const parent = block.parentElement;
                const div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = text;
                parent.parentElement.replaceChild(div, parent);
            }
        });
        
        // Render all mermaid diagrams
        mermaid.run();
    };
    document.head.appendChild(script);
})();
