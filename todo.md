# todo

* sorting and filtering
* search
* environment list should be global ..
environment = SelectField(_l('Environment'), choices=[('dev', 'Development'),
                                                      ('tools', 'Tools'),
                                                      ('cicd', 'CI/CD'),
                                                      ('st', 'System Testing'),
                                                      ('at', 'Acceptance Testing'),
                                                      ('prod', 'Production'),
                                                      ]) #_

* make input safe for sorting lists

## via rest api
* when server is sent in with incomplete data it does not work very well
* improve audit log, id:s do not explain very well ...
