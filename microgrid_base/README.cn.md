
# 微电网算法服务

该目录的主要目的是建立IES系统模型并优化其运行。

用户定义拓扑结构，其中包括负载、电网、能源和发电机等设备。

输入和输出遵循标准格式。建模语言 "IESLang "用于描述系统。

## 使用方法

最简单的设置方法是安装所有依赖项，然后在基本目录下调用`make`。

在不同的系统上，您可能需要修改`Makefile`中的代码以确保正确的依赖关系解析。

在系统中安装 CPLEX 和 Anaconda（用于环境管理）。不要使用非Linux操作系统进行部署，因为它们不支持 "tmux"。

最低Python版本为`3.9`。

通过 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt` 安装 Python 依赖项。

要运行`celery`，需要安装`redis-server`和`rabbitmq-server`。

## 开发

如果有些文件是由模板生成的，不要修改它们。相反，找到相关的".j2 "文件并修改它，然后调用基本目录下的`make test`，以确保你的修改不会带来更多麻烦。

## 路线图

* [x] 创建算法服务
* [x] 解析EXCEL中的输入参数
* [x] 创建名称映射表
* [x] 定义端口类型和连接矩阵
* [x] 使用jinja2和宏生成模型代码
* [x] 准备生成测试
* [ ] 定义和解析 `*.ies` DSL

## 文件结构

- cplex_convex_debug: 用于调试cplex求解器的测试文件
    - init.sh：用于将`*.lp`文件移动到此目录。
- dsl_parser: 国际标准语言解析器和代码生成器
    - functional_base.py: 实验性功能执行机制
    - functional_base.py.j2: 用于生成functional_base.py.j2。
    - generate_code.py：用于读取functional_base.py.j2并生成python代码。
    - lex_yacc.py: 用于标记化和解析IES代码（实验）
    - Makefile: 定义与IESLang相关的构建任务
    - mylang.ies: iesl 语言规范
    - mylang.txt: 传统语言规范
    - pyomo_reduce_ineqalities.py：用于从ineqality表达式系统中计算变量边界，被iesl使用。
    - yacc_init.py: 实验解析器
    - your_model_name.lp：实验模型导出为包含汉字的lp文件。
    - 柴油.IS: 用IES语言编写的柴油发电机模型
- frontend_convert_format: 将非标准的前端数据转换为标准的模型规范格式，供前端使用。
    - customToolbar.vue：前端使用的代码，包括输入数据构造逻辑
    - cvt.js: 非标准输入格式转换
    - error_cvt.js: 错误信息的处理 (翻译)
    - input_template_processed.json: 输入模板示例
    - sample_parse.json: 部分清理过的非标准输入数据
    - sample.json: 原始非标准输入数据
- logs: 保留用于日志记录的目录
    - .log:需要被触动，以便在发布归档`release.7z`中保留此目录。
- makefile_ninja_pytest_incremental_test
    - platform_detect_makefile: 用于使用makefile检测不同的操作系统。
        - Makefile: os 检测实现
    - construct_ninja_file.py: 使用 "ninja_syntax "包生成ninja.build文件。
    - dodo.py: 包 "pydo "的实验
    - generic.py：python类型系统实验
    - lfnf.py：用于测试pytest"-lfnf "命令行标志的pytest文件。
    - Makefile.j2: 用于生成Makefile的jinja测试模板
    - mytest.py：使用类型提示和请求夹具的pytest文件
    - test_buffer.py：conda stdout缓冲机制的无限循环
    - type_check.py: python类型系统的多重实验
    - typecheck.py: exhausitiveness的静态检查
- microgrid_server_release: 用于服务分配
    - constants_en.txt: 由merged_units.txt导入的常量定义
    - merged_units.txt: 包 "pint "使用的修改过的单元定义
    - init：服务器设置脚本（不完整）
        - init.sh: bash 安装脚本
        - requirements.txt: python需求文件
    - 服务器：主服务器代码
        - export_format_validate.py: 验证并输出数据
        - export_format.json: `solve_model.py`用于数据验证。
        - expr_utils.py: 用于分析异常中的表达式
        - fastapi_celery_server.py: 用于模型求解的celery worker
        - fastapi_datamodel_template.py: api的数据交换模式
        - fastapi_server_template.py: fastapi服务器代码，它定义了apis。
        - fastapi_terminate_service.sh: 用于查找并杀死以前的算法服务（用于重启）。
        - fastapi_tmuxp.sh: 通过在一个tmux会话中创建四个面板来启动服务
        - fastapi_tmuxp.yml: tmuxp读取的配置文件，用于创建tmux会话。
        - frontend_sim_param_translation.json: 将中文表头翻译为预定义术语以便输出
        - ies_optim.py: 模型定义和实现
        - passwords.py：存储redis的密码，被`fastapi_celery_server.py`使用。
        - solve_model.py：接收输入作为模型规范，调用优化会话并创建结果。
        - template_input.json: api输入数据格式示例
        - test_json_input_format.py：测试读取输入数据文件，检查拓扑一致性，模型求解和数据输出。
        - test_topo_check.py：测试使用代码构建模型拓扑作为输入数据，并检查拓扑一致性、模型求解和数据导出。
        - topo_check.py: 用于构建模型拓扑和检查的工具
        - unit_utils.py: 用于单位换算的实用工具
    - test: 测试代码
        - sample_data: 存储可能导致系统问题的数据
        - common_fixtures.py: `test_model.py`使用的共享固定装置
        - common_fixtures.py.j2：使用`ies_optim.py`生成输入数据夹具到`common_fixtures.py.tmp`的代码模板。
        - common_fixtures.py.tmp：模板生成目标，在编写`common_fixtures.py`时用作参考。
        - conic_problem.py: 使用numpy解决虚构优化非线性目标的实验
        - dev_info_tmp_gen.py: 读取`common_fixtures.py.j2`并生成`.tmp` target
        - generate_test_model.py: 读取`test_model.py.j2`并生成`test_model.py`。
        - test_model.py: 主模型代码的测试代码
        - Makefile：测试makefile，通过指定构建依赖关系来方便构建
- Makefile：用于生成代码的主makefile，定义编译依赖关系，处理并在子make会话中共享环境变量。
- ies_optim.py.j2: 生成主模型代码的模板
- jinja_utils.py：用于读取和渲染模板、测试和格式化生成代码的实用工具。
- type_system_v2.py：拓扑类型系统生成
- parse_params.py: 用于代码生成的共享参数
- parse_frontend_sim_param_translation.py: 解析`.js`文件并生成导出表头翻译图
- parse_export_format.py: 生成`export_format_validate.py`。
- parse_optim_constraints.py：通过解析`ies_optim.py`生成`constraints.log`（其中包含模型中使用的所有约束）。
- parse_units_and_names.py：生成`microgrid_jinja_param_base.py`，用于`ies_optim.py`中的输入数据结构和单元定义。