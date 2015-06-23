from sphof import LeadActor

class TemplateLeadActor(LeadActor):

    def setup(self):
        return
    
    def update(self):
        return
    
    def draw(self):
        return
    
    def on_peer_enter(self, peer, name, hdrs):
        return
    
    def on_peer_exit(self, peer, name):
        return
    
    def on_peer_subscribed(self, peer, name, data):
        return
    
    def on_peer_unsubscribed(self, peer, name, data):
        return
    
    def on_peer_signaled(self, peer, name, date):
        return

if __name__ == "__main__":
    lead_actor = TemplateLeadActor("ExampleLeadActor")
    lead_actor.run()
