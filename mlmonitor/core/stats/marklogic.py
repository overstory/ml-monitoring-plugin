class JsonRestStatSet():

    def __init__(self, name, url, stats):
        self.name = name
        self.url = url
        self.stats = stats

    def newrelic(self):
        return

    def statsd(self):
        return