# -*- coding: UTF-8 -*-
from plone import api
from datetime import datetime, timedelta
import logging
import pytz

default_profile = 'profile-ploneconf.site:default'

logger = logging.getLogger('ploneconf.site')


def upgrade_site(self):
    self.runImportStepFromProfile(default_profile, 'typeinfo')
    catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    if 'talks' not in portal:
        talks = api.content.create(
            container=portal,
            type='Folder',
            id='talks',
            title='Talks')
    else:
        talks = portal['talks']
    talks_url = talks.absolute_url()
    brains = catalog(portal_type='talk')
    for brain in brains:
        if talks_url in brain.getURL():
            continue
        obj = brain.getObject()
        logger.info('Moving %s' % obj.absolute_url())
        api.content.move(
            source=obj,
            target=talks,
            safe_id=True)


def turn_talks_to_events(self):
    """Set a start- and end-date for old events to work around a
    bug in plone.app.event 1.1.1
    """
    self.runImportStepFromProfile(default_profile, 'typeinfo')
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='talk')
    tz = pytz.timezone("Europe/London")
    dummy_date = tz.localize(datetime.now()) + timedelta(days=30)
    dummy_date = dummy_date.replace(minute=0, second=0, microsecond=0)
    for brain in brains:
        obj = brain.getObject()
        if not getattr(obj, 'start', False):
            obj.start = obj.end = dummy_date
            obj.timezone = "Europe/London"
