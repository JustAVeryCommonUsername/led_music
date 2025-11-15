let currentColor = '#ff0000';
let pickr;
let ws;
let musicEnabled = true; // music mode state

function sendWS(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(data);
    }
}

function updateMusicToggleButton() {
    const toggleBtn = document.getElementById('musicToggle');
    toggleBtn.textContent = 'Music syncing: ' + (musicEnabled ? 'ON' : 'OFF');
    toggleBtn.classList.toggle('off', !musicEnabled);
}

document.addEventListener('DOMContentLoaded', () => {
    ws = new WebSocket('ws://' + window.location.host + '/ws');

    ws.onopen = () => {
        console.log('Connected to Python LED server');
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        console.log('WebSocket closed');
    };

    pickr = Pickr.create({
        el: '#colorPickr',
        theme: 'nano',
        default: currentColor,
        inline: true,
        showAlways: true,
        components: {
            preview: false,
            opacity: false,
            hue: true,
            interaction: {}
        }
    });

    pickr.on('change', (color) => {
        currentColor = color.toHEXA().toString();
        const rgb = color.toRGBA();
        sendWS(new Uint8Array([0x01, rgb[0], rgb[1], rgb[2]]));
        if (musicEnabled) {
            musicEnabled = false;
            updateMusicToggleButton();
            sendWS(new Uint8Array([0x02, 0]));
        }
    });

    const toggleBtn = document.getElementById('musicToggle');
    toggleBtn.addEventListener('click', () => {
        musicEnabled = !musicEnabled;
        updateMusicToggleButton();
        sendWS(new Uint8Array([0x02, musicEnabled ? 1 : 0]));
    });
});
