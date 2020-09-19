<%!
    import shutil
    from logging import getLogger

    import onlinejudge_template.generator.python as python
    import onlinejudge_template.generator.about as about
    import onlinejudge_template.generator.hook as hook
%>\
<%
    logger = getLogger(__name__)
    if not shutil.which("yapf"):
        logger.warning("yapf is not installed. If you want to generate well-formatted code, please install it. You can use $ pip3 install yapf")
    else:
        format_config = "{" + ", ".join([
            "BASED_ON_STYLE: google",
            "COLUMN_LIMIT: 9999",
        ]) + "}"
        hook.register_filter_command(["yapf", "--style", format_config], data=data)
%>\
#!/usr/bin/env python3
# from typing import *

${python.declare_constants(data)}

# def solve(${python.formal_arguments(data)}) -> ${python.return_type(data)}:
def solve(${python.formal_arguments(data, typed=False)}):
    pass  # TODO: edit here

# generated by ${about.title} ${about.version} (${about.url})
def main():
${python.read_input(data)}
    ${python.return_value(data)} = solve(${python.actual_arguments(data)})
${python.write_output(data)}

if __name__ == '__main__':
    main()
