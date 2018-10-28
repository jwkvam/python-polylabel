test:
	py.test --cov=./ --mypy --codestyle --docstyle --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF

static:
	mypy -p polylabel
