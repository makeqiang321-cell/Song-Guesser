// Song Guesser — shared game logic (songspot-style: search guess + difficulty rail + timeline).
// Pure Web Audio playback: fetch → decodeAudioData → createBufferSource + GainNode. No <audio>.
(function(){
  var $ = function(s){ return document.querySelector(s); };
  var $$ = function(s){ return Array.prototype.slice.call(document.querySelectorAll(s)); };

  var GENRE_ID = null;
  var ARTIST = null;
  var DECADE = null;
  var DIFF = 'easy';
  var REVEALS = [
    {sec:0.1, label:'0.1s'},
    {sec:0.5, label:'0.5s'},
    {sec:2,   label:'2s'},
    {sec:8,   label:'8s'},
    {sec:15,  label:'15s'}
  ];
  var POSITION = [0, 3, 13, 53, 98]; // --timeline-position per stage (%)
  var POOL_LIMIT = {easy:12, medium:25, hard:50, expert:50, impossible:50};
  var GENRE_NAMES = {21:'Rock',14:'Pop',18:'Hip-Hop',51:'K-Pop',15:'R&B',7:'Electronic',6:'Country',1153:'Metal'};
  var DIFF_COLORS = {
    easy:       {accent:'#19df70', text:'#39e887', on:'#04160b', rgb:'25,223,112'},
    medium:     {accent:'#ffca12', text:'#ffd234', on:'#171200', rgb:'255,202,18'},
    hard:       {accent:'#ff7517', text:'#ff8631', on:'#190900', rgb:'255,117,23'},
    expert:     {accent:'#f04444', text:'#f66464', on:'#1b0505', rgb:'240,68,68'},
    impossible: {accent:'#9748dd', text:'#ae67ed', on:'#14061e', rgb:'151,72,221'}
  };
  function applyDiffColor(d){
    var c = DIFF_COLORS[d] || DIFF_COLORS.easy;
    var shell = $('#play');
    if(!shell) return;
    shell.style.setProperty('--song-accent', c.accent);
    shell.style.setProperty('--song-accent-text', c.text);
    shell.style.setProperty('--song-accent-on', c.on);
    shell.style.setProperty('--song-accent-rgb', c.rgb);
  }

  var jp = 0;
  function jsonp(url, cb){
    var name = 'jpcb' + (++jp), s = document.createElement('script'), done = false;
    function cleanup(){ try{ delete window[name]; }catch(e){ window[name] = undefined; } if(s.parentNode) s.parentNode.removeChild(s); }
    window[name] = function(data){ if(done) return; done = true; cleanup(); cb(data); };
    s.onerror = function(){ if(done) return; done = true; cleanup(); cb(null); };
    s.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + 'callback=' + name;
    document.body.appendChild(s);
    setTimeout(function(){ if(!done){ done = true; cleanup(); cb(null); } }, 12000);
  }

  var ctx = null, gain = null, pool = [], bufCache = {}, cur = null, VOLUME = 1.0, playTimer = 0, activeSource = null, progressRAF = 0;

  var el = {
    playKey:$('#playKey'), skip:$('#skipBtn'), search:$('#searchInput'), suggestions:$('#suggestions'),
    banner:$('#answerBanner'), status:$('#status'), timeline:$('#timeline'), label:$('#timelineLabel'),
    playStage:$('#playStage'), chips:$('#stageChips'), rail:$('#difficultyList'), tabs:$('#difficultyTabs'),
    genreReel:$('#genreReel'), volume:$('#volume'), reroll:$('#rerollBtn'), badge:$('#filterBadge')
  };

  function getCtx(){
    if(!ctx){
      ctx = new (window.AudioContext||window.webkitAudioContext)();
      gain = ctx.createGain(); gain.gain.value = VOLUME; gain.connect(ctx.destination);
    }
    return ctx;
  }
  function shuffle(a){ for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)), t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
  function norm(s){ return (s||'').toLowerCase().replace(/[^a-z0-9一-鿿]/g,''); }

  function poolUrl(){
    if(ARTIST) return 'https://itunes.apple.com/search?term=' + encodeURIComponent(ARTIST) + '&entity=song&limit=200';
    return GENRE_ID
      ? 'https://itunes.apple.com/us/rss/topsongs/limit=50/genre=' + GENRE_ID + '/json'
      : 'https://itunes.apple.com/us/rss/topsongs/limit=50/json';
  }
  function loadPool(){
    return new Promise(function(resolve, reject){
      if(DECADE){
        var tracks = (window.DECADE_TRACKS && window.DECADE_TRACKS[DECADE]) || [];
        tracks.forEach(function(t){ t.id = t.id || t.preview; });
        pool = shuffle(tracks.slice(0, POOL_LIMIT[DIFF] || 50));
        resolve();
        return;
      }
      jsonp(poolUrl(), function(data){
        var list;
        if(ARTIST){
          var rs = data && data.results;
          if(!rs || !rs.length) return reject(new Error('no artist data'));
          var seen = {};
          list = rs.map(function(r){
            return { id: r.trackId || r.previewUrl || Math.random(), title: r.trackName, artist: r.artistName, preview: r.previewUrl };
          }).filter(function(t){ return t.preview && t.title; })
            .filter(function(t){ var k = norm(t.title); if(seen[k]) return false; seen[k] = true; return true; });
        } else {
          var entry = data && data.feed && data.feed.entry;
          if(!entry) return reject(new Error('no chart data'));
          list = entry.map(function(e){
            var enc = null;
            (e.link || []).forEach(function(l){ if(l.attributes && l.attributes.rel === 'enclosure') enc = l.attributes.href; });
            return {
              id: (e.id && e.id.attributes && e.id.attributes['im:id']) || enc || Math.random(),
              title: e['im:name'] && e['im:name'].label,
              artist: e['im:artist'] && e['im:artist'].label,
              preview: enc
            };
          }).filter(function(t){ return t.preview && t.title; });
        }
        pool = shuffle(list.slice(0, POOL_LIMIT[DIFF] || 50));
        resolve();
      });
    });
  }

  // decode cache
  var decoding = {}, cacheOrder = [];
  function ensureBuffer(track){
    if(bufCache[track.id]) return Promise.resolve(bufCache[track.id]);
    if(decoding[track.id]) return decoding[track.id];
    decoding[track.id] = fetch(track.preview)
      .then(function(r){ if(!r.ok) throw new Error('http ' + r.status); return r.arrayBuffer(); })
      .then(function(ab){ return getCtx().decodeAudioData(ab); })
      .then(function(buf){
        bufCache[track.id] = buf; cacheOrder.push(track.id);
        while(cacheOrder.length > 12){ var old = cacheOrder.shift(); delete bufCache[old]; }
        delete decoding[track.id]; return buf;
      })
      .catch(function(e){ delete decoding[track.id]; throw e; });
    return decoding[track.id];
  }
  function playSlice(track, offset, dur, onStart){
    ensureBuffer(track).then(function(buf){
      if(!cur || cur.done || cur.track.id !== track.id) return;
      getCtx().resume().then(function(){
        if(!cur || cur.done || cur.track.id !== track.id) return;
        var off = Math.max(0, Math.min(offset || 0, buf.duration - 0.01));
        var d = Math.min(dur, buf.duration - off); if(d <= 0) d = dur;
        var s = getCtx().createBufferSource();
        s.buffer = buf; s.connect(gain);
        if(activeSource){ try{ activeSource.stop(); }catch(e){} }
        activeSource = s;
        s.start(0, off, d);
        if(onStart) onStart(d);
      });
    }).catch(function(){ setStatus('Couldn’t load audio — check connection', 'is-failed'); });
  }

  function setStatus(text, cls){
    el.status.textContent = text;
    el.status.className = 'songspot-game-status ' + (cls || '');
  }
  function renderTimeline(){
    $$('.songspot-progress-segment').forEach(function(s){
      var i = +s.getAttribute('data-stage');
      s.classList.toggle('is-active', i <= cur.level);
    });
    var label = REVEALS[cur.level].label;
    el.playStage.textContent = label;
    el.label.textContent = label;
    el.timeline.parentElement.style.setProperty('--timeline-position', POSITION[cur.level] + '%');
    $$('#stageChips .songspot-control-chip').forEach(function(c){
      c.setAttribute('aria-pressed', (+c.getAttribute('data-stage')) === cur.level ? 'true' : 'false');
    });
  }

  function play(){
    if(!cur){ start(); return; }
    if(cur.done){ newRound(); return; }
    getCtx().resume();
    setStatus('Loading clip…', 'is-ready');
    playSlice(cur.track, 0, REVEALS[cur.level].sec, function(d){
      setStatus('Now playing ' + REVEALS[cur.level].label, 'is-playing');
      el.playKey.classList.add('playing');
      el.playKey.style.setProperty('--clip-ms', (d * 1000) + 'ms');
      clearTimeout(playTimer);
      playTimer = setTimeout(function(){ el.playKey.classList.remove('playing'); }, d * 1000);
      // live progress bar, synced to audio via AudioContext time
      var t0 = getCtx().currentTime;
      cancelAnimationFrame(progressRAF);
      (function tick(){
        var p = Math.min(1, (getCtx().currentTime - t0) / d);
        el.timeline.style.setProperty('--playback-progress', (p * 100) + '%');
        el.timeline.setAttribute('data-playback-progress', Math.round(p * 100));
        el.timeline.setAttribute('aria-valuenow', (p * d).toFixed(1));
        if(p < 1 && cur && !cur.done){ progressRAF = requestAnimationFrame(tick); }
        else { el.timeline.style.setProperty('--playback-progress', '0%'); el.timeline.setAttribute('data-playback-progress', '0'); }
      })();
    });
  }

  function newRound(){
    var go = function(){
      cur = { track:pool.splice(Math.floor(Math.random()*pool.length), 1)[0], level:0, done:false };
      ensureBuffer(cur.track).catch(function(){}); // pre-decode so Play is instant and in sync
      cancelAnimationFrame(progressRAF);
      el.timeline.style.setProperty('--playback-progress', '0%');
      el.timeline.setAttribute('data-playback-progress', '0');
      renderTimeline();
      setStatus('Press play', 'is-ready');
      el.banner.classList.remove('show'); el.banner.innerHTML = '';
      el.search.value = ''; el.search.focus();
      closeSuggestions();
    };
    if(pool.length < 1){ loadPool().then(go, function(){ setStatus('Failed to load songs — check connection', 'is-failed'); }); }
    else go();
  }
  function start(){ newRound(); }

  function showAnswer(ok, skipped){
    var t = cur.track;
    el.banner.innerHTML =
      '<span>' + (skipped ? '⏭ Skipped — ' : ok ? '✅ ' : '❌ ') +
      '<b>' + t.title + '</b> — ' + t.artist + '</span> ' +
      '<button type="button" id="nextBtn">Next song →</button>';
    el.banner.classList.add('show');
    var nb = $('#nextBtn'); if(nb) nb.onclick = newRound;
  }

  function guess(track){
    if(!cur || cur.done) return;
    if(track && track.id === cur.track.id){
      cur.done = true;
      setStatus('Correct!', 'is-correct');
      showAnswer(true, false);
    } else if(cur.level < REVEALS.length - 1){
      cur.level++;
      renderTimeline();
      setStatus('Not quite — try a longer clip', 'is-incorrect');
      play();
    } else {
      cur.done = true;
      setStatus('Out of clips', 'is-failed');
      showAnswer(false, false);
    }
  }

  function skip(){
    if(!cur) return;
    if(cur.done){ newRound(); return; }
    if(cur.level < REVEALS.length - 1){
      cur.level++;
      renderTimeline();
      setStatus('Revealing a longer clip', 'is-incorrect');
      play();
    } else {
      cur.done = true;
      setStatus('Out of clips', 'is-failed');
      showAnswer(false, false);
    }
  }

  // ---- suggestions ----
  function closeSuggestions(){ el.suggestions.classList.remove('open'); el.search.setAttribute('aria-expanded','false'); }
  function openSuggestions(list){
    el.suggestions.innerHTML = '';
    list.slice(0, 6).forEach(function(t){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'songspot-suggestion';
      b.innerHTML = '<span>' + t.title + '</span> <span class="art">— ' + t.artist + '</span>';
      b.onclick = function(){ guess(t); closeSuggestions(); };
      el.suggestions.appendChild(b);
    });
    el.suggestions.classList.add('open'); el.search.setAttribute('aria-expanded','true');
  }
  function onType(){
    var v = norm(el.search.value);
    if(!v){ closeSuggestions(); return; }
    var hits = pool.filter(function(t){
      return norm(t.title).indexOf(v) >= 0 || norm(t.artist).indexOf(v) >= 0;
    });
    if(hits.length) openSuggestions(hits); else closeSuggestions();
  }
  function submit(){
    var v = norm(el.search.value);
    if(!v){ setStatus('Type a song or artist', 'is-incorrect'); return; }
    var exact = pool.filter(function(t){ return norm(t.title) === v || norm(t.artist) === v; })[0];
    if(exact){ guess(exact); closeSuggestions(); return; }
    var partial = pool.filter(function(t){ return norm(t.title).indexOf(v) >= 0 || norm(t.artist).indexOf(v) >= 0; })[0];
    if(partial){ guess(partial); closeSuggestions(); }
    else setStatus('No match — keep typing', 'is-incorrect');
  }

  // ---- difficulty ----
  function setDiff(d){
    DIFF = d || 'easy';
    applyDiffColor(DIFF);
    $$('#difficultyList .songspot-difficulty-row').forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-d') === DIFF ? 'true':'false'); });
    $$('#difficultyTabs .songspot-difficulty-tab').forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-d') === DIFF ? 'true':'false'); });
    pool = []; bufCache = {}; cur = null;
    loadPool().then(newRound, function(){ setStatus('Failed to load songs — check connection', 'is-failed'); });
  }
  // ---- genre ----
  function setGenre(id, scroll){
    GENRE_ID = id || null;
    ARTIST = null;
    DECADE = null;
    pool = []; bufCache = {}; cur = null;
    renderBadge();
    loadPool().then(newRound, function(){ setStatus('Failed to load songs — check connection', 'is-failed'); });
    if(scroll){ var g = $('#play'); if(g) g.scrollIntoView({behavior:'smooth', block:'start'}); }
  }
  // ---- artist ----
  function setArtist(name){
    ARTIST = name || null;
    GENRE_ID = null;
    DECADE = null;
    pool = []; bufCache = {}; cur = null;
    renderBadge();
    loadPool().then(newRound, function(){ setStatus('Failed to load songs — check connection', 'is-failed'); });
  }
  // ---- decade ----
  function setDecade(name){
    DECADE = name || null;
    GENRE_ID = null;
    ARTIST = null;
    pool = []; bufCache = {}; cur = null;
    renderBadge();
    loadPool().then(newRound, function(){ setStatus('Failed to load songs — check connection', 'is-failed'); });
  }
  // ---- filter badge + reels ----
  function syncReels(){
    $$('#genreReel [data-genre]').forEach(function(x){
      x.setAttribute('aria-pressed', (GENRE_ID ? x.getAttribute('data-genre') === String(GENRE_ID) : x.getAttribute('data-genre') === '') ? 'true' : 'false');
    });
    $$('[data-decade]').forEach(function(x){
      x.setAttribute('aria-pressed', (DECADE ? x.getAttribute('data-decade') === DECADE : x.getAttribute('data-decade') === '') ? 'true' : 'false');
    });
    $$('[data-artist]').forEach(function(x){
      x.setAttribute('aria-pressed', (ARTIST ? x.getAttribute('data-artist') === ARTIST : x.getAttribute('data-artist') === '') ? 'true' : 'false');
    });
  }
  function renderBadge(){
    syncReels();
    var label = '';
    if(DECADE) label = 'Decade: ' + DECADE;
    else if(ARTIST) label = 'Artist: ' + ARTIST;
    else if(GENRE_ID) label = 'Genre: ' + (GENRE_NAMES[GENRE_ID] || GENRE_ID);
    if(!label){ el.badge.hidden = true; el.badge.innerHTML = ''; return; }
    el.badge.innerHTML = '<span>Now playing — ' + label + '</span><button type="button" aria-label="Clear filter">✕</button>';
    el.badge.hidden = false;
    el.badge.querySelector('button').onclick = clearFilter;
  }
  function clearFilter(){
    GENRE_ID = null; ARTIST = null; DECADE = null;
    pool = []; bufCache = {}; cur = null;
    if(history.replaceState) history.replaceState(null, '', location.pathname);
    renderBadge();
    loadPool().then(newRound, function(){ setStatus('Failed to load songs — check connection', 'is-failed'); });
  }

  // ---- bindings ----
  el.playKey.addEventListener('click', play);
  el.skip.addEventListener('click', skip);
  el.search.addEventListener('input', onType);
  el.search.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ e.preventDefault(); submit(); } });
  el.search.addEventListener('blur', function(){ setTimeout(closeSuggestions, 120); });
  el.reroll.addEventListener('click', function(){ if(pool.length < 1) loadPool().then(newRound); else newRound(); });

  $$('#stageChips .songspot-control-chip').forEach(function(c){
    c.addEventListener('click', function(){
      if(!cur || cur.done) return;
      cur.level = +c.getAttribute('data-stage');
      renderTimeline(); play();
    });
  });
  $$('#difficultyList .songspot-difficulty-row').forEach(function(b){ b.addEventListener('click', function(){ setDiff(b.getAttribute('data-d')); }); });
  $$('#difficultyTabs .songspot-difficulty-tab').forEach(function(b){ b.addEventListener('click', function(){ setDiff(b.getAttribute('data-d')); }); });
  $$('#genreReel [data-genre]').forEach(function(b){
    b.addEventListener('click', function(){
      var id = b.getAttribute('data-genre');
      setGenre(id ? parseInt(id,10) : null, false);
    });
  });
  $$('[data-decade]').forEach(function(b){
    b.addEventListener('click', function(){
      setDecade(b.getAttribute('data-decade') || null);
    });
  });
  $$('[data-artist]').forEach(function(b){
    b.addEventListener('click', function(){
      setArtist(b.getAttribute('data-artist') || null);
    });
  });
  el.volume.addEventListener('input', function(){
    VOLUME = (el.volume.value|0)/100;
    el.volume.style.setProperty('--fill', el.volume.value + '%');
    if(gain) gain.gain.value = VOLUME;
  });

  // Apply the initial filter from window.SONG_INITIAL (subpages) or ?genre/?artist/?decade (directory links) before the first pool loads.
  (function(){
    var init = window.SONG_INITIAL || {};
    var g = /[?&]genre=(\d+)/.exec(location.search);
    var a = /[?&]artist=([^&]+)/.exec(location.search);
    var d = /[?&]decade=([^&]+)/.exec(location.search);
    if(init.artist){ ARTIST = init.artist; }
    else if(init.decade){ DECADE = init.decade; }
    else if(init.genre != null){ GENRE_ID = init.genre; }
    else if(d){ DECADE = decodeURIComponent(d[1].replace(/\+/g, ' ')); }
    else if(a){ ARTIST = decodeURIComponent(a[1].replace(/\+/g, ' ')); }
    else if(g){ GENRE_ID = parseInt(g[1], 10); }
    renderBadge();
  })();

  // Preload the pool so the first Play responds instantly (decode happens on first Play).
  loadPool().catch(function(){});
})();
