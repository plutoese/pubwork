# coding = UTF-8

from ipywidgets import interact, interactive, fixed, interact_manual, HBox, VBox, widgets, Layout

database_category = widgets.Dropdown(
    options={'核心数据库': 1, '爬虫数据库': 2, '用户数据库': 3},
    value=1,
    description='请选择',
)

database_choice = widgets.Dropdown(
    options={'':0, '核心数据库': 1, '爬虫数据库': 2, '用户数据库': 3},
    value=0,
    description='请选择',
    disabled = True
)

accordion = widgets.Accordion(children=[HBox([database_category, database_choice])])
accordion.set_title(0, '数据库')
accordion.set_title(1, '数据查询')
accordion