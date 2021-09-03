# BlenderCompassClino
A lightweight Blender addon for measuring and extracting the dip properties of user-selected mesh faces.  

## Installation
1. Download the latest 'compass_clino.py' file
2. Save .py file within a specified directory on your system
3. In Blender: Edit -> Preferences -> Install
4. Navigate to compass_clino.py file -> select it -> Install Add-on
5. A tab labelled 'Compass-Clino' should appear on the edge of the 3D viewport screen

## Usage
1. In the 3D viewport, enter 'Edit Mode'
2. Using Blender's select tool, select the faces you wish to measure
3. Click on the 'Compass-Clino' tab
4. Click 'Measure Dip'
5. The results are displayed at the mouse hover location, and are automatically copied to the system clip-board
6. You can repeatedly select and measure, each time the result overwrites the last in the system clip-board

## NB
The measurements recorded are Dip and Dip direction. Dip direction assumes the mesh is orientated so that Y = 0 degrees (N). Dip is measured from horiztonal, assuming horizontal to be parallel to the XY plane. The dip and dip direction are calculated as the mean orientations of the selected faces. The error values provided are 95% confidence limits either side of the mean, calculated as 1.96 multipled by the standard error on the mean, and therefore assumes the data are normally distributed. 
