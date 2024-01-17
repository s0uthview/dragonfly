import textwrap
import typing as t

import mistletoe
from mistletoe.contrib.pygments_renderer import PygmentsRenderer

from jinja2.ext import Extension
from jinja2.nodes import CallBlock

from jinja2 import Environment
from jinja2.nodes import Node
from jinja2.parser import Parser


__all__ = ["MarkdownExtension"]


class MarkdownExtension(Extension):
    """A simple Markdown implementation for jinja2 templates."""
    tags = {["markdown"]}

    def __init__(self, environment: "Environment") -> None:
        # initialize Markdown parser
        super(MarkdownExtension, self).__init__(environment)
        self.markdowner = mistletoe
        environment.extend(markdowner=self.markdowner)

    def parse(self, parser: "Parser") -> t.Union["Node", t.List["Node"]]:
        """Handles the use of the '{% markdown %}' block."""
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(
            ("name:endmarkdown", ),
            drop_needle=True
        )

        return CallBlock(
            self.call_method("_render_markdown"),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _render_markdown(self, caller: t.Callable) -> str:
        """Renders a text from Markdown into HTML."""
        text = caller()
        text = self._dedent(text)
        return self.markdowner.markdown(text, PygmentsRenderer)

    @staticmethod
    def _dedent(text: str) -> str:
        # static method to remove newlines from text
        return textwrap.dedent(text.strip("\n"))
