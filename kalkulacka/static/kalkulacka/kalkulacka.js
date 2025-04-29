const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.classList.add(savedTheme);
    if (savedTheme === 'dark-mode') {
        themeSwitch.checked = true;
    }
}

themeSwitch.addEventListener('change', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark-mode');
    } else {
        localStorage.setItem('theme', '');
    }
});

// Zvuk při kliknutí na tlačítko
const button = document.querySelector('button');
const synth = new Tone.Synth().toDestination();

button.addEventListener('click', () => {
    synth.triggerAttackRelease("C4", "8n");
});