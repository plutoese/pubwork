# coding = UTF-8

from bokeh.io import show, output_file
from bokeh.plotting import figure
import pandas as pd
import numpy as np
from bokeh.palettes import Category20_10, Spectral5
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, FactorRange

output_file("bars.html")


class Plot:
    def __init__(self, data_source=None):
        self.data_source = data_source
        self.column_data_source = ColumnDataSource(data_source)

    def figure(self, **kwargs):
        if 'plot_height' not in kwargs:
            kwargs['plot_height'] = 250
        return figure(**kwargs)


class BarPlot(Plot):
    def __init__(self, x, top, type='vbar', data_source=None, **kwargs):
        super().__init__(data_source=data_source)
        self._x = x
        self._top = top
        self._type = type

        print(self.data_source[x])
        x_range = FactorRange(*self.data_source[x])
        self._p = self.figure(x_range=x_range, **kwargs)

    def __call__(self, **kwargs):

        fill_color = factor_cmap(self._x, palette=kwargs.get('palette',Spectral5), factors=sorted(self.data_source[self._x].unique()), end=1)

        if 'type' in kwargs:
            if 'type' == 'vbar':
                pass
            elif 'type' == 'hbar':
                pass
            else:
                raise TypeError
        else:
            pass

        if type == 'vbar':
            p.vbar(x=self._x, top=self._top, source=self.column_data_source, fill_color=fill_color)
        elif type == 'hbar':
            pass
        else:
            raise TypeError

    def bars(self, x, top, fill_color, source):
        p.vbar(x=x, top=top, width=0.9, fill_color=fill_color, source=source)

    def grouped_bars(self):
        pass


df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                   'B' : ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                   'C' : np.random.randn(8), 'D' : np.random.randn(8)})
grouped = df.groupby(['A','B'])

fact = df['A'].astype(str)
#fact = tuple(set(df['A']))

agg_df = grouped['C'].agg(np.mean)
factors = list(agg_df.index)
x = list(agg_df)

mdata = pd.DataFrame(dict(factors = list(agg_df.index), x = list(agg_df)))

source = ColumnDataSource(mdata)

p = figure(x_range=FactorRange(*mdata['factors']),plot_height=250)
#p.vbar(x=factors, top=x, width=0.9, alpha=0.5,palette=Spectral6)

#p.vbar(x='factors', top='x', width=0.9, source=source, line_color="white", fill_color=factor_cmap('factors', palette=Category10_8, factors=sorted(fact.unique()), end=1))

p.scatter([1,2,3],[4,5,6], fill_color=Category20_10[2])

show(p)
#print(grouped)
#print(source)
#print(fact)

print(len(Category20_10))