const button = document.getElementById('report');
const content = document.getElementById("content");

function getReport() {
  const httpRequest = new XMLHttpRequest();
  const url = '/get_report';

  httpRequest.onreadystatechange = function() {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
        const response = httpRequest.responseText;
        document.getElementById('content').textContent = response;
      } else {
        console.error('There was a problem with the request.');
      }
    }
  };

  httpRequest.open('GET', url);
  httpRequest.send();
}

(() => {
    document.getElementById('report').addEventListener('click', getReport)
})();
