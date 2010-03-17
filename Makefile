MANAGE=python2.6 manage.py
MODELVIZ=python2.6 modelviz.py
BACKUPFIXTURE=twitranet-db-backup.json
DEVDB=twitranet-dev.sqlite
DEVPORT=8000

all:
	@echo "Nothing to do by default"

clean: cleancompressed
	find . -name "*.pyc" | xargs rm

test:
	$(MANAGE) test core

savedb:
	$(MANAGE) dumpdata core > $(BACKUPFIXTURE)

restoredb: $(BACKUPFIXTURE)
	$(MANAGE) loaddata $(BACKUPFIXTURE)

resetdb:
	rm -f $(DEVDB)
	$(MANAGE) syncdb --noinput
	$(MANAGE) loaddata users.json

rebuilddb: savedb resetdb restoredb

cleancompressed:
	rm -f compressed/*

rundev: cleancompressed
	$(MANAGE) runserver 0.0.0.0:$(DEVPORT)

schemapng:
	$(MODELVIZ) core | dot -Tpng -o twitranet-schema.png
