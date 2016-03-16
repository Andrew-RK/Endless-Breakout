Changelog:

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

-Improved DEBUGMODE. When DEBUGMODE is on, it enables the following commands:

  'g': Enables godMode. Prevents balls from going out of bounds and freezes score value at 0.

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

-First stable build. New balls spawn every 10 seconds. Game ends when a ball goes out of bounds.
