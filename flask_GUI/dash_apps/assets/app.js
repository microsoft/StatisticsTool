// custom_script.js
function detectTargetDiv() {
    const targetDiv = document.getElementById('report_id');
    if (targetDiv) {
        console.log('Target div found:', targetDiv);
        addMouseDownEventListener(targetDiv);
    } else {
        // Keep checking for the target div until it becomes available
        setTimeout(detectTargetDiv, 100);
    }
}

function addMouseDownEventListener(targetDiv) {
    targetDiv.addEventListener('mousedown', function(event) {
        const message = {
            action: 'viewer-mousedown',
            value: 'viewer-mousedown'
        };
        window.parent.postMessage(message, '*');
    });
}

// Start detecting the target div after the page loads
window.onload = detectTargetDiv;
