

const url = document.getElementById('follow_user_url').textContent
const user_followers_url = document.getElementById('user_followers_url').textContent
const pk = document.getElementById('follow_user_pk').textContent
const followajax = new FetchUpdateAjax(url)


/*
 *
 *
 *
 * Very bad, I know.
 * I will take care of this sometime in the future.
 * Probably no bugs here.
 * Probably...
 *
 *
 *
 */

function buttonupdate(data, button, link, count) {
  if (data.response === "okay") {
    if (data.following) {
      button.innerHTML = 'FOLLOWING!'
      //count.innerHTML = (count.innerHTML + 1)
      count.innerHTML++
      if (count.innerHTML != 0) {
        link.href = user_followers_url
      }
    } else {
      button.innerHTML = 'Follow'
      count.innerHTML--
      if (count.innerHTML == 0) {
        link.href = "#"
      }
      //count.innerHTML = (count.innerHTML - 1)
    }
  }
}

function buttonfetch(data, button) {
  if (data.response === "okay") {
    if (data.following) {
      button.innerHTML = 'FOLLOWING!'
    } else {
      button.innerHTML = 'Follow'
    }
  }
}

const button = document.getElementById('follow')
const link = document.getElementById('followers_link')
const count = document.getElementById('followers_count')

followajax.fetch(pk, data => buttonfetch(data, button))

button.onclick = (event) =>  {
  followajax.update(pk, data => buttonupdate(data, button, link, count))
}
