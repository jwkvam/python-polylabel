test:
	py.test --cov=./ --mypy --codestyle --docstyle --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF

lint:
	py.test --pylint --pylint-rcfile=pylintrc --pylint-error-types=RCWEF

static:
	mypy farpoint.py
