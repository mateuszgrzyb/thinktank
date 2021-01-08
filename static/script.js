class Ajax {
  constructor() {
    const csrfdom = document.querySelector('[name=csrfmiddlewaretoken]')
    if (csrfdom) {
      const csrftoken = csrfdom.value
      const url = document.getElementById('ajax_url').textContent
      this.request = new Request(
        url,
        {
          headers: {'X-CSRFToken': csrftoken},
          method: 'POST',
          mode: 'same-origin',
        }
      )
    } else {
      alert('TRYING TO USE AJAX WITH POST METHOD WITHOUT CSRF TOKEN!!!')
    }
  }


  send(data) {
    fetch(this.request, {body: JSON.stringify(data)})
  }
}

