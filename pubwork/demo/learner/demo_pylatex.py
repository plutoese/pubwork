# coding=UTF-8

# --------------------------------------------------------------
# class_latexdoc文件
# @class: LatexDoc
# @introduction: LatexDoc类用来操作latex文档，生成pdf文档
# @dependency: pylatex模块
# @author: plutoese
# @date: 2016.02.18
# --------------------------------------------------------------

from pylatex.base_classes.command import Command, Options
from pylatex import Document, Package, Itemize, Enumerate, Description, Tabular, Figure
from pylatex.utils import NoEscape, escape_latex


class LatexDoc:
    """ LatexDoc类用来创建、操作latex文档，生成pdf文档

    """
    def __init__(self,documentclass='article',options=None,document=None):
        if document is None:
            self.doc = Document(documentclass=documentclass,document_options=options)
        else:
            self.doc = document.doc

    def preamble_append(self,content):
        """ 添加内容到latex文档中

        :param str content: latex格式字符串
        :return: 无返回值
        """
        self.doc.preamble.append(NoEscape(content))

    def append(self,content):
        """ 添加内容到latex文档中

        :param str content: latex格式字符串
        :return: 无返回值
        """
        self.doc.append(NoEscape(content))

    def add_section(self,section_name,level=1):
        """ 添加章节

        :param str section_name: 章节名称
        :param int level: 章节级别，1表示最高级，2其次，3最次。
        :return: 无返回值
        """
        if level < 2:
            self.append(''.join(['\\section*{',section_name,'}']))
        elif level < 3:
            self.append(''.join(['\\subsection*{',section_name,'}']))
        else:
            self.append(''.join(['\\subsubsection*{',section_name,'}']))

    def add_list(self,lists,type=1):
        """ 添加列表

        :param list lists: 列表名称
        :param int type: 列表类型
        :return: 无返回值
        """
        if type == 1:
            items = Itemize()
        elif type == 2:
            items = Enumerate()
        elif type == 3:
            items = Description()
        else:
            items = Itemize()
        for item in lists:
            items.add_item(item)

        self.doc.append(items)

    def add_table(self, data=None):
        """ 添加表格

        :param list data: 表格数据
        :return: 无返回值
        """
        nrow = len(data)
        ncol = len(data[0])

        tabsize = '|' + '|'.join(['c']*ncol) + '|'
        mtable = Tabular(tabsize)

        for i in range(nrow):
            mtable.add_hline()
            mtable.add_row(tuple([str(item) for item in data[i]]))
        mtable.add_hline()
        self.doc.append(Command('begin',arguments='center'))
        self.doc.append(mtable)
        self.doc.append(Command('end',arguments='center'))

    def add_pretty_table(self,data=None,caption='Table',width='90mm'):
        """ 添加漂亮的表格

        :param list data: 表格数据
        :param str caption: 表格名称
        :param str width: 表格宽度
        :return: 无返回值
        """
        ncol = len(data[0])
        self.append(''.join(['\\begin{tabularx}{',width,'}{','X'*ncol,'}']))
        self.append('\\toprule')
        self.append(''.join(['\\multicolumn{',str(ncol),'}{c}{',caption,'} \\\\']))
        self.append(''.join(['\\cmidrule(r){1-',str(ncol),'}']))
        self.append(''.join([' & '.join([str(item) for item in data[0]]),' \\\\']))
        self.append('\\midrule')

        for item in data[1:]:
            self.append(''.join([' & '.join([str(unit) for unit in item]),' \\\\']))
        self.append('\\bottomrule')
        self.append('\\end{tabularx}')

    def add_figure(self,file=None,caption=None,width='240px'):
        """ 添加图形

        :param str file: 图形文件路径
        :param str caption: 图形标题
        :param str width: 图形宽度
        :return: 无返回值
        """
        graph = Figure(position='h!')
        graph.add_image(file, width=width)
        if caption is not None:
            graph.add_caption(caption)
        self.doc.append(graph)

    def add_package(self,name,options=None):
        """ 添加latex包

        :param str name: latex包的名字
        :param list options: latex包的参数
        :return: 无返回值
        """
        self.doc.packages.append(Package(name=name,options=options))

    def generate_tex(self,filepath=None):
        """ 创建.tex文件

        :param str filepath: 文件路径名称
        :return: 无返回值
        """
        self.doc.generate_tex(filepath=filepath)

    def generate_pdf(self,filepath=None):
        """ 创建pdf文件

        :param str filepath: 文件路径名称
        :return: 无返回值
        """
        self.doc.generate_pdf(filepath=filepath)

if __name__ == '__main__':
    #doc = LatexDoc(options=Options('12pt', 'a4paper', 'twoside'))
    doc = LatexDoc(options=['12pt', 'a4paper', 'UTF8'])
    doc.preamble_append('\\usepackage[space,noindent]{ctex}')
    doc.preamble_append('\\usepackage{booktabs}')
    doc.preamble_append('\\usepackage{tabularx}')
    #doc.add_package('ctex',['UTF8','noindent'])
    doc.add_package('geometry', ['tmargin=1cm','lmargin=2cm'])
    doc.append('这是为你写的歌！你知不知道!')
    #doc.append('\\fontsize{18pt}{27pt}这是初号。\\selectfont ')
    doc.append('\\section{章节一}')
    doc.append('$$P(A \cap B) = P(A)P(B)$$')
    doc.append('\\subsection{子章节}')
    doc.add_section("我的第三级章节",3)
    doc.add_section("我的第二级章节",2)
    doc.add_section("我的第三级章节2",3)
    doc.add_list(['我的列表','你的列表'],type=2)
    doc.add_table([['name','gender','age'],['Tom','Male',24],['Marry','Female',19]])
    doc.add_table([['变量', '第一产业占GDP的比重_(全市)', '第一产业占GDP的比重_$市辖区','我错了'],[1,2,3,4],[5,6,7,8]])
    #doc.add_figure(file='d:/down/europe.jpg',caption="Europe",width='360px')
    doc.add_pretty_table(data=[['name','gender','age'],['Tom','Male',24],['Marry','Female',19]])
    doc.generate_pdf(r'D:\down\basic_new.pdf')
    doc.generate_tex(r'D:\down\basic_new.tex')

    '''
    doc.read_from_tex_file(r'E:\github\latexdoc\latexdoc\template\template_one.tex')
    doc.generate_pdf(r'E:\github\latexdoc\latexdoc\generated\basic_new.pdf')
    doc.generate_tex(r'E:\github\latexdoc\latexdoc\generated\basic_new.tex')'''


