QUYEN 4/16/2020

<b>This is the UI "prototype":</b>
![Basic Interface](/screenshots/app1.png)
Everything is in button format bc I figure it is easier to control things by selecting/deselecting button than hard-coding and operating slider in pygame.

<b>How image look on this new UI:</b>
![in action](/screenshots/app2.png)

<b>Glasses on top:</b>
![glassed](/screenshots/app3.png)

* What I got so far
  * Buttons changed color to indicate the state of being selected
  * The choice of some buttons "automatically" disable some other button

* What's missing
  * Starburst and halo
  * Button deselect: my plan is to deselect a selected button with right click mouse (in contrast to left click to select). This should be easy with `pygame.mouse.get_selected()`, but for some reasons I got `get_selected() can't be found`, which shouldn't be a problem with my pygame version (1.9.6)
  * Key press to control values: my plan is to check whether myopia or hyperopia is selected, then use UP and DOWN arrow key to change values, and have pop-up window displayed the current value after change
  
* Problems
  * Program shuts down if we close the file window not choosing any file
  * Many images are too large to be seen entirely on screen (new screen and old total window), resize image may compromise the quality
  * Upload a new image cause it to sit on top of the old one. Should be reset every time an image is uploaded



https://crypto-resolver-265608.appspot.com/
