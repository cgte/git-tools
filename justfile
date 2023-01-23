
runner := "poetry"
# python_runner := "{{runner}} run python"

python_runner := "python"

test:
    {{python_runner}} -m pytest .
