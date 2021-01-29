
class Ajax {
  constructor() {
    const csrfdom = document.querySelector('[name=csrfmiddlewaretoken]')
    if (csrfdom) {
      this.request = new Request(
        document.getElementById('ajax_url').textContent,
        {
          headers: {'X-CSRFToken': csrfdom.value},
          method: 'POST',
          mode: 'same-origin',
        }
      )
    } else {
      alert('TRYING TO USE AJAX WITH POST METHOD WITHOUT CSRF TOKEN!!!')
    }
  }


  send(request, pk) {
    fetch(this.request, {body: JSON.stringify({request: request, pk: pk})})}
}

