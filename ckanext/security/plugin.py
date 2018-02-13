import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic.schema

from ckanext.security import schema

def ckanext_security_user_show(context, data_dict):
    #just returning success true, no logic check is made since if user is not logged
    #in user not allowed to view user details
    return {'success':True}

class CkanSecurityPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IAuthFunctions)

    def update_config(self, config):
        # Monkeypatching all user schemas in order to enforce a stronger password
        # policy. I tried mokeypatching `ckan.logic.validators.user_password_validator`
        # instead without success.
        ckan.logic.schema.default_user_schema = schema.default_user_schema
        ckan.logic.schema.user_new_form_schema = schema.user_new_form_schema
        ckan.logic.schema.user_edit_form_schema = schema.user_edit_form_schema
        ckan.logic.schema.default_update_user_schema = schema.default_update_user_schema
        toolkit.add_template_directory(config, 'templates')

    def before_map(self, urlmap):
        userController = 'ckanext.security.controllers:SecureUserController'
        urlmap.redirect('/user/edit/', '/user/edit')
        urlmap.connect('/user/edit', controller=userController, action='edit')
        urlmap.connect('/user/edit/{id:.*}', controller=userController, action='edit', ckan_icon='cog')
        urlmap.connect('/user/reset/{id:.*}', controller=userController, action='perform_reset')
        urlmap.connect('/user/reset', controller=userController, action='request_reset')
        return urlmap

    def after_map(self, urlmap):
        return urlmap

    def get_auth_functions(self):
        return {'user_show':ckanext_security_user_show}

