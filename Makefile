run:
	FLASK_APP=app.py FLASK_ENV=development flask run

#help : Makefile
#    @echo "Makefile available command:"
#    @cat $< | grep "##" | sort | sed -n 's/^## /- /p'
#
#.DEFAULT_GOAL :=help