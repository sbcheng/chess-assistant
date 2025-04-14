# chess-assistant
Chess-Assistant is an auxiliary software for automatic chess-playing on the Chess Alliance platform, based on the Stockfish chess AI engine.

This software is built upon another project on GitHub (link: https://github.com/lostlasse/Chess-OpenCV-Cheat). I would like to express my gratitude to lostlasse for their contribution, which has allowed me to "stand on the shoulders of giants."

The functionalities implemented in this software include:

Analyzing chess positions and making decisions.
Fully automated chess-playing, with automatic progression to the next round even after a game concludes.
A certain degree of evasion of anti-cheating mechanisms, such as the ability to adjust parameters so that the software does not aim to win every game.
Points 2 and 3 above are features not present in lostlasse's project.

It is recommended to use Python version 3.7 or above.



#depends on third-party packages
##opencv2
##numpy
##pyautogui
##mss
##screeninfo
##stockfish

#how to use
1.Install Stockfish
2.Change the stockfish path in the config.json. You have to replace \ with \\.
3.Replace the pictures of the figures in the black and white folders. For the best results, you should try to capture all of the figures against the same background color.
4. Run the executable
5. Use the X, Y and the Offset sliders to math the grid
6. If your figures are black, change the W->B to B for black
7. Position the Off->On slider to On to disable the positioning
8. Position the calc slider to On to calculate the next best move
If you run into an Error first check if all figures are detected.
If not then you could try to change the confidence value.


#GUI Instructions
X-Coord : X-coordinate of the captured area
: Y-coordinate of the captured area
: X offset of the captured area
: Y offset of the captured area
: The accuracy of character recognition
: Choose your color (W for white, B for black)
: Turn off auto move. If activated, the script automatically moves the figures. But you still have to press calc.
: Switching on deactivates the transformation mode
: Turn on to calculate the next move. Note: The slider is reset to Off after each successful calculation or after an error.Y-CoordX-OffsetY-OffsetConfidenceW->Bauto-moveOff->Oncalc
