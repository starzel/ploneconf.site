# -*- coding: UTF-8 -*-
from plone import api
from ploneconf.site.content.talk import Talk
import logging

logger = logging.getLogger(__name__)


def migrate_talk_class(self):
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type="talk")
    for brain in brains:
        obj = brain.getObject()
        if obj.__class__ is not Talk:
            obj.__class__ = Talk
            logger.info('Migrated __class__ of %s' % obj.absolute_url())
