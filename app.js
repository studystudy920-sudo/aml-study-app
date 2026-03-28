/* ===== State ===== */
let DATA = { exams: [], questions: { exams: [] }, reference: {} };
let state = {
  quizExam: null, quizMode: 'random', quizChapter: null,
  quizQuestions: [], quizIndex: 0, quizAnswered: false,
  quizCorrect: 0, quizWrong: 0, streak: 0, maxStreak: 0,
  flashIndex: 0, flashTerms: [],
  refTab: 'glossary',
  timerSec: 120, timerInterval: null, timerRemaining: 0
};
const storage = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d } catch { return d } },
  set(k, v) { localStorage.setItem(k, JSON.stringify(v)) }
};
let studyLog = storage.get('studyLog', []);
let quizResults = storage.get('quizResults', {});
let chapterProgress = storage.get('chapterProgress', {});
let badges = storage.get('badges', {});
let totalQuizzes = storage.get('totalQuizzes', 0);
let totalCorrect = storage.get('totalCorrect', 0);

/* ===== Badge Definitions ===== */
const BADGES = [
  { id: 'first_quiz', icon: '\u{1F31F}', name: '初挑戦', desc: '初めてクイズを完了' },
  { id: 'perfect', icon: '\u{1F48E}', name: 'パーフェクト', desc: '全問正解を達成' },
  { id: 'streak5', icon: '\u{1F525}', name: '5連続正解', desc: '5問連続で正解' },
  { id: 'streak10', icon: '\u{26A1}', name: '10連続正解', desc: '10問連続で正解' },
  { id: 'quiz50', icon: '\u{1F4AA}', name: '50問突破', desc: '累計50問に回答' },
  { id: 'quiz200', icon: '\u{1F3AF}', name: '200問突破', desc: '累計200問に回答' },
  { id: 'study7', icon: '\u{1F4C5}', name: '7日連続', desc: '7日連続で学習記録' },
  { id: 'master', icon: '\u{1F451}', name: '全章制覇', desc: 'いずれかの試験で全章完了' },
  { id: 'speed', icon: '\u{23F1}', name: 'スピードスター', desc: 'タイマーモードで80%以上' },
];

/* ===== Init ===== */
async function init() {
  try {
    const [exams, questions, reference] = await Promise.all([
      fetch('./data/exams.json').then(r => r.json()),
      fetch('./data/questions.json').then(r => r.json()),
      fetch('./data/reference.json').then(r => r.json())
    ]);
    DATA = { exams: exams.exams, questions, reference };
  } catch (e) { console.warn('Data load error:', e) }
  setupTabs(); setupQuiz(); setupProgress(); setupReference(); setupBadges();
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js');
}

/* ===== Tabs ===== */
function setupTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab).classList.add('active');
      if (btn.dataset.tab === 'progress') renderProgress();
      if (btn.dataset.tab === 'reference') renderReference();
      if (btn.dataset.tab === 'badges') renderBadges();
    });
  });
}

/* ===== QUIZ ===== */
function setupQuiz() {
  renderExamList();
  document.querySelectorAll('.quiz-mode-btns button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.quiz-mode-btns button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.quizMode = btn.dataset.mode;
      document.getElementById('quiz-chapter-select').classList.toggle('hidden', state.quizMode !== 'chapter');
      document.getElementById('timer-config').classList.toggle('hidden', state.quizMode !== 'timer');
      if (state.quizMode === 'chapter' && state.quizExam) renderChapterSelect();
    });
  });
  // Timer config
  document.querySelectorAll('#timer-config button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#timer-config button').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      state.timerSec = parseInt(btn.dataset.sec);
    });
  });
  document.getElementById('quiz-start-btn').addEventListener('click', startQuiz);
  document.getElementById('quiz-next-btn').addEventListener('click', nextQuestion);
  document.getElementById('quiz-end-btn').addEventListener('click', endQuiz);
  document.getElementById('quiz-retry-btn').addEventListener('click', () => showQuizView('home'));
  document.getElementById('flashcard').addEventListener('click', () =>
    document.getElementById('flashcard').classList.toggle('flipped'));
  document.getElementById('flash-next').addEventListener('click', () => navigateFlash(1));
  document.getElementById('flash-prev').addEventListener('click', () => navigateFlash(-1));
  document.getElementById('flash-end').addEventListener('click', () => showQuizView('home'));
}

function renderExamList() {
  const el = document.getElementById('quiz-exam-list');
  const qExams = DATA.questions.exams || [];
  const exams = DATA.exams.filter(e => qExams.some(qe => qe.id === e.id));
  const list = exams.length ? exams : DATA.exams;
  el.innerHTML = list.map(e =>
    `<button data-id="${e.id}" ${state.quizExam === e.id ? 'class="selected"' : ''}>${e.name}</button>`
  ).join('');
  el.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      el.querySelectorAll('button').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      state.quizExam = btn.dataset.id;
      if (state.quizMode === 'chapter') renderChapterSelect();
    });
  });
}

function renderChapterSelect() {
  const exam = DATA.exams.find(e => e.id === state.quizExam);
  const el = document.getElementById('quiz-chapter-select');
  if (!exam || !exam.chapters.length) { el.innerHTML = '<p class="text-muted text-sm">章データなし</p>'; return; }
  el.innerHTML = exam.chapters.map(ch =>
    `<button data-id="${ch.id}" ${state.quizChapter === ch.id ? 'class="selected"' : ''}>${ch.name}</button>`
  ).join('');
  el.classList.remove('hidden');
  el.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      el.querySelectorAll('button').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      state.quizChapter = btn.dataset.id;
    });
  });
}

function getQuestions() {
  const qExam = (DATA.questions.exams || []).find(e => e.id === state.quizExam);
  if (!qExam) return [];
  let qs = [];
  if (state.quizMode === 'chapter' && state.quizChapter) {
    const ch = qExam.chapters.find(c => c.id === state.quizChapter);
    qs = ch ? ch.questions : [];
  } else if (state.quizMode === 'weak') {
    qExam.chapters.forEach(ch => ch.questions.forEach(q => {
      const r = quizResults[q.id];
      if (r && r.wrong > 0) qs.push(q);
    }));
  } else {
    qExam.chapters.forEach(ch => qs.push(...ch.questions));
  }
  return shuffle([...qs]);
}

function startQuiz() {
  if (!state.quizExam) return;
  if (state.quizMode === 'flash') { startFlashcard(); return; }
  const qs = getQuestions();
  if (!qs.length) { alert('問題がありません'); return; }
  state.quizQuestions = qs;
  state.quizIndex = 0; state.quizCorrect = 0; state.quizWrong = 0;
  state.quizAnswered = false; state.streak = 0; state.maxStreak = 0;
  showQuizView('play');
  document.getElementById('timer-bar').classList.toggle('hidden', state.quizMode !== 'timer');
  renderQuestion();
}

function renderQuestion() {
  const q = state.quizQuestions[state.quizIndex];
  if (!q) { endQuiz(); return; }
  state.quizAnswered = false;
  document.getElementById('quiz-next-btn').disabled = true;
  document.getElementById('quiz-explanation').classList.add('hidden');
  document.getElementById('quiz-progress-label').textContent =
    `問題 ${state.quizIndex + 1} / ${state.quizQuestions.length}`;
  document.getElementById('quiz-question').textContent = q.question;
  renderStats();
  const optEl = document.getElementById('quiz-options');
  optEl.innerHTML = q.options.map((o, i) =>
    `<button class="option-btn" data-idx="${i}">${o}</button>`).join('');
  optEl.querySelectorAll('.option-btn').forEach(btn =>
    btn.addEventListener('click', () => answerQuestion(parseInt(btn.dataset.idx))));
  if (state.quizMode === 'timer') startTimer();
}

function renderStats() {
  const remaining = state.quizQuestions.length - state.quizIndex - (state.quizAnswered ? 1 : 0);
  document.getElementById('quiz-stats').innerHTML =
    `<span class="stat-chip green">正解 ${state.quizCorrect}</span>` +
    `<span class="stat-chip red">不正解 ${state.quizWrong}</span>` +
    `<span class="stat-chip blue">残り ${remaining}</span>` +
    (state.streak >= 3 ? `<span class="stat-chip" style="background:rgba(251,191,36,.12);color:var(--gold);border-color:rgba(251,191,36,.2)">\u{1F525} ${state.streak}連続</span>` : '');
}

function answerQuestion(idx) {
  if (state.quizAnswered) return;
  state.quizAnswered = true;
  stopTimer();
  const q = state.quizQuestions[state.quizIndex];
  const correct = idx === q.answer;
  if (correct) { state.quizCorrect++; state.streak++; state.maxStreak = Math.max(state.maxStreak, state.streak); }
  else { state.quizWrong++; state.streak = 0; }
  totalQuizzes++; if (correct) totalCorrect++;
  storage.set('totalQuizzes', totalQuizzes); storage.set('totalCorrect', totalCorrect);

  const r = quizResults[q.id] || { correct: 0, wrong: 0 };
  if (correct) r.correct++; else r.wrong++;
  r.lastAttempt = today();
  quizResults[q.id] = r;
  storage.set('quizResults', quizResults);

  const btns = document.querySelectorAll('#quiz-options .option-btn');
  btns.forEach((btn, i) => {
    if (i === q.answer) btn.classList.add('correct');
    else if (i === idx) btn.classList.add('wrong');
    else btn.classList.add('reveal');
  });
  document.getElementById('quiz-explanation').textContent = q.explanation;
  document.getElementById('quiz-explanation').classList.remove('hidden');
  document.getElementById('quiz-next-btn').disabled = false;
  renderStats();
  checkBadges();
}

function nextQuestion() {
  state.quizIndex++;
  if (state.quizIndex >= state.quizQuestions.length) { endQuiz(); return; }
  renderQuestion();
}

function endQuiz() {
  stopTimer();
  const total = state.quizCorrect + state.quizWrong;
  const pct = total > 0 ? Math.round(state.quizCorrect / total * 100) : 0;
  const color = pct >= 70 ? 'var(--success)' : pct >= 50 ? 'var(--warning)' : 'var(--danger)';

  document.getElementById('result-score').textContent = `${pct}%`;
  document.getElementById('result-score').style.color = color;
  document.getElementById('result-detail').textContent =
    `${total}問中 ${state.quizCorrect}問正解` +
    (state.maxStreak >= 3 ? ` | 最大${state.maxStreak}連続正解` : '');

  // Animate ring
  const fg = document.getElementById('ring-fg');
  fg.style.stroke = color;
  const circumference = 326.73;
  requestAnimationFrame(() => {
    fg.style.strokeDashoffset = circumference;
    requestAnimationFrame(() => {
      fg.style.strokeDashoffset = circumference * (1 - pct / 100);
    });
  });

  // Wrong list
  const wrongList = document.getElementById('result-wrong-list');
  const wrongs = state.quizQuestions.filter(q => {
    const r = quizResults[q.id];
    return r && r.wrong > r.correct;
  });
  wrongList.innerHTML = wrongs.length ? '<h3 class="mb-8" style="margin-top:14px">要復習</h3>' +
    wrongs.map(q => `<div class="card"><div class="text-sm">${q.question}</div>
      <div class="text-sm text-muted" style="margin-top:6px">${q.explanation}</div></div>`).join('') : '';

  showQuizView('result');
  if (pct === 100) spawnConfetti();
  checkBadges();
}

/* Timer */
function startTimer() {
  stopTimer();
  state.timerRemaining = state.timerSec;
  const display = document.getElementById('timer-display');
  const fill = document.getElementById('timer-fill');
  fill.style.width = '100%';
  display.classList.remove('urgent');
  updateTimerDisplay();
  state.timerInterval = setInterval(() => {
    state.timerRemaining--;
    updateTimerDisplay();
    fill.style.width = (state.timerRemaining / state.timerSec * 100) + '%';
    if (state.timerRemaining <= 10) display.classList.add('urgent');
    if (state.timerRemaining <= 0) { stopTimer(); autoAnswer(); }
  }, 1000);
}

function stopTimer() {
  if (state.timerInterval) { clearInterval(state.timerInterval); state.timerInterval = null; }
}

function updateTimerDisplay() {
  const m = Math.floor(state.timerRemaining / 60);
  const s = state.timerRemaining % 60;
  document.getElementById('timer-display').textContent = `${m}:${String(s).padStart(2, '0')}`;
}

function autoAnswer() {
  if (!state.quizAnswered) {
    state.quizAnswered = true;
    state.quizWrong++; state.streak = 0;
    totalQuizzes++; storage.set('totalQuizzes', totalQuizzes);
    const q = state.quizQuestions[state.quizIndex];
    const r = quizResults[q.id] || { correct: 0, wrong: 0 }; r.wrong++; r.lastAttempt = today();
    quizResults[q.id] = r; storage.set('quizResults', quizResults);
    const btns = document.querySelectorAll('#quiz-options .option-btn');
    btns.forEach((btn, i) => { if (i === q.answer) btn.classList.add('correct'); else btn.classList.add('reveal'); });
    document.getElementById('quiz-explanation').textContent = '\u{23F0} 時間切れ！ ' + q.explanation;
    document.getElementById('quiz-explanation').classList.remove('hidden');
    document.getElementById('quiz-next-btn').disabled = false;
    renderStats();
  }
}

/* Flashcard */
function startFlashcard() {
  const ref = DATA.reference;
  if (!ref.glossary || !ref.glossary.length) { alert('用語データがありません'); return; }
  state.flashTerms = shuffle([...ref.glossary]);
  state.flashIndex = 0;
  showQuizView('flash');
  renderFlashcard();
}
function renderFlashcard() {
  const t = state.flashTerms[state.flashIndex];
  if (!t) return;
  document.getElementById('flashcard').classList.remove('flipped');
  document.getElementById('flash-front').innerHTML =
    `<div><div style="font-size:1.6rem;font-weight:900">${t.term}</div>
     <div class="text-muted text-sm" style="margin-top:10px">${t.full || ''}</div></div>`;
  document.getElementById('flash-back').innerHTML =
    `<div><div class="fw-700">${t.ja || t.term}</div>
     <div style="margin-top:10px;line-height:1.7">${t.description}</div></div>`;
  document.getElementById('flash-progress').textContent =
    `${state.flashIndex + 1} / ${state.flashTerms.length}`;
}
function navigateFlash(dir) {
  state.flashIndex = Math.max(0, Math.min(state.flashTerms.length - 1, state.flashIndex + dir));
  renderFlashcard();
}

function showQuizView(view) {
  ['quiz-home', 'quiz-play', 'quiz-flash', 'quiz-result'].forEach(id =>
    document.getElementById(id).classList.add('hidden'));
  document.getElementById(view === 'home' ? 'quiz-home' : view === 'play' ? 'quiz-play' :
    view === 'flash' ? 'quiz-flash' : 'quiz-result').classList.remove('hidden');
}

/* ===== PROGRESS ===== */
function setupProgress() {
  const sel = document.getElementById('log-exam');
  sel.innerHTML = '<option value="">-- 試験を選択 --</option>' +
    DATA.exams.map(e => `<option value="${e.id}">${e.name}</option>`).join('');
  document.querySelectorAll('.time-btns button').forEach(btn => {
    btn.addEventListener('click', () => {
      const min = btn.dataset.min;
      if (min === 'custom') {
        const v = prompt('学習時間（分）を入力:');
        if (v && !isNaN(v)) addStudyLog(parseInt(v));
      } else addStudyLog(parseInt(min));
    });
  });
}
function addStudyLog(minutes) {
  const exam = document.getElementById('log-exam').value;
  const note = document.getElementById('log-note').value;
  studyLog.push({ date: today(), exam: exam || 'general', minutes, note });
  storage.set('studyLog', studyLog);
  document.getElementById('log-note').value = '';
  renderProgress(); checkBadges();
}
function renderProgress() {
  renderCountdown(); renderHeatmap(); renderTodayLog(); renderChapterProgress();
}
function renderCountdown() {
  const el = document.getElementById('countdown');
  const upcoming = DATA.exams.filter(e => e.date).sort((a, b) => a.date.localeCompare(b.date));
  el.innerHTML = upcoming.slice(0, 4).map(e => {
    const days = diffDays(today(), e.date);
    const urgent = days <= 14;
    return `<div class="countdown-card">
      <div class="exam-name">${e.name}</div>
      <div class="days ${urgent ? 'urgent' : ''}">${days >= 0 ? days : '\u2705'}</div>
      <div class="label">${days >= 0 ? '日後' : '終了'} (${e.date})</div>
    </div>`;
  }).join('');
}
function renderHeatmap() {
  const el = document.getElementById('heatmap');
  const d = new Date(); const cells = [];
  const dayOffset = (d.getDay() + 6) % 7;
  const startDate = new Date(d); startDate.setDate(d.getDate() - 27 - dayOffset);
  let totalMin = 0, studyDays = 0;
  for (let i = 0; i < 35; i++) {
    const cd = new Date(startDate); cd.setDate(startDate.getDate() + i);
    const ds = formatDate(cd);
    const mins = studyLog.filter(l => l.date === ds).reduce((s, l) => s + l.minutes, 0);
    if (mins > 0) { totalMin += mins; studyDays++; }
    const level = mins === 0 ? '' : mins < 30 ? 'l1' : mins < 60 ? 'l2' : mins < 120 ? 'l3' : 'l4';
    const isFuture = cd > d;
    cells.push(`<div class="heatmap-cell ${level}" title="${ds}: ${mins}分" ${isFuture ? 'style="opacity:.2"' : ''}></div>`);
  }
  el.innerHTML = cells.join('');
  document.getElementById('heatmap-summary').textContent =
    `過去28日: ${studyDays}日学習 / 合計${totalMin}分（${Math.round(totalMin / 60 * 10) / 10}時間）`;
}
function renderTodayLog() {
  const todayLogs = studyLog.filter(l => l.date === today());
  const total = todayLogs.reduce((s, l) => s + l.minutes, 0);
  document.getElementById('log-today').textContent =
    total > 0 ? `今日の学習: ${total}分` : 'まだ記録がありません';
}
function renderChapterProgress() {
  const el = document.getElementById('chapter-progress');
  let html = '';
  const levels = { '未着手': 0, '1周目': 25, '2周目': 50, '3周目以上': 75, '完了': 100 };
  DATA.exams.filter(e => e.chapters && e.chapters.length).forEach(exam => {
    const cp = chapterProgress[exam.id] || {};
    html += `<div class="mb-16"><div class="fw-700 mb-8">${exam.name}</div>`;
    exam.chapters.forEach(ch => {
      const status = cp[ch.id] || '未着手';
      const pct = levels[status] || 0;
      const gradient = pct === 100 ? 'var(--success)' : pct >= 50 ?
        'linear-gradient(90deg,var(--accent),var(--accent2))' : 'var(--text-secondary)';
      html += `<div class="mb-8">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span class="text-sm">${ch.name}${ch.points ? ` (${ch.points}点)` : ''}</span>
          <select class="text-sm" data-exam="${exam.id}" data-ch="${ch.id}" style="padding:4px 8px;border-radius:8px;border:1px solid var(--glass-border);background:var(--glass);color:var(--text);font-size:.75rem;backdrop-filter:blur(10px)">
            ${Object.keys(levels).map(l => `<option ${l === status ? 'selected' : ''}>${l}</option>`).join('')}
          </select>
        </div>
        <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${pct}%;background:${gradient}"></div></div>
      </div>`;
    });
    html += '</div>';
  });
  el.innerHTML = html;
  el.querySelectorAll('select').forEach(sel => {
    sel.addEventListener('change', () => {
      if (!chapterProgress[sel.dataset.exam]) chapterProgress[sel.dataset.exam] = {};
      chapterProgress[sel.dataset.exam][sel.dataset.ch] = sel.value;
      storage.set('chapterProgress', chapterProgress);
      renderChapterProgress(); checkBadges();
    });
  });
}

/* ===== REFERENCE ===== */
function setupReference() {
  document.querySelectorAll('.ref-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.ref-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.refTab = btn.dataset.ref;
      renderReference();
    });
  });
  document.getElementById('ref-search').addEventListener('input', () => renderReference());
}
function renderReference() {
  const ref = DATA.reference;
  const q = (document.getElementById('ref-search').value || '').toLowerCase();
  const el = document.getElementById('ref-content');

  if (state.refTab === 'glossary') {
    const items = (ref.glossary || []).filter(g =>
      !q || g.term.toLowerCase().includes(q) || (g.ja || '').includes(q) ||
      (g.full || '').toLowerCase().includes(q) || (g.description || '').includes(q));
    el.innerHTML = items.map(g =>
      `<div class="glossary-item"><div class="glossary-term">${g.term}</div>
       <div class="glossary-full">${g.full || ''} ${g.ja ? '/ ' + g.ja : ''}</div>
       <div class="glossary-desc">${g.description}</div></div>`
    ).join('') || '<p class="text-muted">該当なし</p>';
  } else if (state.refTab === 'fatf40') {
    const items = (ref.fatf40 || []).filter(r =>
      !q || r.title.includes(q) || r.summary.includes(q) || String(r.number).includes(q));
    el.innerHTML = items.map(r =>
      `<div class="card"><div class="fw-700 text-sm" style="color:var(--accent)">勧告${r.number}</div>
       <div class="fw-700">${r.title}</div>
       <div class="text-sm" style="margin-top:6px;color:rgba(255,255,255,.7)">${r.summary}</div></div>`
    ).join('') || '<p class="text-muted">該当なし</p>';
  } else if (state.refTab === 'regulations') {
    const items = (ref.regulations || []).filter(r =>
      !q || r.name.includes(q) || r.summary.includes(q) || r.jurisdiction.includes(q));
    const jColor = { '日本': '#ef4444', 'EU': '#8b5cf6', '米国': '#f59e0b', '国際': '#6366f1' };
    el.innerHTML = items.map(r =>
      `<div class="card">
       <span class="stat-chip" style="background:${jColor[r.jurisdiction] || '#6366f1'}15;color:${jColor[r.jurisdiction] || '#6366f1'};border:1px solid ${jColor[r.jurisdiction] || '#6366f1'}30;display:inline-block;margin-bottom:8px">${r.jurisdiction}</span>
       <div class="fw-700">${r.name} <span class="text-muted text-sm">(${r.year})</span></div>
       <div class="text-sm" style="margin-top:6px;color:rgba(255,255,255,.7)">${r.summary}</div></div>`
    ).join('') || '<p class="text-muted">該当なし</p>';
  } else if (state.refTab === 'comparisons') {
    const rows = ref.comparisons || [];
    el.innerHTML = `<div style="overflow-x:auto"><table class="compare-table">
      <thead><tr><th>観点</th><th>日本</th><th>EU</th><th>米国</th></tr></thead>
      <tbody>${rows.map(r =>
        `<tr><td>${r.aspect}</td><td>${r.japan}</td><td>${r.eu}</td><td>${r.us}</td></tr>`
      ).join('')}</tbody></table></div>`;
  }
}

/* ===== BADGES ===== */
function setupBadges() { renderBadges(); }
function renderBadges() {
  const grid = document.getElementById('badge-grid');
  grid.innerHTML = BADGES.map(b => {
    const unlocked = !!badges[b.id];
    return `<div class="badge ${unlocked ? 'unlocked' : 'locked'}">
      <span class="badge-icon">${b.icon}</span>
      <div class="badge-name">${b.name}</div>
      <div class="badge-desc">${b.desc}</div>
    </div>`;
  }).join('');

  const stats = document.getElementById('overall-stats');
  const unlockCount = Object.keys(badges).length;
  stats.innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
      <div class="card text-center"><div style="font-size:1.5rem;font-weight:800;color:var(--accent)">${totalQuizzes}</div><div class="text-sm text-muted">回答数</div></div>
      <div class="card text-center"><div style="font-size:1.5rem;font-weight:800;color:var(--success)">${totalQuizzes > 0 ? Math.round(totalCorrect / totalQuizzes * 100) : 0}%</div><div class="text-sm text-muted">正答率</div></div>
      <div class="card text-center"><div style="font-size:1.5rem;font-weight:800;color:var(--gold)">${unlockCount}/${BADGES.length}</div><div class="text-sm text-muted">バッジ</div></div>
      <div class="card text-center"><div style="font-size:1.5rem;font-weight:800;color:var(--accent2)">${studyLog.reduce((s, l) => s + l.minutes, 0)}</div><div class="text-sm text-muted">学習(分)</div></div>
    </div>`;
}

function checkBadges() {
  const unlock = (id) => {
    if (badges[id]) return;
    badges[id] = { date: today() };
    storage.set('badges', badges);
    showBadgeToast(BADGES.find(b => b.id === id));
  };
  if (totalQuizzes >= 1) unlock('first_quiz');
  if (state.quizCorrect > 0 && state.quizWrong === 0 && state.quizQuestions.length >= 5 && state.quizAnswered) unlock('perfect');
  if (state.maxStreak >= 5) unlock('streak5');
  if (state.maxStreak >= 10) unlock('streak10');
  if (totalQuizzes >= 50) unlock('quiz50');
  if (totalQuizzes >= 200) unlock('quiz200');
  // 7 consecutive days
  const last7 = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(); d.setDate(d.getDate() - i);
    last7.push(formatDate(d));
  }
  if (last7.every(d => studyLog.some(l => l.date === d))) unlock('study7');
  // All chapters complete
  DATA.exams.forEach(exam => {
    if (exam.chapters.length > 0) {
      const cp = chapterProgress[exam.id] || {};
      if (exam.chapters.every(ch => cp[ch.id] === '完了')) unlock('master');
    }
  });
  // Speed badge
  if (state.quizMode === 'timer') {
    const total = state.quizCorrect + state.quizWrong;
    if (total >= 10 && state.quizCorrect / total >= 0.8) unlock('speed');
  }
}

function showBadgeToast(badge) {
  if (!badge) return;
  const toast = document.getElementById('badge-toast');
  toast.innerHTML = `${badge.icon} ${badge.name} 獲得！`;
  toast.classList.add('show');
  spawnConfetti();
  setTimeout(() => toast.classList.remove('show'), 3000);
}

/* ===== Effects ===== */
function spawnConfetti() {
  const container = document.getElementById('confetti');
  const colors = ['#6366f1', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#fbbf24'];
  for (let i = 0; i < 40; i++) {
    const el = document.createElement('div');
    el.className = 'confetti';
    el.style.left = Math.random() * 100 + '%';
    el.style.background = colors[Math.random() * colors.length | 0];
    el.style.animationDelay = Math.random() * .8 + 's';
    el.style.animationDuration = (1.5 + Math.random()) + 's';
    el.style.width = (6 + Math.random() * 6) + 'px';
    el.style.height = (6 + Math.random() * 6) + 'px';
    container.appendChild(el);
  }
  setTimeout(() => { container.innerHTML = ''; }, 3000);
}

/* ===== Helpers ===== */
function today() { return formatDate(new Date()) }
function formatDate(d) { return d.toISOString().slice(0, 10) }
function diffDays(a, b) { return Math.ceil((new Date(b) - new Date(a)) / 86400000) }
function shuffle(arr) { for (let i = arr.length - 1; i > 0; i--) { const j = Math.random() * (i + 1) | 0; [arr[i], arr[j]] = [arr[j], arr[i]] } return arr }

document.addEventListener('DOMContentLoaded', init);
