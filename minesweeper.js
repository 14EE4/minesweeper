// 간단한 브라우저용 Minesweeper (DOM 기반)
(function(){
  const gameDiv = document.getElementById('game');
  const startBtn = document.getElementById('startBtn');
  const resetBtn = document.getElementById('resetBtn');
  const flagsLeftSpan = document.getElementById('flagsLeft');
  const statusEl = document.getElementById('status');

  let rows=10, cols=10, mines=12;
  let board = [];
  let started=false, gameOver=false, flagsLeft=0;

  function Cell(){
    this.mine=false; this.revealed=false; this.flagged=false; this.adj=0;
  }

  function randInt(n){ return Math.floor(Math.random()*n); }

  function init(r,c,m){
    rows=r; cols=c; mines=m;
    board = Array.from({length:rows}, ()=> Array.from({length:cols}, ()=> new Cell()));
    started=false; gameOver=false; flagsLeft=mines; flagsLeftSpan.textContent = flagsLeft;
    statusEl.textContent='준비';
    renderGrid();
  }

  function placeMines(firstR, firstC){
    let placed=0;
    while(placed<mines){
      const rr = randInt(rows), cc = randInt(cols);
      if(board[rr][cc].mine) continue;
      // avoid first click cell
      if(Math.abs(rr-firstR)<=1 && Math.abs(cc-firstC)<=1) continue;
      board[rr][cc].mine=true; placed++;
    }
    // compute adjacent counts
    for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
      if(board[r][c].mine) continue;
      let cnt=0;
      for(let dr=-1;dr<=1;dr++) for(let dc=-1;dc<=1;dc++){
        const nr=r+dr, nc=c+dc;
        if(nr<0||nc<0||nr>=rows||nc>=cols) continue;
        if(board[nr][nc].mine) cnt++;
      }
      board[r][c].adj = cnt;
    }
  }

  function renderGrid(){
    gameDiv.innerHTML='';
    gameDiv.style.display='grid';
    gameDiv.style.gridTemplateColumns = `repeat(${cols}, 30px)`;
    gameDiv.style.gap='2px';
    gameDiv.style.maxWidth = `${cols*32}px`;
    for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
      const cell = board[r][c];
      const el = document.createElement('button');
      el.className = 'ms-cell';
      el.style.width='30px'; el.style.height='30px'; el.style.padding='0';
      el.style.fontSize='14px'; el.style.lineHeight='1'; el.style.textAlign='center';
      el.dataset.r=r; el.dataset.c=c;
      if(cell.revealed){
        el.disabled=true; el.style.background='#ddd';
        if(cell.mine) el.textContent='💣';
        else if(cell.adj>0) el.textContent=cell.adj;
      } else {
        el.textContent = cell.flagged ? '🚩' : '';
      }
      el.addEventListener('click', onLeftClick);
      el.addEventListener('contextmenu', onRightClick);
      gameDiv.appendChild(el);
    }
  }

  function reveal(r,c){
    if(r<0||c<0||r>=rows||c>=cols) return;
    const cell = board[r][c];
    if(cell.revealed || cell.flagged) return;
    cell.revealed = true;
    if(cell.mine){ gameLost(); return; }
    if(cell.adj===0){
      for(let dr=-1;dr<=1;dr++) for(let dc=-1;dc<=1;dc++) reveal(r+dr,c+dc);
    }
  }

  function onLeftClick(e){
    if(gameOver) return;
    const r = +this.dataset.r, c = +this.dataset.c;
    if(!started){ placeMines(r,c); started=true; statusEl.textContent='진행중'; }
    reveal(r,c);
    checkWin(); renderGrid();
  }

  function onRightClick(e){
    e.preventDefault(); if(gameOver) return;
    const r = +this.dataset.r, c = +this.dataset.c;
    const cell = board[r][c];
    if(cell.revealed) return;
    cell.flagged = !cell.flagged;
    flagsLeft += cell.flagged ? -1 : 1;
    flagsLeftSpan.textContent = flagsLeft;
    renderGrid();
  }

  function gameLost(){
    gameOver=true; statusEl.textContent='패배';
    // reveal all mines
    for(let r=0;r<rows;r++) for(let c=0;c<cols;c++) if(board[r][c].mine) board[r][c].revealed=true;
    renderGrid();
  }

  function checkWin(){
    let ok=true;
    for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
      const cell = board[r][c];
      if(!cell.mine && !cell.revealed) ok=false;
    }
    if(ok){ gameOver=true; statusEl.textContent='승리'; }
  }

  startBtn.addEventListener('click', ()=>{
    const r = Math.max(5, Math.min(30, parseInt(document.getElementById('rows').value)||10));
    const c = Math.max(5, Math.min(30, parseInt(document.getElementById('cols').value)||10));
    let m = parseInt(document.getElementById('mines').value)||12;
    m = Math.max(1, Math.min(r*c-1, m));
    init(r,c,m);
  });

  resetBtn.addEventListener('click', ()=>{
    init(rows,cols,mines);
  });

  // init default
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', ()=>init(10,10,12)); else init(10,10,12);

})();
