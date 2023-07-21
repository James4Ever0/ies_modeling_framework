import subprocess

from tempfile import TemporaryDirectory
import black
import jinja2
import shutil
import os
import pyright # for checking if really installed.

class NeverUndefined(jinja2.StrictUndefined):
    def __init__(self, *args, **kwargs):
        # ARGS: ("parameter 'myvar2' was not provided",)
        # KWARGS: {'name': 'myvar2'}
        if len(args) == 1:
            info = args[0]
        elif "name" in kwargs.keys():
            info = f"Undefined variable '{kwargs['name']}"
        else:
            infoList = ["Not allowing any undefined variable."]
            infoList.append(f"ARGS: {args}")
            infoList.append(f"KWARGS: {kwargs}")
            info = "\n".join(infoList)

        raise Exception(info)


def load_render_and_format(
    template_path: str,
    output_path: str,
    render_params: dict,
    banner: str,
    needFormat: bool = True,
):
    tpl = load_template(template_path)
    result = tpl.render(**render_params)

    print()
    print("______________________[{}]".format(banner))
    print(result)

    # import black.Mode
    output_path_elems = output_path.split(".")
    output_path_elems.insert(-1, "new")
    with open(tmp_output_path := ".".join(output_path_elems), "w+") as f:
        f.write(result)
    if not needFormat:
        shutil.move(tmp_output_path, output_path)
        return
    try:
        # TODO: add more test, like checking for undefined variables, before rewriting the source file.
        # TODO: add rollback mechanism in makefile
        result = black.format_str(result, mode=black.Mode())
        print("Formatter Ok.")
        with TemporaryDirectory() as TP:
            typechecker_input_path = os.path.join(TP, os.path.basename(output_path))
            with open(typechecker_input_path, "w+") as f:
                f.write(typechecker_input_path)
            output = subprocess.run(['pyright', typechecker_input_path], capture_output=True)
            output.stdout # bytes!
            errorRegex = r"^.+?reportUndefinedVariable.+$"
        with open(output_path, "w+") as f:
            f.write(result)
        os.remove(tmp_output_path)
    except:
        import traceback

        traceback.print_exc()
        raise Exception(f"Syntax check failed.\nTemporary cache saved to: '{tmp_output_path}'")
    print("=" * 40)


def code_and_template_path(base_name):
    code_path = f"{base_name}.py"
    template_path = f"{code_path}.j2"
    return code_path, template_path


def load_template(template_path, extra_func_dict={}):
    try:
        assert template_path.endswith(".j2")
    except:
        Exception(f"jinja template path '{template_path}' is malformed.")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("./"),
        extensions=[
            "jinja2_error.ErrorExtension",
            "jinja2.ext.do",
            "jinja2.ext.loopcontrols",
        ],
        trim_blocks=True,
        lstrip_blocks=True,
        # undefined=jinja2.StrictUndefined,
        undefined=NeverUndefined,
    )
    tpl = env.get_template(template_path)
    # def myJoin(mstr, mlist):
    #     print("STR:", repr(mstr))
    #     print("LIST:", repr(mlist))
    #     return mstr.join(mlist)
    func_dict = dict(
        list=list,
        str=str,
        _dict=dict,
        _set=set,  # avoid name collision
        tuple=tuple,
        ord=ord,
        len=len,
        repr=repr,
        # eval=eval,
        #  join=myJoin
        **extra_func_dict,
    )
    tpl.globals.update(func_dict)
    return tpl


def test(cmd: list, exec="python3" if os.name != "nt" else "python"):
    cmd = [exec] + cmd
    p = subprocess.run(cmd)
    p.check_returncode()
