
runner := "poetry"
# python_runner := "{{runner}} run python"

python_runner := "python"

test:
    {{python_runner}} -m pytest .

failed_test:
    {{python_runner}} -m pytest . --nf --lf --tb=short

tdd:
    {{python_runner}} -m pytest . --nf -x --ff --tb=short

clean:
    find . -name "*.pyc" -delete
    git ls-files -o | xargs rm
