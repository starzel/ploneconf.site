# -*- coding: UTF-8 -*-
from plone.dexterity.content import Container
from ploneconf.site.interfaces import ITalk
from zope.interface import implements


class Talk(Container):
    implements(ITalk)
