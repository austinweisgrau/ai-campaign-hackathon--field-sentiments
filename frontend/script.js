function getSpeechRecognition() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.continuous = true;
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.onresult = (event) => {
    content.value = event.results[0][0].transcript;
    const status = confirm("Look correct?\n\n" + content.value);
    if (status) {
      window.fetch('/api/receive_memo', {
        type: 'POST',
        data: {
          geo_lat: 100,
          geo_lng: 100,
          memo: content.value
        },
      });
    }
    content.value = '';
  };
  return recognition;
}

const button = document.getElementById('record');
const content = document.getElementById("content");
const bg = document.querySelector("html");

(() => {
  let live = null;
  document.getElementById('record').addEventListener('click', () => {
    debugger;
    if (live) {
      live.stop();
      live = null;
      button.classList.remove('recording');
    }
    else {
      live = getSpeechRecognition()
      live.start();
      button.classList.add('recording');
    }
  });
})();
