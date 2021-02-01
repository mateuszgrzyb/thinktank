#### What is Thinktank?


It's a social media service made in 
[Django][django] 
web framework.


You can create posts, follow other users
to see what they want to say and chat with them 
in group and private chats.


Chat functionality was made with 
[Django Channels][channels] 
and websockets.

---

#### TODO:


* Finish profile settings
    * Email verification
    * Combining profile settings and password pages
* Code cleanup
* UI
    * Finish/clean up some pages
    * Horizontal scaling is not working
        * Most pages looks great on only half of screen
        * I want it to look great on both half and fullscreen
        * In case of problems fullscreen is the priority

---

<sub>by [Mateusz Grzyb][github]<sub>

[django]: https://www.djangoproject.com/
[channels]: https://channels.readthedocs.io/en/stable/
[github]: https://www.github.com/mateuszgrzyb "Link to my github page"