
const url = document.getElementById('like_post_url').textContent

const likeajax = new FetchUpdateAjax(url)

function buttonupdate(data, button) {
  if (data.response === "okay") {
    button.innerHTML =
      `${(data.liked) ? 'LIKED!' : 'Like'}  ${data.likes}`
  }
}



document
  .querySelectorAll("[id*='button']")
  .forEach(function (button)  {

    const id = button.id.split('_')[1]

    likeajax.fetch(id, data => buttonupdate(data, button))

    button.onclick = (event) => {
      likeajax.update(id, data => buttonupdate(data, button))
    }
  })

