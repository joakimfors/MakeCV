import argparse
import sys
import yaml
import mistletoe
from mistletoe.latex_renderer import LaTeXRenderer

from jinja2 import Environment, FileSystemLoader

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yaml', type=str, required=True, help='Input YAML')
    parser.add_argument('-t', '--template', type=str, required=True, help='Jinja2 template')
    parser.add_argument('-i', '--input', type=str, help='Input Markdown')
    parser.add_argument('-o', '--output', type=str, help='Output TeX file')
    args = parser.parse_args()

    env = Environment(
        block_start_string = '\\block{',
        block_end_string = '}',
        variable_start_string = '\\var{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%%',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader=FileSystemLoader('.')
    )

    def md_to_latex(value):
        with LaTeXRenderer() as renderer:
            return renderer.render_inner(mistletoe.Document(value))

    env.filters['latex'] = md_to_latex

    tpl = env.get_template(args.template)

    with open(args.yaml, 'r') as fp:
        data = yaml.safe_load(fp)

    data['title'] = 'Curriculum Vitae'
    if args.input and args.input.endswith('.md'):
        with open(args.input, 'r') as fp:
            data['title'] = 'Personligt brev'
            data['letter'] = fp.read()

    result = tpl.render(**data)
    if args.output:
        with open(args.output, 'w') as fp:
            fp.write(result)
    else:
        print(result)


if __name__ == '__main__':
    main()
