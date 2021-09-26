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
