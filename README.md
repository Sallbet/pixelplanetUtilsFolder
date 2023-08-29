# ppfun utilities

## areaDownload.py
downloads an area of the canvas into a png file.
Usage: `areaDownload.py startX_startY endX_endY filename.png`
(note that you can copy the current coordinates in this format on the site by pressing R)

## historyDownload.py
downloads the history from a canvas area between two dates.
Needs python and ffmpeg installed
Usage: `python historyDownload.py canvasId startX_startY endX_endY start_date [end_date]`
This is used for creating timelapses, see the cmd help to know how. To get more info type `python historyDownload.py` in cmd

## ppfunChanges.py
Download tiles of pixelplanet
Usage: `ppfunChnages.py canvasID zoomLevel filename.png [filenameToCompare.png] [redownloadImage]`
Needs python and Pillow installed
This is used for downloading tiles, see the cmd help to know how. To get more info type `python ppfunChanges.py` in cmd
