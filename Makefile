SOLR_CORE_CONF_PATH=/Users/mrojas/Downloads/solr-8.11.4/server/solr/wanderwise_mentions/conf

build_solr_schema:
	python manage.py build_solr_schema --configure-directory=$(SOLR_CORE_CONF_PATH) -r RELOAD_CORE

install:
	python manage.py migrate
	python manage.py createsuperuser --user admin --email admin@example.com

scrape:
	python manage.py scrape_reddit
