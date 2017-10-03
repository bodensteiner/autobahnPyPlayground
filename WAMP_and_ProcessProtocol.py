from twisted.internet import protocol, reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep

class MyProcessComponent(protocol.ProcessProtocol):

    def __init__(self, session, text):
        self.text = text
        self.session = session

    def connectionMade(self):
        print("Connection to process made")
        self.transport.write(self.text)
        self.transport.closeStdin()

    def outReceived(self, data):
        fieldLength = len(data) / 3

        lines = int(data[:fieldLength])
        words = int(data[fieldLength:fieldLength*2])
        chars = int(data[fieldLength*2:])
        self.transport.loseConnection()
        self.receiveCounts(lines, words, chars)

    def receiveCounts(self, lines, words, chars):
        print 'Received counts from wc.'
        print 'Lines:', lines
        print 'Words:', words
        print 'Characters:', chars

        self.session.publish(u'com.myapp.hello1', 5)

class MyWampComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("session joined")

        self.processObject = MyProcessComponent(self, "accessing protocols through Twisted is fun!\n")
        reactor.spawnProcess(self.processObject, 'wc', ['wc'])

        yield sleep(1)


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1")
    runner.run(MyWampComponent);
