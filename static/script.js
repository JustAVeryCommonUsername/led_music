let currentColor = '#ff0000';
let pickr;
let ws;

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
        if (ws && ws.readyState === WebSocket.OPEN) {
            const rgb = color.toRGBA();
            const buf = new Uint8Array([rgb[0], rgb[1], rgb[2]]);
            ws.send(buf);
        }
    });
});
