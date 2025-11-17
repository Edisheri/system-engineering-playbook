// Mermaid initialization script for mdBook
// This script loads Mermaid from CDN and renders all mermaid code blocks

(function() {
    // Load Mermaid library from CDN
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    
    script.onload = function() {
        // Initialize Mermaid
        mermaid.initialize({
            startOnLoad: false, // We'll render manually
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
        
        // Function to convert code blocks to mermaid divs
        function convertMermaidBlocks() {
            // Find all code blocks that contain mermaid diagrams
            const codeBlocks = document.querySelectorAll('pre code');
            
            codeBlocks.forEach(function(block) {
                const text = block.textContent.trim();
                
                // Check if this is a mermaid diagram
                if (text.startsWith('flowchart') || 
                    text.startsWith('graph') || 
                    text.startsWith('sequenceDiagram') || 
                    text.startsWith('classDiagram') ||
                    text.startsWith('stateDiagram') ||
                    text.startsWith('erDiagram')) {
                    
                    // Create mermaid div
                    const mermaidDiv = document.createElement('div');
                    mermaidDiv.className = 'mermaid';
                    mermaidDiv.textContent = text;
                    
                    // Replace the pre code block with mermaid div
                    const pre = block.parentElement;
                    pre.parentElement.replaceChild(mermaidDiv, pre);
                }
            });
            
            // Render all mermaid diagrams
            mermaid.run();
        }
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', convertMermaidBlocks);
        } else {
            convertMermaidBlocks();
        }
    };
    
    script.onerror = function() {
        console.error('Failed to load Mermaid library');
    };
    
    // Add script to head
    if (document.head) {
        document.head.appendChild(script);
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            document.head.appendChild(script);
        });
    }
})();
