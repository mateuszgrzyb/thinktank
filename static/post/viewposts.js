

const likeajax = new Ajax()
const yes = 'LIKED!'
const no = 'Like'

function buttonupdate(liked, count) {
  switch (liked.innerHTML) {
    case no:
      liked.innerHTML = yes
      count.innerHTML++
      break
    case yes:
      liked.innerHTML = no
      count.innerHTML--
      break
    default:
      alert('LIKE UPDATE ERROR!!')
  }
}



document
  .querySelectorAll("[id*='button']")
  .forEach(function (button)  {

    const pk = button.id.split('_')[1]
    const liked = button.children[0]
    const count = button.children[1]

    button.onclick = (event) => {
      likeajax.send('like',pk)
      buttonupdate(liked, count)
    }
  })

