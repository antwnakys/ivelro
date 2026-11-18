(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var root = document.documentElement;

  // Footer year
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Header: solid background once the page scrolls
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 24); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Hero title: word-by-word reveal
  var title = document.querySelector('[data-split]');
  if (title && !reduce) {
    var words = title.textContent.trim().split(/\s+/);
    title.setAttribute('aria-label', title.textContent.trim());
    title.innerHTML = words.map(function (w, i) {
      return '<span class="w" aria-hidden="true"><span style="--i:' + i + '">' + w + '</span></span>';
    }).join(' ');
    title.classList.add('split');
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  var steps = document.querySelector('.steps');
  if (!hasIO || reduce) {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    root.classList.add('js-reveal');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });

    if (steps) {
      var so = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { steps.classList.add('is-drawn'); so.disconnect(); }
      }, { rootMargin: '0px 0px -20% 0px' });
      so.observe(steps);
    }
  }

  // Scroll-spy: highlight the nav link of the section in view
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  if (hasIO && links.length) {
    var map = {};
    links.forEach(function (a) {
      var t = document.querySelector(a.getAttribute('href'));
      if (t) map[t.id] = a;
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('is-active'); });
          if (map[e.target.id]) map[e.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { spy.observe(document.getElementById(id)); });
    // Clear when back at the top
    window.addEventListener('scroll', function () {
      if (window.scrollY < window.innerHeight * 0.4) links.forEach(function (a) { a.classList.remove('is-active'); });
    }, { passive: true });
  }

  // Service cards: cursor-following spotlight
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.card').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }
  // Intro overlay: remove after it plays, or on click
  var intro = document.querySelector('.intro');
  if (intro) {
    var endIntro = function () { intro.classList.add('is-done'); };
    intro.addEventListener('animationend', function (e) { if (e.animationName === 'intro-out') endIntro(); });
    intro.addEventListener('click', endIntro);
  }
  var introDelay = root.classList.contains('has-intro') ? 1000 : 0;

  // Pause SMIL animations (card illustration) for reduced motion
  if (reduce) document.querySelectorAll('svg.illo').forEach(function (svg) { if (svg.pauseAnimations) svg.pauseAnimations(); });

  // Mission / Vision: words light up as the section scrolls through
  var statements = Array.prototype.slice.call(document.querySelectorAll('[data-words]'));
  if (statements.length && !reduce) {
    var groups = statements.map(function (el) {
      var words = el.textContent.trim().split(/\s+/);
      el.setAttribute('aria-label', el.textContent.trim());
      el.innerHTML = words.map(function (w) { return '<span class="wd" aria-hidden="true">' + w + '</span>'; }).join(' ');
      el.classList.add('words');
      return Array.prototype.slice.call(el.querySelectorAll('.wd'));
    });
    var ticking = false;
    var lightWords = function () {
      ticking = false;
      var vh = window.innerHeight;
      statements.forEach(function (el, gi) {
        var r = el.getBoundingClientRect();
        // 0 when the text's top reaches 85% of the viewport, 1 when its bottom reaches 45%
        var start = vh * 0.85, end = vh * 0.45;
        var p = (start - r.top) / ((start - end) + r.height);
        p = Math.max(0, Math.min(1, p));
        var lit = Math.round(p * groups[gi].length);
        groups[gi].forEach(function (w, i) { w.classList.toggle('on', i < lit); });
      });
    };
    var requestLight = function () { if (!ticking) { ticking = true; requestAnimationFrame(lightWords); } };
    window.addEventListener('scroll', requestLight, { passive: true });
    window.addEventListener('resize', requestLight);
    lightWords();
  }

  // Hero: particle "i" mark
  var canvas = document.querySelector('.hero-canvas');
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext('2d');
    var hero = document.querySelector('.hero');
    var img = new Image();
    var pts = [], W = 0, H = 0, dpr = 1, dot = 2;
    var mouse = { x: -9999, y: -9999 };
    var running = false, visible = true, started = false, raf = 0, t0 = 0;

    var build = function () {
      var box = canvas.parentNode.getBoundingClientRect();
      W = box.width; H = box.height;
      if (!W || !H) return;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Fit the mark inside the box
      var ar = img.naturalWidth / img.naturalHeight;
      var mh = Math.min(H * 0.92, (W * 0.92) / ar), mw = mh * ar;
      var ox = (W - mw) / 2, oy = (H - mh) / 2;
      var step = Math.max(3, mh * 0.0155);
      dot = Math.max(1.1, step * 0.36);

      var off = document.createElement('canvas');
      off.width = Math.ceil(mw); off.height = Math.ceil(mh);
      var octx = off.getContext('2d');
      octx.drawImage(img, 0, 0, off.width, off.height);
      var data = octx.getImageData(0, 0, off.width, off.height).data;

      var old = pts; pts = [];
      for (var y = step / 2; y < off.height; y += step) {
        for (var x = step / 2; x < off.width; x += step) {
          var a = data[((y | 0) * off.width + (x | 0)) * 4 + 3];
          if (a > 140) {
            var prev = old[pts.length];
            pts.push({
              tx: ox + x, ty: oy + y,
              x: prev ? prev.x : Math.random() * W,
              y: prev ? prev.y : Math.random() * H,
              vx: 0, vy: 0,
              ph: Math.random() * Math.PI * 2,
              s: 0.75 + Math.random() * 0.5
            });
          }
        }
      }
      if (reduce) { pts.forEach(function (p) { p.x = p.tx; p.y = p.ty; }); draw(0); }
    };

    var draw = function (t) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#f2f2f2';
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        ctx.globalAlpha = reduce ? 0.9 : 0.55 + 0.45 * Math.sin(t * 0.0016 + p.ph);
        var d = dot * p.s;
        ctx.fillRect(p.x - d / 2, p.y - d / 2, d, d);
      }
      ctx.globalAlpha = 1;
    };

    var R = 90, R2 = R * R;
    var tick = function (t) {
      if (!running) return;
      var elapsed = t - t0;
      var k = elapsed < 2200 ? 0.012 + 0.03 * (elapsed / 2200) : 0.042;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        var ax = (p.tx - p.x) * k, ay = (p.ty - p.y) * k;
        var dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < R2) {
          var d = Math.sqrt(d2) || 1, f = (1 - d / R) * 4.2;
          ax += (dx / d) * f; ay += (dy / d) * f;
        }
        p.vx = (p.vx + ax) * 0.86; p.vy = (p.vy + ay) * 0.86;
        p.x += p.vx; p.y += p.vy;
      }
      draw(t);
      raf = requestAnimationFrame(tick);
    };

    var setRunning = function () {
      var should = started && visible && !document.hidden && !reduce;
      if (should && !running) { running = true; raf = requestAnimationFrame(function (t) { if (!t0) t0 = t; tick(t); }); }
      if (!should && running) { running = false; cancelAnimationFrame(raf); }
    };

    img.onload = function () {
      build();
      if (reduce) return;
      setTimeout(function () { started = true; setRunning(); }, introDelay + 150);

      var rt;
      window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(build, 150); });
      document.addEventListener('visibilitychange', setRunning);
      if (hasIO) {
        new IntersectionObserver(function (e) { visible = e[0].isIntersecting; setRunning(); }).observe(hero);
      }
      var move = function (e) {
        var r = canvas.getBoundingClientRect();
        mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
      };
      hero.addEventListener('pointermove', move, { passive: true });
      hero.addEventListener('pointerdown', move, { passive: true });
      hero.addEventListener('pointerleave', function () { mouse.x = mouse.y = -9999; });
      hero.addEventListener('pointerup', function (e) { if (e.pointerType !== 'mouse') mouse.x = mouse.y = -9999; });
    };
    img.src = 'assets/img/mark.png';
  }
})();
