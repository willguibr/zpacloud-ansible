default: install

install:
	rm -f willguibr*
	ansible-galaxy collection build . --force
	ansible-galaxy collection install willguibr* --force
	rm -f willguibr*

doctest:
	for i in $$(ls -1 plugins/modules | grep -v init); do \
		echo "Checking $$i..." ; \
		ansible-doc -M plugins/modules $$i > /dev/null ; \
	done

.PHONY: install doctest
