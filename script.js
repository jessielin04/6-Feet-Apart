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
    //quick change: when users click "search again" on resulst page, values are cleared from search input page blep :P
    if (id === 'screen-search') {
        document.getElementById('input-user-a').value = '';
        document.getElementById('input-user-b').value = '';
    }
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
    setTimeout(() => showResults(3, []), 6000);
}

//RESULTS
//need to link to backend to work grrrr
let bfsResult = {
    degrees: null,
    path: [],
};

const searchCompleteSfx = new Audio('assets/audio/search-complete-sound-effect.mp3');
searchCompleteSfx.volume = 0.75;

function showResults(degrees, path) {
    bfsResult.degrees = degrees;
    bfsResult.path    = path;

    //blurb under title swap to amt of deg/nodes apart
    const sub = document.getElementById('results-subtitle');
    sub.style.opacity = '1';
    sub.textContent = "It's a small Twitch after all!";
    showScreen('screen-results');
    searchCompleteSfx.currentTime = 0;
    searchCompleteSfx.play();

    // swap subtitle after 10s
    setTimeout(() => {
        sub.style.opacity = '0';
        setTimeout(() => {
            sub.textContent = `Only ${bfsResult.degrees} degree${bfsResult.degrees === 1 ? '' : 's'} apart!`;
            sub.style.opacity = '1';
        }, 500); 
    }, 10000);
}