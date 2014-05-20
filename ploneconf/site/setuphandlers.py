# -*- coding: UTF-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-ploneconf.site:default'


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('ploneconf.site_various.txt') is None:
        return

    # Add additional setup code here
    logger = context.getLogger('ploneconf.site')
    site = context.getSite()
    add_catalog_indexes(site, logger)


def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('ploneconf.site')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with
    # ('index_name', 'index_type', 'indexed_attribute')
    wanted = (
        ('type_of_talk', 'FieldIndex', 'type_of_talk'),
        ('speaker', 'FieldIndex', 'speaker'),
        ('audience', 'KeywordIndex', 'audience'),
    )
    indexables = []
    for name, meta_type, attribute in wanted:
        if name not in indexes:
            if attribute:
                extra = {'indexed_attrs': attribute}
                catalog.addIndex(name, meta_type, extra=extra)
            else:
                catalog.addIndex(name, meta_type)
            indexables.append(name)
            if not attribute:
                attribute = name
            logger.info("Added %s '%s' for attribute '%s'.", meta_type, name, extra)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
