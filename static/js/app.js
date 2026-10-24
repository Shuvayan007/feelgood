/* ============================================================
   Feel Good — Frontend JavaScript
   ============================================================ */

(function () {
  'use strict';

  // ── CSRF helper ─────────────────────────────────────────────
  function getCookie(name) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var c = cookies[i].trim();
      if (c.startsWith(name + '=')) {
        return decodeURIComponent(c.substring(name.length + 1));
      }
    }
    return null;
  }

  var csrfToken = getCookie('csrftoken');

  function apiHeaders() {
    return {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken || '',
    };
  }

  // ── Mobile sidebar toggle ───────────────────────────────────
  var hamburger = document.getElementById('hamburger');
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebar-overlay');

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
  }

  if (hamburger) {
    hamburger.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('open');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }

  // ── Alert auto-dismiss ──────────────────────────────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    var btn = alert.querySelector('.dismiss');
    if (btn) {
      btn.addEventListener('click', function () {
        alert.remove();
      });
    }
    setTimeout(function () {
      if (alert.parentNode) {
        alert.style.transition = 'opacity 0.3s';
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 300);
      }
    }, 5000);
  });

  // ── Chat form submission ────────────────────────────────────
  var chatForm = document.getElementById('chat-form');
  var chatMessages = document.getElementById('chat-messages');
  var chatInput = document.getElementById('chat-input');
  var conversationId = null;

  // Grab conversation id from the page if set
  var convIdEl = document.getElementById('conversation-id');
  if (convIdEl) {
    conversationId = convIdEl.value || null;
  }

  function appendMessage(role, content) {
    if (!chatMessages) return;
    var div = document.createElement('div');
    div.className = 'msg ' + (role === 'user' ? 'msg-user' : 'msg-assistant');
    div.textContent = content;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  if (chatForm) {
    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = chatInput.value.trim();
      if (!text) return;

      appendMessage('user', text);
      chatInput.value = '';

      var body = { content: text };
      if (conversationId) {
        body.conversation_id = conversationId;
      }

      fetch('/api/mentor/chat/', {
        method: 'POST',
        headers: apiHeaders(),
        body: JSON.stringify(body),
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.conversation_id) {
            conversationId = data.conversation_id;
          }
          appendMessage('assistant', data.content || data.message || 'I received your message.');
        })
        .catch(function () {
          appendMessage('assistant', 'Something went wrong. Please try again.');
        });
    });
  }

  // Scroll chat to bottom on load
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // ── Habit log toggle ────────────────────────────────────────
  document.querySelectorAll('[data-habit-log]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var habitId = btn.getAttribute('data-habit-log');
      btn.disabled = true;
      btn.textContent = 'Logging...';

      fetch('/api/habits/' + habitId + '/log/', {
        method: 'POST',
        headers: apiHeaders(),
        body: JSON.stringify({ count: 1 }),
      })
        .then(function (res) { return res.json(); })
        .then(function () {
          btn.textContent = 'Logged';
          btn.classList.remove('btn-primary');
          btn.classList.add('btn-secondary');
        })
        .catch(function () {
          btn.disabled = false;
          btn.textContent = 'Log';
        });
    });
  });

  // ── Dark mode toggle ────────────────────────────────────────
  var themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    var currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
      document.documentElement.style.colorScheme = 'dark';
    }

    themeToggle.addEventListener('click', function () {
      var isDark = localStorage.getItem('theme') === 'dark';
      if (isDark) {
        localStorage.removeItem('theme');
        document.documentElement.style.colorScheme = '';
      } else {
        localStorage.setItem('theme', 'dark');
        document.documentElement.style.colorScheme = 'dark';
      }
    });
  }
})();
