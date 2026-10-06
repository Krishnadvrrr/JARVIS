// J.A.R.V.I.S. Core Frontend Logic
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatFeed = document.getElementById('chatFeed');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const micBtn = document.getElementById('micBtn');
    const visualizer = document.getElementById('visualizer');
    const reactorStatus = document.getElementById('reactorStatus');
    const speechToggleBtn = document.getElementById('speechToggleBtn');
    const speechIcon = document.getElementById('speechIcon');
    const speechToggleText = document.getElementById('speechToggleText');
    const voiceSelect = document.getElementById('voiceSelect');
    const resetSessionBtn = document.getElementById('resetSessionBtn');
    const systemTime = document.getElementById('system-time');
    const modelName = document.getElementById('model-name');
    const promptChips = document.querySelectorAll('.chip-btn');

    const sessionId = 'jarvis_session_' + Math.random().toString(36).substring(2, 9);
    let speechEnabled = true;
    let selectedVoice = null;
    let isListening = false;
    let recognition = null;

    // 1. System Clock
    function updateClock() {
        const now = new Date();
        systemTime.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }
    setInterval(updateClock, 1000);
    updateClock();

    // 2. Fetch System Diagnostics
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            if (data.model) {
                modelName.textContent = data.model.toUpperCase();
            }
        })
        .catch(err => console.error('Status check failed:', err));

    // 3. Setup Text-to-Speech (JARVIS Voice)
    function populateVoices() {
        if (!('speechSynthesis' in window)) {
            console.warn('Speech synthesis not supported.');
            return;
        }

        const voices = window.speechSynthesis.getVoices();
        voiceSelect.innerHTML = '';

        let ukVoice = null;

        voices.forEach((v, idx) => {
            const option = document.createElement('option');
            option.value = idx;
            option.textContent = `${v.name} (${v.lang})`;

            // Prefer English UK or deep male voices reminiscent of Paul Bettany
            if (!ukVoice && (v.lang === 'en-GB' || v.name.toLowerCase().includes('british') || v.name.toLowerCase().includes('daniel') || v.name.toLowerCase().includes('george'))) {
                ukVoice = v;
                option.selected = true;
            } else if (!ukVoice && v.lang.startsWith('en')) {
                ukVoice = v;
                option.selected = true;
            }

            voiceSelect.appendChild(option);
        });

        if (ukVoice) {
            selectedVoice = ukVoice;
        } else if (voices.length > 0) {
            selectedVoice = voices[0];
        }
    }

    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = populateVoices;
        populateVoices();
    }

    voiceSelect.addEventListener('change', () => {
        const voices = window.speechSynthesis.getVoices();
        const idx = voiceSelect.value;
        if (voices[idx]) {
            selectedVoice = voices[idx];
        }
    });

    // Toggle Speech Audio
    speechToggleBtn.addEventListener('click', () => {
        speechEnabled = !speechEnabled;
        if (speechEnabled) {
            speechToggleBtn.classList.add('active');
            speechIcon.className = 'fa-solid fa-volume-high';
            speechToggleText.textContent = 'Audio: ON';
        } else {
            speechToggleBtn.classList.remove('active');
            speechIcon.className = 'fa-solid fa-volume-xmark';
            speechToggleText.textContent = 'Audio: OFF';
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                visualizer.classList.remove('active');
                reactorStatus.textContent = 'STANDBY // READY FOR DIRECTIVE';
            }
        }
    });

    // Speak text through speech synthesis
    function speakJARVIS(text) {
        if (!speechEnabled || !('speechSynthesis' in window)) return;

        window.speechSynthesis.cancel(); // cancel any active speech

        // Strip markdown symbols and ensure Jarvis is pronounced smoothly as a word
        const cleanText = text
            .replace(/```[\s\S]*?```/g, 'Code block output omitted.')
            .replace(/`([^`]+)`/g, '$1')
            .replace(/[*_#~]/g, '')
            .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1')
            .replace(/\bJ\.?A\.?R\.?V\.?I\.?S\.?\b/gi, 'Jarvis')
            .replace(/J\.A\.R\.V\.I\.S\./g, 'Jarvis')
            .replace(/J-A-R-V-I-S/gi, 'Jarvis')
            .trim();

        if (!cleanText) return;

        const utterance = new SpeechSynthesisUtterance(cleanText);
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }
        utterance.rate = 1.0;
        utterance.pitch = 0.95; // Slightly lower pitch for dignified tone

        utterance.onstart = () => {
            visualizer.classList.add('active');
            reactorStatus.textContent = 'TRANSMITTING AUDIO DIRECTIVE...';
        };

        utterance.onend = () => {
            visualizer.classList.remove('active');
            reactorStatus.textContent = 'STANDBY // READY FOR DIRECTIVE';
        };

        utterance.onerror = () => {
            visualizer.classList.remove('active');
            reactorStatus.textContent = 'STANDBY // READY FOR DIRECTIVE';
        };

        window.speechSynthesis.speak(utterance);
    }

    // 4. Setup Speech Recognition (Speech-to-Text)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
            visualizer.classList.add('active');
            reactorStatus.textContent = 'LISTENING FOR AUDIO DIRECTIVE...';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            stopListening();
        };

        recognition.onend = () => {
            stopListening();
        };

        micBtn.addEventListener('click', () => {
            if (isListening) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (err) {
                    console.error('Recognition start failed:', err);
                }
            }
        });
    } else {
        micBtn.title = 'Speech Recognition not supported in this browser (use Chrome/Edge)';
        micBtn.style.opacity = '0.5';
        micBtn.addEventListener('click', () => {
            alert('Voice recognition requires a browser with Web Speech API support like Google Chrome or Microsoft Edge.');
        });
    }

    function stopListening() {
        isListening = false;
        micBtn.classList.remove('listening');
        visualizer.classList.remove('active');
        reactorStatus.textContent = 'STANDBY // READY FOR DIRECTIVE';
    }

    // 5. Chat Messaging Logic
    function appendMessage(sender, text, timestamp = null) {
        const timeStr = timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const isJarvis = sender === 'JARVIS';

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isJarvis ? 'jarvis-message' : 'user-message'}`;

        const avatarIcon = isJarvis ? '<i class="fa-solid fa-atom"></i>' : '<i class="fa-solid fa-user"></i>';
        const senderName = isJarvis ? 'J.A.R.V.I.S.' : 'YOU';

        // Simple markdown parsing for bold and code
        let formattedText = escapeHTML(text)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');

        msgDiv.innerHTML = `
            <div class="avatar">${avatarIcon}</div>
            <div class="msg-bubble">
                <div class="msg-sender">${senderName}</div>
                <div class="msg-text">${formattedText}</div>
                <div class="msg-time">${timeStr}</div>
            </div>
        `;

        chatFeed.appendChild(msgDiv);
        chatFeed.scrollTop = chatFeed.scrollHeight;
        return msgDiv;
    }

    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Display user message
        appendMessage('USER', text);
        userInput.value = '';
        userInput.style.height = 'auto';

        // Show thinking indicator
        reactorStatus.textContent = 'PROCESSING NEURAL QUERY...';
        visualizer.classList.add('active');

        const thinkingMsg = appendMessage('JARVIS', 'Thinking...');
        const textContainer = thinkingMsg.querySelector('.msg-text');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    session_id: sessionId
                })
            });

            const data = await response.json();

            if (data.success) {
                let formatted = escapeHTML(data.response)
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.*?)\*/g, '<em>$1</em>')
                    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
                    .replace(/`([^`]+)`/g, '<code>$1</code>')
                    .replace(/\n/g, '<br>');

                textContainer.innerHTML = formatted;
                if (data.timestamp) {
                    thinkingMsg.querySelector('.msg-time').textContent = data.timestamp;
                }

                // Speak response
                speakJARVIS(data.response);
            } else {
                textContainer.innerHTML = `<span style="color: #ff5555;">[Alert]: ${escapeHTML(data.error || 'Unknown system fault.')}</span>`;
                reactorStatus.textContent = 'FAULT DETECTED // STANDBY';
                visualizer.classList.remove('active');
            }
        } catch (err) {
            textContainer.innerHTML = `<span style="color: #ff5555;">[Connection Failure]: ${escapeHTML(err.message)}</span>`;
            reactorStatus.textContent = 'OFFLINE FAULT // STANDBY';
            visualizer.classList.remove('active');
        }

        if (!speechEnabled) {
            reactorStatus.textContent = 'STANDBY // READY FOR DIRECTIVE';
            visualizer.classList.remove('active');
        }
    }

    // Event Listeners for input
    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-expand textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
    });

    // Quick directives chips
    promptChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const directive = chip.getAttribute('data-msg');
            userInput.value = directive;
            sendMessage();
        });
    });

    // Reset session
    resetSessionBtn.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId })
            });
            const data = await res.json();
            
            chatFeed.innerHTML = '';
            appendMessage('JARVIS', 'Memory cache cleared, sir. All neural registers have been purged. How may I assist you anew?');
            speakJARVIS('Memory cache cleared, sir. How may I assist you anew?');
        } catch (err) {
            console.error('Reset failed:', err);
        }
    });
});
