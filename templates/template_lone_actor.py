from sphof import LoneActor

class TemplateLoneActor(LoneActor):

    def setup(self):
        return
    
    def update(self):
        return
    
    def draw(self):
        return

if __name__ == "__main__":
    lone_actor = TemplateLoneActor("ExampleLoneActor")
    lone_actor.run()
