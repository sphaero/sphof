from random import randint
import sphof
from sphof import CanvasActor, PainterActor

class MyPainter(PainterActor):

    def setup(self):
        self.count = 0
        return

    def update(self):
        self.count += 1
        if self.count > 60 and len(sphof.shared_ns) < 8:
            self.send_img()
            self.count = 0
            #print(self.count)

    def draw(self):
        #self._img = Image.new("RGB", (200,600), (255,255,55))
        #self._d = ImageDraw.Draw(self._img)
        start = (randint(0,200), randint(0,600))
        end = (randint(0,200), randint(0,600))
        color = (randint(70,110), randint(160,210), randint(70,210))
        self.line([start, end], color, 20)

if __name__ == '__main__':
    test = MyPainter("MyPainter1")
    try:
        test.thread.join()
    except:
        test.stop()
    print("hmm")

