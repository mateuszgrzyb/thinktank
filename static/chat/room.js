

const chattext = document.querySelector('#chattext')
const chatlog = document.querySelector('#chatlog')
const chatsend = document.querySelector('#chatsend')

const name = JSON.parse(document.getElementById('room-name').textContent)
const user = JSON.parse(document.getElementById('user-name').textContent)
const isAnon = JSON.parse(document.getElementById('is-anon').textContent)

const s = new WebSocket(
  `ws://${window.location.host}/ws/${isAnon}chat/${name}/`
)

s.onmessage = event => {
  const data = JSON.parse(event.data)
  chatlog.innerHTML +=
    `<li>${data.from}: ${data.msg}</li>`
}

function sendmsg() {
  const msg = chattext.value
  if (msg) {
    s.send(JSON.stringify({
      'from': user,
      'msg': msg
    }))
    chattext.value = ''
  }
}

chatsend.onclick = event => {
  sendmsg()
}

chattext.onkeyup = event => {
  if (event.key === 'Enter') {
    sendmsg()
  }
}


s.onclose = event => {
  alert('socket closed for some reason')
}
