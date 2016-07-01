How to play:
Endless Breakout is like regular Breakout, but with a few simple twists.
Instead of destroying bricks, the objective of the game is to survive as long as possible.
The longer you survive, the more points you’ll score. New balls spawn every 10 seconds.
Let any ball go out of bounds and it is game over. Using the mouse, your paddle is able to move
anywhere on the screen, not just the bottom. In addition, your paddle comes equipped with two
special abilities: Left click increases your score faster, but also increases the speed of
the balls. Right click slows the balls down, but also consumes energy. Use your abilities wisely!


Planned future updates:
 -Targets to aim for
 -Better graphics
 -Sound and music
 -Menus
 -Customizable controls
 -Save highscore between play sessions
 -Gameplay tweaks and balances
 -Possibly another physics overhaul


Changelog:

6/30/2016:

Version 0.3.1:
-Made ball and paddle a bit smaller
-Balls are slightly slower now
-Ball and paddle collision code adjusted slightly

Version 0.3:
-Physics overhaul:
  New balls now gradually accelerate to full speed
  Balls can move in a wide range of angles
  New balls have a random starting angle between 20 and 70 degrees
  Ball's angle changes based on what part of the paddle it hits
-ALT + F4 now closes the game.
  

3/23/2016:

Version 0.2.3:
-Text is now prerendered before the game starts
-Added more debugging info

3/15/2016:

Version 0.2.1:
-First public release
-Added some randomness to the ball spawns

3/14/2016:

Version 0.2:
-New game mechanics:
  Left click scores you double the points, but also speeds balls up
  Right click slows balls down, but also consumes energy
  Energy is displayed on the statsSurface
-Game window is now widescreen.
-Rewrote text drawing code to consume fewer system resources
-Time is now displayed in m:s.ms format
-New DEBUGMODE command:
  'x': Spawns 100 balls.
-Misc small fixes

3/12/2016:

Version 0.1:
-Game window now consists of two surfaces: playfield and statsSurface
-statsSurface shows the following stats:
  highscore
  score
  number of balls in play
  time survived
-Improved DEBUGMODE. When DEBUGMODE is on, it enables the following
 commands:
  'g': Enables godMode. Prevents balls from going out of bounds and freezes
  score value at 0.
  'b': Spawns a new ball.
 DEBUGMODE also displays the following variables on the statsSurface:
  FPS
  current frame
  godMode
  mouse position
-Improved game over screen.
-Mouse can no longer leave the game window while the game loop is running

Version 0.02:
-Added DEBUGMODE.
-Paddle can now move anywhere on the screen.

3/11/2016:

Version 0.01:
-First stable build. New balls spawn every 10 seconds. Game ends when a ball
 goes out of bounds.


Gameplay observations:
-I'm usually unable to see my energy meter while playing, because my eyes are on the playfield. I'm going to draw an energy bar onto the paddle to see if that helps. Another game called Alphabounce actually has a similar feature to this for certain power-ups.
-To my surprise, the v0.3 physics overhaul actually makes it harder to keep the balls in play. I think this is because the ball
movement was more predictable before. Also, it is hard to control what part of the paddle a ball hits when you have several or more balls to keep track of. I've lowered the speed slightly in v0.3.1 to compensate.