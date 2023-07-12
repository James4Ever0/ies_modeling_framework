import sys

sys.path.append("../")
import jinja_utils

code_path, template_path = jinja_utils.code_and_template_path("functional_base")

jinja_utils.load_render_and_format(
    template_path, code_path, render_params=dict(), banner="FUNCTIONAL BASE CODE"
)
