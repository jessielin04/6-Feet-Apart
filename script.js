//AUDIO SETUP 
const bgMusic = document.getElementById('bg-music');
const btnSfx  = document.getElementById('sfx-btn');

bgMusic.volume = 0.4;

//NEED TO WORK ON THIS; MUSIC NOT PLAYING IN DEMO
//start music on very first button click
let musicStarted = false;
document.addEventListener('click', e => {
    const btn = e.target.closest('.btn');
    if (!btn) return;
    //start bg music on first user interaction IF music toggle is still yar
    if (!musicStarted && musicEnabled()) {
        bgMusic.play();
        musicStarted = true;
    }
    //button sound effect 
    if (sfxEnabled()) {
        btnSfx.currentTime = 0;
        btnSfx.play();
    }
});

//SETTINGS HELPERS
function musicEnabled() {
    const row = document.querySelectorAll('.settings-row')[0];
    return !row || row.querySelector('.active-toggle')?.textContent.trim() === 'yes';
}
function sfxEnabled() {
    const row = document.querySelectorAll('.settings-row')[1];
    return !row || row.querySelector('.active-toggle')?.textContent.trim() === 'yes';
}

//music toggle button callers
function handleMusicToggle(btn) {
    if (btn.textContent.trim() === 'yes') {
        musicStarted = true;
        bgMusic.play();
    } else {
        bgMusic.pause();
    }
}

//SCREEN SWITCH 
function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

//YES/NO TOGGLE FOR SETTINGS
function toggle(btn) {
    const group = btn.closest('.settings-btns').querySelectorAll('.settings-toggle');
    group.forEach(b => {
        b.classList.remove('btn-sky', 'active-toggle');
        b.classList.add('btn-sky-dim');
    });
    btn.classList.remove('btn-sky-dim');
    btn.classList.add('btn-sky', 'active-toggle');
}

function handleSearch() {
    const a = document.getElementById('input-user-a').value.trim();
    const b = document.getElementById('input-user-b').value.trim();
    //NOTE!!!!
    //need to link to oreoluwa's backend; dont forget, need to finish after UI is done!!!!!!!
    if (!a || !b) return;
    showScreen('screen-searching');
    setTimeout(() => showScreen('screen-results'), 8000);
}