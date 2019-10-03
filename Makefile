.PHONY: translations

# Create the .po and .mo files used for i18n
translations:
	cd src/oscarreports && \
	django-admin makemessages -a && \
	django-admin compilemessages
