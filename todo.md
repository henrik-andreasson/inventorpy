# todo

* import twice (negative test) do not work fine for compartment

## via browser
* make input safe for sorting lists

## via rest api
* when server is sent in with incomplete data it does not work very well
* improve audit log, id:s do not explain very well ...
* switch do not set rack, service in model
* UNIQUE constraint failed: firewall.alias

## common

* environment list should be global ..
environment = SelectField(_l('Environment'), choices=[('dev', 'Development'),
                                                      ('tools', 'Tools'),
                                                      ('cicd', 'CI/CD'),
                                                      ('st', 'System Testing'),
                                                      ('at', 'Acceptance Testing'),
                                                      ('prod', 'Production'),
                                                      ]) #_

# bugs


* /inventorpy/app/__init__.py:26: SAWarning: relationship 'User.service' will copy column user.id to column service.manager_id, which conflicts with relationship(s): 'Service.manager' (copies user.id to service.manager_id). If this is not the intention, consider if these relationships should be linked with back_populates, or if viewonly=True should be applied to one or more if they are read-only. For the less common case that foreign key constraints are partially overlapping, the orm.foreign() annotation can be used to isolate the columns that should be written towards.   To silence this warning, add the parameter 'overlaps="manager"' to the 'User.service' relationship. (Background on this error at: https://sqlalche.me/e/14/qzyx)
