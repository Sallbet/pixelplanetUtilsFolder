# Utils for map creation, conversion, 3d models and related stuff

Note:

- EVERY SCRIPT THAT USES REDIS IS JUST AS REFERENCE (node-redis and keys update and change over time and i am not keeping those up-to-date) 
- we use blender 2.8
- js script are executed with `npm run babel-node utils/[scriptname].js`

## areaDownload.py
downloads an area of the canvas into a png file.
Usage: `areaDownload.py startX_startY endX_endY filename.png`
(note that you can copy the current coordinates in this format on the site by pressing R)

## historyDownload.py
downloads the history from an canvas area between two dates.
Needs python and ffmpeg installed
Usage: `python historyDownload.py canvasId startX_startY endX_endY start_date end_date`
This is used for creating timelapses, see the cmd help to know how. To get more info type `python historyDownload.py` in cmd
