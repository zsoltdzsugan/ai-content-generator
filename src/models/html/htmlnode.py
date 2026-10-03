class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError()


    def props_to_html(self):
        if self.props is None or self.props == "":
            return ""
        html = ""
        for k, v in self.props.items():
            html += f' {k}="{v}"'

        return html


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
