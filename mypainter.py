from random import randint
from sphof.canvas_actors import CanvasActor
from PIL import Image, ImageDraw

class MyPainter(CanvasActor):
    def setup(self):
        pass
    
    def update(self):
        #print("Painter update")
        #self._img = Image.new("RGB", (200,600), (255,255,55))
        #self._d = ImageDraw.Draw(self._img)
        start = (randint(0,200), randint(0,600))
        end = (randint(0,200), randint(0,600))
        color = (randint(70,110), randint(160,210), randint(70,210))
        self.line([start, end], color, 20)

if __name__ == '__main__':
    test = MyPainter("MyPainter1")

