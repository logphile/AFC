// Abbott Family Chiropractic — small, dependency-free helpers.

(function () {
  // ---- Mobile menu ----
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.querySelector('.menu-label').textContent = open ? 'Close' : 'Menu';
    });
  }

  // ---- Office hours (single source of truth) ----
  // Days: 0 = Sunday ... 6 = Saturday. Times in 24h, Eastern time.
  var HOURS = {
    hampton: {
      2: [['9:30', '13:00'], ['15:00', '19:00']],
      4: [['9:30', '13:00'], ['15:00', '19:00']],
      5: [['9:30', '13:00'], ['15:00', '17:00']]
    },
    gloucester: {
      1: [['9:00', '13:00'], ['15:00', '17:30']],
      3: [['10:00', '13:00'], ['15:00', '17:30']]
    }
  };
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function fmt(t) {
    var p = t.split(':'), h = +p[0], m = p[1];
    var ampm = h >= 12 ? 'pm' : 'am';
    h = h % 12 || 12;
    return m === '00' ? h + ' ' + ampm : h + ':' + m + ' ' + ampm;
  }
  function toMin(t) { var p = t.split(':'); return +p[0] * 60 + +p[1]; }

  // Current day/time in Eastern, regardless of the visitor's own time zone.
  var now = new Date();
  var et = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
  var day = et.getDay();
  var mins = et.getHours() * 60 + et.getMinutes();

  function status(office) {
    var blocks = HOURS[office][day];
    if (!blocks) return { open: false, text: 'Closed today' };
    for (var i = 0; i < blocks.length; i++) {
      var s = toMin(blocks[i][0]), e = toMin(blocks[i][1]);
      if (mins >= s && mins < e) return { open: true, text: 'Open now until ' + fmt(blocks[i][1]) };
      if (mins < s) return { open: false, text: 'Opens today at ' + fmt(blocks[i][0]) };
    }
    return { open: false, text: 'Closed for the day' };
  }

  document.querySelectorAll('[data-status]').forEach(function (el) {
    var st = status(el.getAttribute('data-status'));
    var dot = el.querySelector('.dot');
    var txt = el.querySelector('.status-text');
    if (dot) dot.classList.toggle('open', st.open);
    if (txt) txt.textContent = st.text;
  });

  var todayName = document.querySelector('[data-today-name]');
  if (todayName) todayName.textContent = DAYS[day];

  // Highlight today's row in any hours table.
  document.querySelectorAll('.hours tr[data-day]').forEach(function (row) {
    if (+row.getAttribute('data-day') === day) row.classList.add('is-today');
  });

  // ---- Appointment request (preview only) ----
  var form = document.getElementById('appt-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      form.hidden = true;
      var ok = document.getElementById('appt-success');
      ok.classList.add('show');
      ok.focus();
    });
  }

  // ---- Footer year ----
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = et.getFullYear(); });
})();
