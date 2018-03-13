import ckan.logic as logic
import ckan.authz as authz
import ckan.plugins.toolkit as toolkit
from ckan.lib.base import _
from ckan.logic.auth import (get_package_object, get_group_object,
                            get_resource_object)

try:
    from ckan.lib.plugins import get_permission_labels
except ImportError:
    pass


def user_list(context, data_dict):
    # Get the user name of the logged-in user.
    user = context['user']

    # check if user doesn't exist (e.g. they're not logged-in)
    convert_user_name_or_id_to_id = toolkit.get_converter('convert_user_name_or_id_to_id')
    try:
        user_id = convert_user_name_or_id_to_id(user, context)
    except toolkit.Invalid:
        return {'success': False}
    return {'success': True}