
runner := "poetry"
# python_runner := "{{runner}} run python"

python_runner := "python"

install:
    {{python_runner}} -m pip install --user -e .

test:
    {{python_runner}} -m pytest .

failed_test:
    {{python_runner}} -m pytest . --nf --lf --tb=short

tdd:
    {{python_runner}} -m pytest . --nf -x --ff --tb=short

clean:
    find . -name "*.pyc" -delete
    git ls-files -o | xargs rm
    {{python_runner}} -m pip uninstall -y git-tools


build: clean install test

