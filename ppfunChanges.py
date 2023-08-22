import requests
import sys
import PIL.Image
import asyncio
import aiohttp
import io

sess = requests.Session()
apime = sess.get("https://pixelplanet.fun/api/me").json()

class Tiles():
    def __init__(self):
        self.width = None
        self.height = None
        self.zoomLevel = None
        self.tiles = []
    
    def set_dimentions(self, zoomLevel):
        self.width = 256*pow(2, zoomLevel)
        self.height = 256*pow(2, zoomLevel)
        self.zoomLevel = zoomLevel
        self.tiles = [[0]*(pow(2, zoomLevel)) for i in range(pow(2, zoomLevel))]

    def create_image(self, filename = None):
        img = PIL.Image.new('RGB', (self.width, self.height))
        for x in range(pow(2, self.zoomLevel)):
            for y in range(pow(2, self.zoomLevel)):
                img.paste(PIL.Image.open(io.BytesIO(self.tiles[x][y])), (256*x, 256*y))
        if filename is not None:
            img.save(filename)
            print('Image saved!')
        img.close()

async def fetch(session, canvasID, zoomLevel, xoffset, yoffset, target_tiles: Tiles):
    url = f'https://pixelplanet.fun/tiles/{canvasID}/{zoomLevel}/{xoffset}/{yoffset}.webp'
    attempts = 0
    while True:
        try:
            async with session.get(url) as resp:
                data = await resp.read()
                target_tiles.tiles[xoffset][yoffset] = data
                print(f"Loaded {url}")
                break
        except:
            if attempts > 3:
                return 
            attempts += 1
            pass

async def get_tiles(canvasID, zoomLevel):
    target_tiles = Tiles()
    target_tiles.set_dimentions(zoomLevel)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for y in range(pow(2, zoomLevel)):
            for x in range(pow(2, zoomLevel)):
                tasks.append(fetch(session, canvasID, zoomLevel, x, y, target_tiles))
        await asyncio.gather(*tasks)
        return target_tiles

if __name__ == '__main__':
    if len(sys.argv) != 4 and len(sys.argv) != 6:
        print("Download tiles of pixelplanet")
        print("Usage: ppfunChnages.py canvasID zoomLevel filename [filenameToCompare] [redownloadImage]")
        print("canvasID: 0 = earth, 1 = moon, 3 = covid, 5 = PixelZone, 6 = PixelCanvas, 7 = 1bit, 8 = top10")
        print("Maximum zoom level is 7.")
        print("Resulting images for zoom levels 0 to 7: 256x256, 512x512, 1024x1024, 2048x2048, 4096x4096, 8192x8192, 16384x16384 and 32768x32768.")
        print("I would recommend you to set zoom level to 5.")
        print("You can compare two images by passing the name of the file as filenameToCompare. It's not requierd argument.")
        print("redownloadImage should be set to True or False (case sensitive) if filenameToCompare is provided. Forces to download tiles again and save them as filename.")
        sys.exit()

    canvasID = sys.argv[1]
    zoomLevel = int(sys.argv[2])
    filename = sys.argv[3]

    if zoomLevel > 7:
        print("Zoom level is too high. Maximum zoom level is 7.")
        sys.exit()

    if canvasID == '3':
        print("Can't get tiles for 3d canvas.")
        sys.exit()

    while True:
        try:
            if (256*pow(2, zoomLevel) < apime["canvases"][canvasID]["size"]):
                break
            else:
                print(f'Resulting image with zoom level {zoomLevel} is bigger than the canvas itself. Trying {zoomLevel-1}.')
                zoomLevel -= 1
                if zoomLevel < 0:
                    print('Tiles for canvas \'{canvasID}\' does not exist.')     
        except KeyError:
            print(f'Canvas with ID {canvasID} does not exist.')
            sys.exit()

    shouldCompare = False
    redownloadImage = True
    if(len(sys.argv) == 6):
        shouldCompare = True
        filenameToCompare = sys.argv[4]
        redownloadImage = False if sys.argv[5] == 'False' else True

    if redownloadImage:
        loop = asyncio.new_event_loop()
        tiles = loop.run_until_complete(get_tiles(canvasID, zoomLevel))
        tiles.create_image(filename)

    if shouldCompare:
        print(f'Comparing images {filename} and {filenameToCompare}')
        with PIL.Image.open(filename) as im1:
            with PIL.Image.open(filenameToCompare) as im2:
                if not im1.size == im2.size:
                    print('Images are not the same size.')
                    sys.exit()
                translucent = PIL.Image.new("RGB", im1.size, (0, 0, 0))
                mask = PIL.ImageChops.difference(im1, im2).convert("L")
                im2.putalpha(32)
                im2.paste(translucent, (0, 0), mask)
                im2.save("difference.png")
        
        print("Done!")