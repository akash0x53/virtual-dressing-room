Virtual Dressing Room
===

Example of how to use OpenCV+Python and how to change colors and add images in live video.
----

This project does a lot. It removes backgroun screen, detects T-shirt in almost any light conditions, replaces T-shirt color.


Watch demo [here](https://www.youtube.com/watch?v=yGOVVHLjbQc).

Requirements
----
1. Green backdrop like [this](http://akash0x53.github.io/images/norm/norm.jpg)
2. Use have to wear blue t-shirt - as it detects only blue color
3. Computer with Camera
4. Python (2.7)
5. OpenCV Python bindings
6. NumPy, Gdk

Test Mode
----
In this mode VDR will not require camera. It will use recorded video for processing.  
To use this is mode set environment variable `VDR_TEST=1`.  
For Example,  

`
akash@SkyFall:~/repos/virtual-dressing-room$ VDR_TEST=1 python vdr
`

Adapt to Camera Resolution
---
You can change `width` and `height` defined in `vdr/config.py` file according to your camera capability.



I will try to add requirements.txt soon.
