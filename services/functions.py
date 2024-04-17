import cssutils
from cssutils.css.cssstylesheet import CSSStyleSheet
from cssutils.css.cssstylerule import CSSStyleRule
from cssutils.css.selector import Selector
from cssutils.css import CSSStyleDeclaration


def get_css_styles(
        file_path: str
) -> list[dict[str, str]]:
    """Reads CSS file and returns list of css styles"""
    with open(file_path, 'r') as file:
        css: str = file.read()

    style_list = []
    sheet: CSSStyleSheet = cssutils.parseString(css)
    for rule in sheet:
        rule: CSSStyleRule
        selector: str | Selector = rule.selectorText
        props: str | CSSStyleDeclaration.cssText = rule.style.cssText
        style_list.append({'selector': selector,
                           'props': props})
    return style_list
