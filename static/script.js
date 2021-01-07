class Ajax {
  constructor(url) {
    try {
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
      this.request = new Request(
        url,
        {headers: {'X-CSRFToken': csrftoken}}
      )
    } catch (e) {
      if (e instanceof TypeError) {
        alert('TRYING TO USE AJAX WITH POST METHOD WITHOUT CSRF TOKEN!!!')
      } else {
        throw e;
      }
    }
  }

  send(data, onmessage) {
    fetch(
      this.request,
      {
        method: 'POST',
        body: JSON.stringify(data),
        mode: 'same-origin'
      })
      .then(response => response.json())
      .then(data => { console.log(data); return data})
      .then(data => onmessage(data))
  }

  /*
  fetch(pk, onmessage) {
    this.send({type: 'fetch', pk: pk}, onmessage)
  }

  update(pk, onmessage) {
    this.send({type: 'update', pk: pk}, onmessage)
  }

   */
}

class FetchUpdateAjax extends Ajax {
  fetch(pk, onmessage) {
    this.send({type: 'fetch', pk: pk}, onmessage)
  }


  update(pk, onmessage) {
    this.send({type: 'update', pk: pk}, onmessage)
  }
}

class AutomaticAjax {
  constructor(url) {
    this.xhttp = new XMLHttpRequest()
    this.xhttp.onreadystatechange = () => {
      if (this.xhttp.readyState == 4 && this.xhttp.status == 200) {
        alert(this.xhttp.responseText)
      }
    }
    this.xhttp.open('POST', url, true)
  }
}