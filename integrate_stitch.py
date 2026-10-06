import os
import shutil
import zipfile

zip_path = r"C:\Users\spect\Downloads\stitch_jarvis_holographic_ai_hud.zip"
dest_templates = r"C:\Users\spect\JARVIS\templates"
dest_static = r"C:\Users\spect\JARVIS\static"
index_path = os.path.join(dest_templates, "index.html")
backup_path = os.path.join(dest_templates, "index_backup.html")

if not os.path.exists(zip_path):
    print("Stitch zip not found at:", zip_path)
    exit(1)

# Backup existing index.html
if os.path.exists(index_path) and not os.path.exists(backup_path):
    shutil.copyfile(index_path, backup_path)
    print("Backed up existing index.html to index_backup.html")

# Extract zip contents
with zipfile.ZipFile(zip_path, "r") as z:
    z.extract("screen.png", dest_static)
    z.extract("DESIGN.md", r"C:\Users\spect\JARVIS")
    raw_html = z.read("code.html").decode("utf-8", errors="ignore")

real_script = """
    // J.A.R.V.I.S. Live Core Integration
    function dismissWelcomeModal() {
      const modal = document.getElementById('welcome-modal');
      if (modal) {
        modal.style.opacity = '0';
        modal.style.transform = 'translateY(-10px)';
        setTimeout(() => { modal.style.display = 'none'; }, 400);
      }
    }

    function insertPrompt(text) {
      const input = document.getElementById('directive-input');
      if (input) {
        input.value = text;
        input.focus();
      }
    }

    function escapeHtml(str) {
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function appendUserMessage(msg) {
      const chatFeed = document.getElementById('agent-chat-feed');
      if (!chatFeed) return;
      const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      const userCard = document.createElement('div');
      userCard.className = 'flex items-start justify-end gap-3 transition-all animate-fade-in';
      userCard.innerHTML = `
        <div class="flex flex-col items-end max-w-[85%]">
          <div class="flex items-center gap-2 mb-1 font-label-sm text-label-sm">
            <span class="text-outline text-[10px]">${now}</span>
            <span class="text-secondary font-semibold tracking-wider">SIR // A. STARK</span>
          </div>
          <div class="p-3.5 rounded-2xl rounded-tr-sm bg-gradient-to-r from-secondary-container/20 to-secondary/20 border border-secondary/40 text-on-surface shadow-md">
            <p class="font-body-md text-body-md leading-relaxed">${escapeHtml(msg)}</p>
          </div>
        </div>
        <div class="w-8 h-8 rounded-full bg-secondary/20 border border-secondary/50 flex items-center justify-center flex-shrink-0 text-secondary shadow-[0_0_8px_rgba(255,185,95,0.4)]">
          <span class="material-symbols-outlined text-[17px]">person</span>
        </div>
      `;
      chatFeed.appendChild(userCard);
      chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    function appendJarvisResponse(responseMsg) {
      const chatFeed = document.getElementById('agent-chat-feed');
      if (!chatFeed) return;
      const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      let formatted = escapeHtml(responseMsg)
        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
        .replace(/```([\\s\\S]*?)```/g, '<pre class="bg-black/60 p-2 rounded border border-primary/20 text-xs font-mono my-2 overflow-x-auto text-primary"><code>$1</code></pre>')
        .replace(/`([^`]+)`/g, '<code class="bg-black/40 px-1 py-0.5 rounded text-primary text-xs font-mono">$1</code>')
        .replace(/\\n/g, '<br>');

      const jarvisCard = document.createElement('div');
      jarvisCard.className = 'flex items-start gap-3 transition-all animate-fade-in';
      jarvisCard.innerHTML = `
        <div class="w-8 h-8 rounded-full bg-primary-container/20 border border-primary-container/40 flex items-center justify-center flex-shrink-0 text-primary-container shadow-[0_0_8px_rgba(0,240,255,0.4)]">
          <span class="material-symbols-outlined text-[17px]">smart_toy</span>
        </div>
        <div class="flex flex-col max-w-[85%]">
          <div class="flex items-center gap-2 mb-1 font-label-sm text-label-sm">
            <span class="text-primary-container font-semibold tracking-wider">J.A.R.V.I.S.</span>
            <span class="text-outline text-[10px]">${now}</span>
          </div>
          <div class="p-3.5 rounded-2xl rounded-tl-sm bg-surface-container-high/70 border border-primary-container/20 text-on-surface shadow-md">
            <div class="font-body-md text-body-md leading-relaxed">${formatted}</div>
          </div>
        </div>
      `;
      chatFeed.appendChild(jarvisCard);
      chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    function appendJarvisThinking(id) {
      const chatFeed = document.getElementById('agent-chat-feed');
      if (!chatFeed) return;
      const card = document.createElement('div');
      card.id = id;
      card.className = 'flex items-start gap-3 transition-all';
      card.innerHTML = `
        <div class="w-8 h-8 rounded-full bg-primary-container/20 border border-primary-container/40 flex items-center justify-center flex-shrink-0 text-primary-container animate-pulse">
          <span class="material-symbols-outlined text-[17px]">smart_toy</span>
        </div>
        <div class="flex flex-col max-w-[85%]">
          <div class="p-3 rounded-2xl rounded-tl-sm bg-surface-container-high/40 border border-primary-container/20 text-primary-container text-xs flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-primary-container animate-ping"></span>
            <span>J.A.R.V.I.S. is processing neural directives with Gemini 3.6...</span>
          </div>
        </div>
      `;
      chatFeed.appendChild(card);
      chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    function removeJarvisThinking(id) {
      const el = document.getElementById(id);
      if (el) el.remove();
    }

    // Live Text-To-Speech (J.A.R.V.I.S. Voice)
    function speakJARVIS(text) {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const clean = text
        .replace(/```[\\s\\S]*?```/g, 'Code block output omitted.')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/[*_#~]/g, '')
        .trim();
      if (!clean) return;

      const u = new SpeechSynthesisUtterance(clean);
      const voices = window.speechSynthesis.getVoices();
      const ukVoice = voices.find(v => v.lang === 'en-GB' || v.name.toLowerCase().includes('british') || v.name.toLowerCase().includes('daniel') || v.name.toLowerCase().includes('george'));
      if (ukVoice) u.voice = ukVoice;
      u.pitch = 0.95;
      u.rate = 1.0;
      window.speechSynthesis.speak(u);
    }

    async function executeCommand(customPrompt) {
      const input = document.getElementById('directive-input');
      const cmd = customPrompt || (input ? input.value.trim() : '');
      if (!cmd) return;

      appendUserMessage(cmd);
      if (input && !customPrompt) {
        input.value = '';
      }

      const thinkingId = 'thinking-' + Date.now();
      appendJarvisThinking(thinkingId);

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: cmd, session_id: 'stark_session' })
        });
        const data = await res.json();
        removeJarvisThinking(thinkingId);

        if (data.success) {
          appendJarvisResponse(data.response);
          speakJARVIS(data.response);
        } else {
          appendJarvisResponse('[System Alert]: ' + (data.error || 'Directive processing error.'));
        }
      } catch (err) {
        removeJarvisThinking(thinkingId);
        appendJarvisResponse('[Connection Fault]: Stark neural link unreachable. ' + err.message);
      }
    }

    function triggerDirective(action) {
      const directives = {
        'DIAGNOSTICS': 'Jarvis, run a full system diagnostics check on the Mark LXXXV armor and quantum grid.',
        'NANO_SHIELD': 'Deploy nano-barrier kinetic shielding and report integrity.',
        'REROUTE_POWER': 'Reroute auxiliary power to the primary arc reactor core.',
        'LOCKDOWN': 'Initiate Omega lockdown defensive perimeter immediately.'
      };
      executeCommand(directives[action] || `Execute ${action} directive.`);
    }

    // Real Speech-To-Text (Microphone)
    let isListening = false;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        isListening = true;
        updateMicUI(true);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('directive-input');
        if (input) input.value = transcript;
        executeCommand();
      };

      recognition.onerror = () => {
        isListening = false;
        updateMicUI(false);
      };

      recognition.onend = () => {
        isListening = false;
        updateMicUI(false);
      };
    }

    function toggleVoiceListen() {
      if (!SpeechRecognition) {
        alert('Vocal directives require Google Chrome or Microsoft Edge with Web Speech API support.');
        return;
      }
      if (isListening) {
        recognition.stop();
      } else {
        try {
          recognition.start();
        } catch (e) {
          console.error(e);
        }
      }
    }

    function updateMicUI(listening) {
      const micIcon = document.getElementById('mic-icon');
      const input = document.getElementById('directive-input');
      if (micIcon) {
        micIcon.innerText = listening ? 'record_voice_over' : 'mic';
      }
      if (input) {
        input.placeholder = listening ? 'Listening to vocal directive... Speak now, Sir.' : 'Speak or type command, Sir... ("JARVIS, calibrate targeting systems")';
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      const input = document.getElementById('directive-input');
      if (input) {
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            executeCommand();
          }
        });
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
      }
    });
"""

# Replace the last <script>...</script> block in raw_html
last_script_pos = raw_html.rfind("<script>")
if last_script_pos != -1:
    end_script_pos = raw_html.find("</script>", last_script_pos)
    final_html = raw_html[:last_script_pos] + "<script>" + real_script + raw_html[end_script_pos:]
else:
    final_html = raw_html.replace("</body>", f"<script>{real_script}</script></body>")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("SUCCESS: Stitch UI integrated into templates/index.html with live Gemini backend!")
