
PELICAN=pelican
PELICANOPTS=None

BASEDIR=$(PWD)
INPUTDIR=$(BASEDIR)/
OUTPUTDIR=$(BASEDIR)/_output
CONFFILE=$(BASEDIR)/pelican.conf.py

FTP_HOST=localhost
FTP_USER=anonymous
FTP_TARGET_DIR=/

SSH_HOST=srvb
SSH_USER=data
SSH_TARGET_DIR=/home/data/websites/static/ebenezer-bf.org

DROPBOX_DIR=~/Dropbox/Public/

LESSC=$(BASEDIR)/less.js/bin/lessc


help:
	@echo 'Makefile for a pelican Web site                                       '
	@echo '                                                                      '
	@echo 'Usage:                                                                '
	@echo '   make html                        (re)generate the web site         '
	@echo '   make clean                       remove the generated files        '
	@echo '   ftp_upload                       upload the web site using FTP     '
	@echo '   ssh_upload                       upload the web site using SSH     '
	@echo '   dropbox_upload                   upload the web site using Dropbox '
	@echo '                                                                      '


less:
	$(LESSC) --compress $(BASEDIR)/theme/static/swatchmaker.less $(OUTPUTDIR)/theme/bootstrap.min.css
	@echo 'Done'

js:
	mkdir -p $(OUTPUTDIR)/theme/bootstrap/js/
	cp $(BASEDIR)/theme/static/bootstrap/js/bootstrap-dropdown.js $(OUTPUTDIR)/theme/bootstrap/js/
	cp $(BASEDIR)/theme/static/bootstrap/js/bootstrap-collapse.js $(OUTPUTDIR)/theme/bootstrap/js/
	@echo 'Done'

html: clean $(OUTPUTDIR)/index.html
	@echo 'Done'

$(OUTPUTDIR)/%.html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

clean:
	rm -fr $(OUTPUTDIR)
	mkdir $(OUTPUTDIR)

dropbox_upload: $(OUTPUTDIR)/index.html
	cp -r $(OUTPUTDIR)/* $(DROPBOX_DIR)

ssh_upload: $(OUTPUTDIR)/index.html
	rsync -Cavz -e ssh --delete --exclude="theme/swatch" --exclude="theme/bootstrap" $(OUTPUTDIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

ftp_upload: $(OUTPUTDIR)/index.html
	lftp ftp://$(FTP_USER)@$(FTP_HOST) -e "mirror -R $(OUTPUT_DIR)/* $(FTP_TARGET_DIR) ; quit"

github: $(OUTPUTDIR)/index.html
	ghp-import $(OUTPUTDIR)
	git push origin gh-pages

.PHONY: html help clean ftp_upload ssh_upload dropbox_upload github
    
