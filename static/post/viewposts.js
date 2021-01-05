
const url = document.getElementById('like_post_url').textContent
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const request = new Request(
  url,
  {headers: {'X-CSRFToken': csrftoken}},
)

function ajax(data, button) {


  fetch(request, {
    method: 'POST',
    body: JSON.stringify(data),
    mode: 'same-origin'
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      if (data.response === "okay") {
        console.log(data.likes)
        console.log(data.user)
        button.innerHTML =
          `${(data.user) ? 'LIKED!' : 'Like'}  ${data.likes}`
      }
    })
}

document
  .querySelectorAll("[id*='button']")
  .forEach(function (button)  {
    const id = button.id.split('_')[1]
    console.log(id)
    ajax({type: 'fetch', like: id}, button)
    console.log('okay')

    button.onclick = event => {
      ajax({type: 'update', like: id}, button)
    }
  })

