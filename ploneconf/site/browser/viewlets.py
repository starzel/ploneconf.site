# -*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from collections import OrderedDict
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from ploneconf.site.content.sponsor import LevelVocabulary
from ploneconf.site.behavior.social import ISocial
from random import shuffle
from time import time
from zope.component import getMultiAdapter


class SocialViewlet(ViewletBase):

    def lanyrd_link(self):
        adapted = ISocial(self.context)
        return adapted.lanyrd


class SponsorsViewlet(ViewletBase):

    @ram.cache(lambda *args: time() // (60 * 60))
    def _sponsors(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(portal_type='sponsor')
        results = []
        for brain in brains:
            obj = brain.getObject()
            scales = getMultiAdapter((obj, self.request), name='images')
            scale = scales.scale('logo', width=200, height=80, direction='down')
            tag = scale.tag() if scale else ''
            if not tag:
                # only display sponsors with a logo
                continue
            results.append(dict(
                title=brain.Title,
                description=brain.Description,
                tag=tag,
                url=obj.url or obj.absolute_url(),
                level=obj.level
            ))
        return results

    def sponsors(self):
        sponsors = self._sponsors()
        if not sponsors:
            return
        results = OrderedDict()
        levels = [i.value for i in LevelVocabulary]
        for level in levels:
            level_sponsors = []
            for sponsor in self._sponsors():
                if level == sponsor['level']:
                    level_sponsors.append(sponsor)
            if not level_sponsors:
                continue
            shuffle(level_sponsors)
            results[level] = level_sponsors
        return results
