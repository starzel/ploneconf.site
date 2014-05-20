from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView


class DemoView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # Do stuff
        return super(DemoView, self).__call__()


class TalkView(DefaultView):
    """ The default view for talks
    """


