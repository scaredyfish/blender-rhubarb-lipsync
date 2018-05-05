# Blender Rhubarb Lip Sync

Blender Rhubarb Lipsync is an addon for [Blender](http://blender.org) integrating [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) to automatically generate mouth-shape keyframes from a pose library.

Rhubarb Lip Sync is a command-line tool that automatically creates 2D mouth animation from voice recordings. You can use it for characters in computer games, in animated cartoons, or in any other project that requires animating mouths based on existing recordings.

## Example output

[![Example video](http://img.youtube.com/vi/azrpByrvw-o/0.jpg)](http://www.youtube.com/watch?v=azrpByrvw-o)

http://www.youtube.com/watch?v=azrpByrvw-o

## Usage

First, set the path to the Rhubarb Lipsync executable in user preferences (download from [https://github.com/DanielSWolf/rhubarb-lip-sync](https://github.com/DanielSWolf/rhubarb-lip-sync))

![Preferences](img/prefs.PNG)

Create a [pose library](https://docs.blender.org/manual/en/dev/rigging/armatures/properties/pose_library.html) with the mouth shapes described in the Rhubarb Lip Sync documentation. You can name your poses whatever you like.

![Pose library](img/poselib.PNG)

Match your poses with the Rhubarb Lip Sync names.
Select your sound file, and dialog file (optional), and the start frame where your sound begins.

![Options panel](img/panel.PNG)

Click the Rhubarb Lip Sync button and wait for the process to complete. There is no progress indicator yet, but your keyframes will appear when the process is complete.