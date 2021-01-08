

const url = document.getElementById('user_followers_url').textContent
const pk = document.getElementById('follow_user_pk').textContent
const ajax = new Ajax()


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

class State {
  constructor(label, link) {
    this.label = label
    this.link = link
  }
}

const yes = new State('FOLLOWING!', url)
const no = new State('Follow', '#')

/*

const yes = {
  label: 'FOLLOWING!',
  link: url,
}

const no = {
  label: 'Follow',
  link: '#',
}

*/

function buttonupdate(label, link, count) {

  switch (label.innerHTML) {
    case no.label:
      label.innerHTML = yes.label
      link.href = yes.link
      count.innerHTML++
      break
    case yes.label:
      label.innerHTML = no.label
      link.href = no.link
      count.innerHTML--
      break
    default:
      alert('FOLLOW UPDATE ERROR!!')
  }
}

const button = document.getElementById('followers_button')
const link = document.getElementById('followers_link')
const count = document.getElementById('followers_count')
const label = document.getElementById('followers_label')


button.onclick = (event) => {
  ajax.send({request: 'follow', id: pk})
  buttonupdate(label, link, count)
}
