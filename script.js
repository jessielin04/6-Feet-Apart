//REFERENCES UNDER REFERENCES.TXT 
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
    //if-condition: start bg music on first user interaction IF music toggle is still yar
    if (!musicStarted && musicEnabled()) {
        bgMusic.play();
        musicStarted = true;
    }
    //if-condition: button sound effect 
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
//music toggle button callers: stop/play music 
function handleMusicToggle(btn) {
    if (btn.textContent.trim() === 'yes') {
        musicStarted = true;
        bgMusic.play();
    } 
    else {
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

//TO DO: error page "Oh no!" if time permits 
//SEARCH PAGE RAAAAAAA
async function handleSearch() {
    const a = document.getElementById('input-user-a').value.trim();
    const b = document.getElementById('input-user-b').value.trim();
    //if-condition: is input empty? no whitespace!!!
    if (!a || !b) return;
    //if-condition: nonnumeric values = error 
    if (isNaN(a) || isNaN(b)) {
        showError('nonnumeric');
        return;
    }
    showScreen('screen-searching'); //mermaid loop 
    //connects to backend via flask to get results 
    try {
        const res = await fetch(`http://localhost:5000/search?a=${a}&b=${b}`);
        const data = await res.json();
        //TO DO: add error check here 
        window.lastResult = data; // save for "who did it better?" screen later
        showResults(data.degrees, data.path);
    } 
    //TO DO: error cases 
    catch (err) {
    }
}
//RESULTS
//no longer needed bfsResult bcs window.lastResult is used

const searchCompleteSfx = new Audio('assets/audio/search-complete-sound-effect.mp3');
searchCompleteSfx.volume = 0.75;
function showResults(degrees, path) {
    const sub = document.getElementById('results-subtitle');
    sub.style.opacity = '1';
    sub.textContent = "It's a small Twitch after all!";

    //initial blurb under title 
    showScreen('screen-results');
    searchCompleteSfx.currentTime = 0;
    searchCompleteSfx.play();
    //draw vis.js graph
    drawGraph(path);
    //secondary blurb, changes from initial blurb after delay w a fade out
    setTimeout(() => {
        sub.style.opacity = '0';
        setTimeout(() => {
            //changes bcs bfsResults removed 
            sub.textContent = `Only ${degrees} degree${degrees === 1 ? '' : 's'} apart!`;
            sub.style.opacity = '1';
        }, 500);
    }, 10000);
}

function drawGraph(path) {
    const container = document.getElementById('results-graph');
    // build nodes array from path by mapping userID to vis.js node object 
    const nodes = path.map((uid, i) => {
        let color = '#C8A9F5'; 
        if (i === 0)              color = '#F7B3D6'; //userA
        if (i === path.length -1) color = '#A8D8F0'; //userB
        return {
            id: uid,
            label: `User\n${uid}`,
            color: {
                background: color,
                border: '#ffffff',
                highlight: { background: color, border: '#2E2052' }
            },
            font: {
                color: '#2E2052',
                face: 'DMMono',
                size: 13,
            },
            shape: 'circle',
            size: 30,
            borderWidth: 2,
        };
    });

    //vis.js render 
    const edges = [];
    //for-loop: builds edges by pairing each node 
    for (let i = 0; i < path.length - 1; i++) {
        edges.push({
            from: path[i],
            to: path[i + 1],
            color: { color: '#C8A9F5', highlight: '#9b7fe8' },
            width: 2,
            smooth: { type: 'curvedCW', roundness: 0.2 },
        });
    }

    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
    const options = {
        layout: {
            hierarchical: {
                direction: 'LR',
                sortMethod: 'directed',
                nodeSpacing: 120,
                levelSeparation: 160,
            }
        },
        //moving around = NO
        physics: { enabled: false },
        interaction: { zoomView: false, dragView: false },
    };
    new vis.Network(container, data, options);
}

//who did it better comparison screen setup 
function showComparison() {
    const data = window.lastResult;
    //stats for Hash Map + Red-Black Tree
    document.getElementById('hash-time').textContent  = `${data.hash.elapsed_ms} ms`;
    document.getElementById('hash-nodes').textContent = data.hash.nodes_visited.toLocaleString();
    document.getElementById('rbt-time').textContent   = `${data.rbtree.elapsed_ms} ms`;
    document.getElementById('rbt-nodes').textContent  = data.rbtree.nodes_visited.toLocaleString();

    const crown = document.getElementById('crown-img');
    crown.classList.remove('visible');
    //picks faster algorithn + places it above corresponding box 
    const winnerCard = data.hash.elapsed_ms <= data.rbtree.elapsed_ms
        ? document.getElementById('card-hash')
        : document.getElementById('card-rbtree');
    winnerCard.insertBefore(crown, winnerCard.firstChild);
    setTimeout(() => crown.classList.add('visible'), 100);
    showScreen('screen-comparison'); //comparison screen active B)
}