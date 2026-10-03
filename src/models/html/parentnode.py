from models.html.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("Node requires a tag")
        if self.children is None:
            raise ValueError("Node requires children")

        html = ""  
        for child in self.children:
            html += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{html}</{self.tag}>'
            

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
