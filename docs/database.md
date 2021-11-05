# clean database

* mv app.db demo.db
* flask db init
* flask db migrate -m baseline
* flask db upgrade
* flask user new admin foo123 admin@example.com
