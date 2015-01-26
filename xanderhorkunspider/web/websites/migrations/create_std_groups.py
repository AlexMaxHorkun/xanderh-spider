# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group, Permission
from django.db import models, migrations
from xanderhorkunspider.web.config import settings
from django.contrib.contenttypes.models import ContentType
from xanderhorkunspider.web.websites.models import WebsitesModel

def create_groups_and_permissions(app, schema_editor):
    #read_only
    """group, created = Group.objects.get_or_create(name='read_only')
    if created:
        group.permissions.add(can_read_campaign)
        logger.info('read_only_user Group created')

    #standard
    group, created = Group.objects.get_or_create(name='standard_user')
    if created:
        group.permissions.add(can_edit_users)
        logger.info('standard_user Group created')

    #admin
    group, created = Group.objects.get_or_create(name='admin_user')
    if created:
        group.permissions.add(can_edit_campaign, can_edit_users)
        logger.info('admin_user Group created')"""
    ultimate_content_type = ContentType.objects.get_for_model(WebsitesModel, for_concrete_model=False)
    for group_name, permissions_names in settings.DEFAULT_PERMISSIONS.items():
        group = Group.objects.get_or_create(name=group_name)[0]
        if not group:
            raise RuntimeError("Failed to create group %s" % group_name,)
        for perm_name in permissions_names:
            perm = Permission.objects.get_or_create(codename=perm_name, content_type=ultimate_content_type)[0]
            if not perm in group.permissions.all():
                group.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions,),
    ]
