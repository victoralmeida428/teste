from django import template

register = template.Library()

@register.tag
def try_except(parser, token):
    try_node = parser.parse(('except', 'end_try_except'))
    token = parser.next_token()

    except_node = None
    if token.contents == 'except':
        except_node = parser.parse(('end_try_except',))
        parser.delete_first_token()

    return TryExceptNode(try_node, except_node)

class TryExceptNode(template.Node):
    def __init__(self, try_node, except_node):
        self.try_node = try_node
        self.except_node = except_node

    def render(self, context):
        try:
            return self.try_node.render(context)
        except Exception:
            if self.except_node:
                return self.except_node.render(context)
            else:
                return ''

