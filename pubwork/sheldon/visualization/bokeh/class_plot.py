# coding=UTF-8

"""
=========================================
Plot类
=========================================

:Author: glen
:Date: 2017.10.05
:Tags: bokeh plot
:abstract: 连利用bokeh库进行可视化

**类**
==================
Plot
    作图的主类
BarPlot
    柱状图的类
PointPlot
    散点图类

**使用方法**
==================

**示范代码**
==================
::
"""

from bokeh.io import show, output_file
from bokeh.plotting import figure
import pandas as pd
import numpy as np
from bokeh.palettes import Category20_20, Spectral5, Paired12
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, FactorRange, LabelSet
import warnings
warnings.filterwarnings("ignore")


output_file("bars.html")


class Plot:
    """ 作图主类，用于被继承

    :param pandas.DataFrame data_source: 数据源
    :return: 无返回值
    """
    def __init__(self, **kwargs):
        # 设置调色板，默认为Category20_20
        if 'palette' in kwargs:
            self._palette = kwargs['palette']
            kwargs.pop('palette')
        else:
            self._palette = Category20_20
        self._params = kwargs

    def figure(self, **kwargs):
        if 'plot_height' not in kwargs:
            kwargs['plot_height'] = 250
        return figure(**kwargs)


class BarPlot(Plot):
    """ 柱状图类

    :param str x: x变量
    :param str y: y变量
    :param str type: 柱状图类型，选择'vbar'或者'hbar'
    :param pandas.DataFrame data_source: 数据源
    :param function group_fn：分组统计变量，默认为均值函数np.mean
    :return: 无返回值
    """
    def __init__(self, x, y=None, type='vbar', data_source=None, group_fn=np.mean, **kwargs):
        if isinstance(x,(list,tuple)) and len(x) == 1:
            x = x[0]
        if isinstance(y,(list,tuple)) and len(y) == 1:
            y = y[0]
        if isinstance(x,str) and data_source[x].duplicated().any():
            data_source = (data_source.groupby(x)).aggregate(group_fn)
            data_source[x] = list(data_source.index)

        super().__init__(**kwargs)

        if isinstance(x,(list,tuple)):
            for x_value in x:
                data_source[x_value] = data_source[x_value].astype(str)
                column_data_source = ColumnDataSource(data_source)
                column_data_source.data[x_value] = column_data_source.data[x_value].astype(str)
        else:
            data_source[x] = data_source[x].astype(str)
            column_data_source = ColumnDataSource(data_source)
            column_data_source.data[x] = column_data_source.data[x].astype(str)
        self.data_source = data_source
        self.column_data_source = column_data_source

        self._x = x
        self._y = y
        self._type = type
        self._groupfn = group_fn

    def __call__(self, **kwargs):
        """ 作图主函数

        :param kwargs: plot函数的参数
        :return: 返回figure对象
        """
        if isinstance(self._x,(tuple,list)) and len(self._x) > 1:
            return self.grouped_bars(**kwargs)
        if self._type == 'vbar':
            return self.vbars(**kwargs)
        elif self._type == 'hbar':
            return self.hbars(**kwargs)
        else:
            raise TypeError

    def vbars(self,**kwargs):
        # 设置x坐标轴的范围
        x_range = FactorRange(*self.data_source[self._x])
        # 设置填充的颜色
        #print('999',type(self._x),'000',self.data_source[self._y],type(self.data_source[self._y]))
        fill_color = factor_cmap(self._x, palette=self._palette, factors=sorted(self.data_source[self._x].unique()), end=1)
        # 作柱状图
        p = self.figure(x_range=x_range,**self._params)
        #print('hhhh',self._x,self._y)
        p.vbar(x=self._x, top=self._y, width=0.6, fill_color=fill_color, source=self.column_data_source,**kwargs)
        return p

    def hbars(self,**kwargs):
        # 设置y坐标轴的范围
        y_range = FactorRange(*self.data_source[self._x])
        # 设置x坐标轴的范围
        min_number = 0
        if self.data_source[self._y].min() < 0:
            min_number = self.data_source[self._y].min() - 1
        x_range = (min_number,self.data_source[self._y].max()+0.2*self.data_source[self._y].std())
        # 设置填充的颜色
        fill_color = factor_cmap(self._x, palette=self._palette, factors=sorted(self.data_source[self._x].unique()), end=1)
        # 作柱状图
        p = self.figure(y_range=y_range, x_range=x_range, **self._params)
        p.hbar(y=self._x, right=self._y, height=0.5, fill_color=fill_color, source=self.column_data_source,**kwargs)
        return p

    def grouped_bars(self,**kwargs):
        # 设置组别
        grouped = self.data_source.groupby(self._x)
        # 设置大类别
        category = self.data_source[self._x[0]].astype(str)

        # 根据group_fn函数计算每组的值
        aggregate_dataframe = grouped[self._y].agg(self._groupfn)
        # 生成新的数据源
        generated_dataframe = pd.DataFrame(dict(x=list(aggregate_dataframe.index), y=list(aggregate_dataframe)))
        source = ColumnDataSource(generated_dataframe)

        # 设置x坐标轴的范围
        x_range = FactorRange(*generated_dataframe['x'])
        # 设置填充的颜色
        fill_color = factor_cmap('x', palette=self._palette, factors=sorted(category.unique()), end=1)
        # 作柱状图
        p = self.figure(x_range=x_range,**self._params)
        p.vbar(x='x', top='y', width=0.9, source=source, line_color="white",fill_color=fill_color,**kwargs)
        return p


class PointPlot(Plot):
    """ 散点图

    :param str x: x变量
    :param str y: y变量
    :param str label: 点标签变量
    :param str type: 点的形状
    :param pandas.DataFrame data_source: 数据源
    :param str groupby：分组变量
    :return: 无返回值
    """
    def __init__(self, x, y=None, label=None, type='circle', data_source=None, groupby=None, **kwargs):
        super().__init__(**kwargs)
        #self.data_source = data_source
        #self.column_data_source = ColumnDataSource(data_source)
        self._x = x
        self._y = y
        self._label = label
        self._type = type
        self._groupby = groupby
        if groupby is not None:
            data_source[groupby] = data_source[groupby].astype(str)
            column_data_source = ColumnDataSource(data_source)
            column_data_source.data[groupby] = column_data_source.data[groupby].astype(str)
        else:
            column_data_source = ColumnDataSource(data_source)
        self.data_source = data_source
        self.column_data_source = column_data_source

        self._p = self.figure(**kwargs)

    def __call__(self, **kwargs):
        if isinstance(self._x, str) and isinstance(self._y,str):
            if self._groupby is None:
                self.single_plot(**kwargs)
            else:
                self.multi_group_plot(**kwargs)
            if self._label is not None:
                labels = LabelSet(x=self._x, y=self._y, text=self._label, level='glyph', x_offset=5, y_offset=5, source=self.column_data_source, render_mode='canvas')
                self._p.add_layout(labels)
        elif isinstance(self._x, (tuple,list)) and isinstance(self._y, (tuple,list)):
            self.mulit_variable_plot(**kwargs)
        else:
            raise TypeError

        return self._p

    def single_plot(self,**kwargs):
        if self._type == 'circle':
            self._p.circle(self._x, self._y, source=self.column_data_source, color=self._palette[0], **kwargs)
        elif self._type == 'square':
            self._p.square(self._x, self._y, source=self.column_data_source, color=self._palette[0], **kwargs)

    def multi_group_plot(self,**kwargs):
        i = 0
        for name, inngroup in self.data_source.groupby(self._groupby):
            self._p.circle(self._x, self._y, legend=name, source=ColumnDataSource(inngroup), color=self._palette[i], **kwargs)
            i += 2

    def mulit_variable_plot(self,**kwargs):
        i = 0
        for x,y in zip(self._x,self._y):
            self._p.circle(x, y, legend=''.join([x,'~',y]), source=ColumnDataSource(dict({x:self.data_source[x],y:self.data_source[y]})), color=self._palette[i], **kwargs)
            i += 2


class HistPlot(Plot):
    def __init__(self, x, y= None, data_source=None, type=None, **kwargs):
        super().__init__(data_source=data_source)
        if isinstance(x,(list,tuple)) and len(x) == 1:
            x = x[0]
        self._x = x
        self._y = y
        self._palette = kwargs.get('palette', Category20_20)
        self._params = kwargs
        self._p = self.figure(**kwargs)
        self.data_source = data_source
        self.column_data_source = ColumnDataSource(data_source)

    def __call__(self, **kwargs):
        measured = (self.data_source[self._x]).dropna()
        num_of_bins = int(1+3.322*np.log(len(measured)))
        hist, edges = np.histogram(measured, density=True, bins=num_of_bins)

        self._p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],fill_color=self._palette[0])
        self._p.xaxis.axis_label = 'x'
        self._p.yaxis.axis_label = 'Pr(x)'

        return self._p


if __name__ == '__main__':
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    counts = [5, 3, 4, 2, 4, 6]

    mdata = pd.DataFrame({'fruits': fruits, 'counts': counts})
    mdata = mdata.sort_values(by='counts',ascending=True)
    #barplot = BarPlot(x=('fruits',),y='counts',type='vbar', data_source=mdata)

    df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                       'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                       'C': np.random.randn(8), 'D': np.random.randn(8)})
    #barplot = BarPlot(x=['A','B'],y='C',type='vbar',data_source=df,title='这是')
    #show(barplot())

    #circle_plot = PointPlot(x='C',y='D',data_source=df,groupby='A',label='A',plot_width=400,plot_height=400,title='散点图')
    #show(circle_plot(size=10,alpha=0.5))

    random_df = pd.DataFrame(np.random.randn(100, 4), columns=['A', 'B', 'C', 'D'])
    #circle_plot = PointPlot(x=['A','C'],y=['B','D'],data_source=random_df,plot_width=400,plot_height=400,title='散点图')
    #show(circle_plot(size=10,alpha=0.5))

    #hist_plot = HistPlot(x='A',data_source=random_df,plot_width=400,plot_height=400,title='直方图')
    #show(hist_plot())

    mdata = pd.read_excel('d:/data/current.xlsx')
    print(mdata.columns)
    barplot = PointPlot(x=('人口数','出口'), y=('国内生产总值','国内生产总值'), type='vbar', data_source=mdata)
    show(barplot())

    #circle_plot = PointPlot(x='人口数', y='国内生产总值', data_source=mdata, groupby='year', label='region', plot_width=400, plot_height=400, title='散点图')
    #show(circle_plot(size=10, alpha=0.5))

