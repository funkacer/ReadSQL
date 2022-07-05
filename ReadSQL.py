# sys.version_info[0]

#conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES) PARSE_COLNAMES
#import socket
#print(socket.gethostname())

# SELECT database();
# TODO: command {command} was not recognized
# TODO: no data returned must not delete global data
# TODO: delete:data Command
# TODO: pause: make clever

import sys
import os
import argparse
import sqlite3
import traceback
import socket
import time
import datetime
#from datetime import timedelta, datetime, date, time
import random
import copy

from importlib.metadata import version

import multiprocessing as mp

import logging

from src.params import variables, command_options

is_np = False
try:
    import numpy as np
    is_np = True
except Exception as e:
    traceback.print_exc()

is_mpl = False
try:
    import matplotlib.pyplot as plt
    is_mpl = True
except Exception as e:
    traceback.print_exc()

#from Scipy.stats import skew


def __rd(x,y=2):
    ''' A classical mathematical rounding by Voznica '''
    try:
        m = int('1'+'0'*y) # multiplier - how many positions to the right
        q = x*m # shift to the right by multiplier
        c = int(q) # new number
        i = int( (q-c)*10 ) # indicator number on the right
        if i >= 5:
            c += 1
        result = '{num:.{prec}f}'.format(num=c/m,prec=y)
    except:
        result = ''
    return result

def getHistogram(colsp, ci, cspi, title='Graf'):
    '''
    Takes disctionary of labels and np arrays for boxplots
    '''
    #print("Split:", colsp[ci]['split'])
    if cspi is None:
        fig, ax = plt.subplots()
        n, bins, patches = ax.hist(colsp[ci]['array_valids']['value'], 50, density=True, facecolor='g', alpha=0.75)
        plt.title(title)
        plt.tight_layout()
        plt.show()
    else:
        cspis = str(cspi)
        #print("Cats:", colsp[cspi]['cats'])
        fig, ax = plt.subplots()
        bins = np.linspace(20, 100, 100)
        for cspiss in colsp[ci]['split']:
            if cspis in cspiss:
                print(cspiss)
                for cat in colsp[ci]['split'][cspiss]:
                    n, bins, patches = ax.hist(colsp[ci]['split'][cspiss][cat]['value'], bins, alpha=0.5, label=cat)
        #n, bins, patches = ax.hist(colsp[ci]['m'], 50, density=True, facecolor='g', alpha=0.75)
        ax.legend(loc='upper right')
        plt.title(title)
        plt.tight_layout()
        plt.show()


def getLineChartI(colsp, ci, title='Graf'):
    '''Tato funkce akceptuje df a nazvy sloupcu, vraci HTML kod vertikalniho grafu'''
    rotation = 90
    #sort_values = True
    #sort_ascending = True
    precision = 0
    cols = colsp[ci]['categ_counts']['value']
    print(len(cols))
    '''
    if len(cols) > 0:
        width = 0.8/len(cols)
    else:
        width = 1
    '''
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(range(len(cols)), colsp[ci]['categ_counts']['count'])
    '''
    plt.bar(range(len(cols)), [colsp[ci]['c'][col] for col in cols])
    rects = plt.bar(range(len(cols)), [colsp[ci]['c'][col] for col in cols])
    for rect in rects:
        ax.annotate(text = __rd(rect.get_height(),precision), xy = (rect.get_x() + rect.get_width()/2, rect.get_height()/2), ha = 'center', va = 'bottom')
    '''
    plt.xticks(range(len(cols)), cols, rotation = rotation)
    plt.title(title)
    '''
    #plt.show()
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    '''
    plt.tight_layout()
    plt.show()


def getBarChartI(colsp, ci, title='Graf'):
    '''Tato funkce akceptuje df a nazvy sloupcu, vraci HTML kod vertikalniho grafu'''
    rotation = 90
    #sort_values = True
    #sort_ascending = True
    precision = 0
    cols = colsp[ci]['categ_counts']['value']
    if len(cols) > 0:
        width = 0.8/len(cols)
    else:
        width = 1
    fig, ax = plt.subplots(figsize = (10,5))
    rects = plt.bar(range(len(cols)), colsp[ci]['categ_counts']['count'])
    for rect in rects:
        ax.annotate(text = __rd(rect.get_height(),precision), xy = (rect.get_x() + rect.get_width()/2, rect.get_height()/2), ha = 'center', va = 'bottom')
    plt.xticks(range(len(cols)), cols, rotation = rotation)
    plt.title(title)
    '''
    #plt.show()
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    '''
    plt.tight_layout()
    plt.show()


def getBarChartV(ci):
    '''Tato funkce akceptuje df a nazvy sloupcu, vraci HTML kod vertikalniho grafu'''
    #df, columns, title='Graf', rotation = 45, sort_values = True, sort_ascending = True, limit = 100, precision = 0
    #df = self.__df
    #columns = df.columns
    #if show_columns != '': columns = show_columns
    title='Graf'
    rotation = 90
    #sort_values = True
    #sort_ascending = True
    limit = 100
    precision = 1
    cols = list(colsp[ci]['c'].keys())
    print(cols)
    '''
    for i, column in enumerate(columns):
        #raise error if not found
        cols.append(df.columns.get_loc(column))
    if sort_values:
        df.sort_values(by=df.columns[cols[0]], axis = 0, inplace = True, ascending = sort_ascending)
    else:
        df.sort_index(inplace = True, ascending = sort_ascending)
    df = df.head(limit)
    '''
    ind = range(len(cols))
    width = 0.8/len(cols)
    fig, ax = plt.subplots(figsize = (10,5))
    rectss = []
    #bottom=[0 for i in range(len(cols))]
    # this makes stack
    for i in range(1):
        #rectss.append(plt.bar(ind, colsp[ci]['c'][cols[i]], bottom = bottom, label = cols[i]))
        rectss.append(plt.bar(ind, [colsp[ci]['c'][col] for col in cols]))
        #bottom += colsp[ci]['c'][cols[i]]
    #bottom=[0 for i in range(len(cols))]
    for rects in rectss:
        #bott = []
        for i, rect in enumerate(rects):
            if len(cols) == 1:
                #ax.annotate(s = self.__rd(rect.get_height(),precision), xy = (rect.get_x() + rect.get_width()/2, rect.get_height() + bottom[i]), ha = 'center', va = 'bottom')
                ax.annotate(s = __rd(rect.get_height(),precision), xy = (rect.get_x() + rect.get_width()/2, rect.get_height()), ha = 'center', va = 'center')
            else:
                #ax.annotate(s = self.__rd(rect.get_height(),precision), xy = (rect.get_x() + rect.get_width()/2, rect.get_height()/2 + bottom[i]), ha = 'center', va = 'center')
                ax.annotate(s = __rd(rect.get_height(),precision), xy = (rect.get_x() + rect.get_width()/2, rect.get_height()/2), ha = 'center', va = 'center')
            #bott.append(rect.get_height())
        #bottom += bott
    plt.xticks(ind, cols, rotation = rotation)
    plt.title(title)
    #ax.legend(loc='upper center', bbox_to_anchor=(1.1, 1),
    #      ncol=1, fancybox=True, shadow=True)
    '''
    #plt.show()
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    '''
    plt.show()


def getBoxplotI(colsp, colsi, title = 'Box Plot', boxplot_showfliers = True):
    '''
    Takes disctionary of labels and np arrays for boxplots
    '''
    #data_df = self.__data_df
    #boxplot_showfliers = True

    #bottom = np.inf
    #top = -np.inf

    #for key in np_dict.keys():
        #data_part_np = data_df.iloc[data_df[data_df[column].isnull() == 0].index,data_df.columns.get_loc(column)].to_numpy()
        #data_part_np = data_df.loc[data_df[data_df[column].isnull() == 0].index, column].to_numpy()
        #print(data_part_np)
        #data_np[i] = data_part_np
        #bottom = min(bottom, np_dict[key].min())
        #top = max(top, np_dict[key].max())

    #margin = (top - bottom)*0.1
    #if margin == 0: margin = top*0.1 # if top == bottom
    #bottom -= margin
    #top += margin

    np_dict = {}

    for ci in colsi:
        #print(colsp[ci]['m'])
        #for i, column in enumerate(column_list):
        #data_part_np = data_df.iloc[data_df[data_df[column].isnull() == 0].index,data_df.columns.get_loc(column)].to_numpy()
        #data_part_np = data_df.loc[data_df[data_df[column].isnull() == 0].index, column].to_numpy()
        #data_part_np = np.array(colsp[ci]['m'])
        data_part_np = colsp[ci]['array_valids']['value']
        #print(data_part_np)
        #data_np[i] = data_part_np
        np_dict[colsp[ci]['name']] = data_part_np

    fig1, ax1 = plt.subplots()
    ax1.set_title(title)
    ax1.boxplot(np_dict.values(), showfliers=boxplot_showfliers, showmeans = True, meanline=True)
    #ax1.boxplot(np_list, showfliers=True, showmeans = True, meanline=True, conf_intervals = [[None,None],[None,None]], notch = True)
    #plt.xticks(range(1, len(column_list)+1), [str(c) + ' (n=' + str(len(np_list[i])) + ')' for i, c in enumerate(column_list)], rotation = 90)
    plt.xticks(range(1, len(np_dict)+1), [str(key) + ' (n=' + str(len(np_dict[key])) + ')' for key in np_dict.keys()], rotation = 90)
    #plt.ylim(bottom, top)
    #ax1.legend([{'k--':'A simple line'}])
    #legend
    ax1.plot([1,1], [1,1], 'darkorange', label='Median')
    ax1.plot([1,1], [1,1], 'g--', label='Mean')
    #legend = ax1.legend(loc='upper right', shadow=True, fontsize='x-large')
    legend = ax1.legend(bbox_to_anchor=(1, 1))
    # Put a nicer background color on the legend.
    #legend.get_frame().set_facecolor('C0')
    plt.tight_layout()
    plt.show()


def colorCode(color):
    cc = ""
    cc0 = ["", "\033[1m", "\033[4m", "\033[1m\033[4m"]
    colorcode0 = 0
    colorcode1 = 0
    colorcode2 = 0
    if color >= 10000:
        colorcode2 = int(color/10000)
        colorcode1 = color - colorcode2*10000
    else:
        colorcode1 = color
    if colorcode1 >= 3000:
        colorcode1 = colorcode1-int(colorcode1/1000)*1000
        colorcode0 = 3
    elif colorcode1 >= 2000:
        colorcode1 -= 2000
        colorcode0 = 2
    elif colorcode1 >= 1000:
        colorcode1 -= 1000
        colorcode0 = 1
    #print(colorcode0, colorcode1, colorcode2)
    if color >= 10000:
        cc = cc0[colorcode0] + '\033[38;5;' + str(colorcode1) + 'm' + '\033[48;5;' + str(colorcode2) + 'm'
    else:
        cc = cc0[colorcode0] + '\033[38;5;' + str(colorcode1) + 'm'
    return cc


def terminal_resize(colsp):
    columns, rows = os.get_terminal_size()
    #print(columns, rows)
    width = 0
    screen = 1
    first = 0
    for col in colsp:
        if first == 0: first = colsp[col]['w']
        width += colsp[col]['w']
        if width >= columns:
            screen += 1
            width = first + colsp[col]['w']
        colsp[col]['screen'] = screen
        #print(col, screen)


def data_split_prep_mp(inn):
    colsp = inn[0]
    colspi = inn[1]
    for cspi in colspi:
        colsp[cspi]['cats'] = {}
        '''
        for cat in colsp[cspi]['c']:
            colsp[cspi]['cats'][cat] = []  #find rows for every category
            #print(cat)
        '''
        for av in colsp[cspi]["array_valids"]:
            if colsp[cspi]['cats'].get(av['value']) is None:
                colsp[cspi]['cats'][av['value']] = []
            colsp[cspi]['cats'][av['value']].append(av['row'])

    return [cspi, colsp[cspi]['cats']]


def data_split_prep(colsp, colspi):
    for cspi in colspi:
        colsp[cspi]['cats'] = {}
        '''
        for cat in colsp[cspi]["categ_counts"]:
            colsp[cspi]['cats'][cat[0]] = []  #find rows for every category
            #print(cat)
        '''
        # make better
        for av in colsp[cspi]["array_valids"]:
            if colsp[cspi]['cats'].get(av['value']) is None:
                colsp[cspi]['cats'][av['value']] = []
            colsp[cspi]['cats'][av['value']].append(av['row'])
    return colsp


def data_split_mp(inn):
    #global colsp

    colsp = inn[0]
    colsi = inn[1]
    colspi = inn[2]
    combine = inn[3]

    if not combine:
        for cspi in colspi:
            cspis = str(cspi)   #level 0 (level 1 will be "cspi1,cspi2", and so on)
            for ci in colsi:
                #print(colsps)
                colsp[ci]['split'][cspis] = {}
                for cat in colsp[cspi]['cats']:
                    #print(cat, colsp[ci]['split'][cspis][cat][:5])
                    ind = 0
                    filterr = []
                    maxx = len(colsp[cspi]['cats'][cat])
                    print(colsp[cspi]['name'], cat, len(colsp[cspi]['cats'][cat]))
                    for i in colsp[ci]["array_valids"]:
                        if i[0] >= colsp[cspi]['cats'][cat][ind]:
                            while i[0] > colsp[cspi]['cats'][cat][ind]:
                                ind += 1
                                if ind >= maxx: break
                            if ind >= maxx: break
                            if i[0] == colsp[cspi]['cats'][cat][ind]:
                                filterr.append(True)
                            else:
                                filterr.append(False)
                            ind += 1
                        else:
                            filterr.append(False)
                        if ind >= maxx: break
                    for i in range(len(colsp[ci]["array_valids"])-len(filterr)):
                        filterr.append(False)
                    #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                    colsp[ci]['split'][cspis][cat] = colsp[ci]["array_valids"][filterr]
                    if colsp[ci]['type'] == "Integer" or colsp[ci]['type'] == "Float":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["array_valids"]['value'].mean(),2))
                    elif colsp[ci]['type'] == "Datetime" or colsp[ci]['type'] == "Date" or colsp[ci]['type'] == "Time":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["array_valids"]['value'].max())
                    else:
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5])
    else:
        for ci in colsi:
            cspi = colspi[0]
            cspis = str(cspi)   #level 0 (level 1 will be "cspi1,cspi2", and so on)
            #print(colsps)
            colsp[ci]['split'][cspis] = {}
            for cat in colsp[cspi]['cats']:
                #print(cat, colsp[ci]['split'][cspis][cat][:5])
                ind = 0
                filterr = []
                maxx = len(colsp[cspi]['cats'][cat])
                print(colsp[cspi]['name'], cat, len(colsp[cspi]['cats'][cat]))
                for i in colsp[ci]["array_valids"]:
                    if i[0] >= colsp[cspi]['cats'][cat][ind]:
                        while i[0] > colsp[cspi]['cats'][cat][ind]:
                            ind += 1
                            if ind >= maxx: break
                        if ind >= maxx: break
                        if i[0] == colsp[cspi]['cats'][cat][ind]:
                            filterr.append(True)
                        else:
                            filterr.append(False)
                        ind += 1
                    else:
                        filterr.append(False)
                    if ind >= maxx: break
                for i in range(len(colsp[ci]["array_valids"])-len(filterr)):
                    filterr.append(False)
                #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                colsp[ci]['split'][cspis][cat] = colsp[ci]["array_valids"][filterr]
                if colsp[ci]['type'] == "Integer" or colsp[ci]['type'] == "Float":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["array_valids"]['value'].mean(),2))
                elif colsp[ci]['type'] == "Datetime" or colsp[ci]['type'] == "Date" or colsp[ci]['type'] == "Time":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["array_valids"]['value'].max())
                else:
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5])

            print ("ci", ci, "cspis", cspis)

            if len(colspi) > 1:
                # do levels of split from 1 on (0 is done)
                for level in range(1, len(colspi)):
                    print("level", level)
                    cspis = ",".join([str(colspi[l]) for l in range(level+1)])
                    print("cspis", cspis)
                    cspisp = ",".join([str(colspi[l]) for l in range(level)])
                    print("cspisp", cspisp)

                    cspi = colspi[level]

                    #print(colsps)
                    colsp[ci]['split'][cspis] = {}
                    for cat in colsp[cspi]['cats']:
                        #print(cat, colsp[ci]['split'][cspis][cat][:5])
                        maxx = len(colsp[cspi]['cats'][cat])
                        print("col, cat, len", colsp[cspi]['name'], cat, len(colsp[cspi]['cats'][cat]))
                        for catp in colsp[ci]['split'][cspisp]:
                            ind = 0
                            filterr = []
                            print("catp, len", catp, len(colsp[ci]['split'][cspisp][catp]))
                            for i in colsp[ci]['split'][cspisp][catp]:
                                if i[0] >= colsp[cspi]['cats'][cat][ind]:
                                    while i[0] > colsp[cspi]['cats'][cat][ind]:
                                        ind += 1
                                        if ind >= maxx: break
                                    if ind >= maxx: break
                                    if i[0] == colsp[cspi]['cats'][cat][ind]:
                                        filterr.append(True)
                                    else:
                                        filterr.append(False)
                                    ind += 1
                                else:
                                    filterr.append(False)
                                if ind >= maxx: break
                            for i in range(len(colsp[ci]['split'][cspisp][catp])-len(filterr)):
                                filterr.append(False)
                            #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                            catn = catp + " - " + cat   # change " - " to user option
                            print("cspis", cspis, "catn", catn)
                            colsp[ci]['split'][cspis][catn] = colsp[ci]['split'][cspisp][catp][filterr]
                            '''
                            if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float":
                                print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["av"]['value'].mean(),2))
                            elif colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time":
                                print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["av"]['value'].max())
                            else:
                                print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5])
                            '''

    return [ci, colsp[ci]['split']]


def data_split(colsp, colsi, colspi, combine = True):

    if not combine:
        for cspi in colspi:
            cspis = str(cspi)   #level 0 (level 1 will be "cspi1,cspi2", and so on)
            for ci in colsi:
                #print(colsps)
                colsp[ci]['split'][cspis] = {}
                for cat in colsp[cspi]['cats']:
                    #print(cat, colsp[ci]['split'][cspis][cat][:5])
                    ind = 0
                    filterr = []
                    maxx = len(colsp[cspi]['cats'][cat])
                    print(colsp[cspi]['name'], cat, len(colsp[cspi]['cats'][cat]))
                    for i in colsp[ci]["array_valids"]:
                        if i[0] >= colsp[cspi]['cats'][cat][ind]:
                            while i[0] > colsp[cspi]['cats'][cat][ind]:
                                ind += 1
                                if ind >= maxx: break
                            if ind >= maxx: break
                            if i[0] == colsp[cspi]['cats'][cat][ind]:
                                filterr.append(True)
                            else:
                                filterr.append(False)
                            ind += 1
                        else:
                            filterr.append(False)
                        if ind >= maxx: break
                    for i in range(len(colsp[ci]["array_valids"])-len(filterr)):
                        filterr.append(False)
                    #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                    colsp[ci]['split'][cspis][cat] = colsp[ci]["array_valids"][filterr]
                    if colsp[ci]['type'] == "Integer" or colsp[ci]['type'] == "Float":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["array_valids"]['value'].mean(),2))
                    elif colsp[ci]['type'] == "Datetime" or colsp[ci]['type'] == "Date" or colsp[ci]['type'] == "Time":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["array_valids"]['value'].max())
                    else:
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5])
    else:
        for ci in colsi:
            cspi = colspi[0]
            cspis = str(cspi)   #level 0 (level 1 will be "cspi1,cspi2", and so on)
            #print(colsps)
            colsp[ci]['split'][cspis] = {}
            for cat in colsp[cspi]['cats']:
                #print(cat, colsp[ci]['split'][cspis][cat][:5])
                ind = 0
                filterr = []
                maxx = len(colsp[cspi]['cats'][cat])
                print(colsp[cspi]['name'], cat, len(colsp[cspi]['cats'][cat]))
                for i in colsp[ci]["array_valids"]:
                    if i[0] >= colsp[cspi]['cats'][cat][ind]:
                        while i[0] > colsp[cspi]['cats'][cat][ind]:
                            ind += 1
                            if ind >= maxx: break
                        if ind >= maxx: break
                        if i[0] == colsp[cspi]['cats'][cat][ind]:
                            filterr.append(True)
                        else:
                            filterr.append(False)
                        ind += 1
                    else:
                        filterr.append(False)
                    if ind >= maxx: break
                for i in range(len(colsp[ci]["array_valids"])-len(filterr)):
                    filterr.append(False)
                #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                colsp[ci]['split'][cspis][cat] = colsp[ci]["array_valids"][filterr]
                if colsp[ci]['type'] == "Integer" or colsp[ci]['type'] == "Float":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["array_valids"]['value'].mean(),2))
                elif colsp[ci]['type'] == "Datetime" or colsp[ci]['type'] == "Date" or colsp[ci]['type'] == "Time":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["array_valids"]['value'].max())
                else:
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5])

            print ("ci", ci, "cspis", cspis)

            if len(colspi) > 1:
                # do levels of split from 1 on (0 is done)
                for level in range(1, len(colspi)):
                    print("level", level)
                    cspis = ",".join([str(colspi[l]) for l in range(level+1)])
                    print("cspis", cspis)
                    cspisp = ",".join([str(colspi[l]) for l in range(level)])
                    print("cspisp", cspisp)

                    cspi = colspi[level]

                    #print(colsps)
                    colsp[ci]['split'][cspis] = {}
                    for cat in colsp[cspi]['cats']:
                        #print(cat, colsp[ci]['split'][cspis][cat][:5])
                        maxx = len(colsp[cspi]['cats'][cat])
                        print("col, cat, len", colsp[cspi]['name'], cat, len(colsp[cspi]['cats'][cat]))
                        for catp in colsp[ci]['split'][cspisp]:
                            ind = 0
                            filterr = []
                            print("catp, len", catp, len(colsp[ci]['split'][cspisp][catp]))
                            for i in colsp[ci]['split'][cspisp][catp]:
                                if i[0] >= colsp[cspi]['cats'][cat][ind]:
                                    while i[0] > colsp[cspi]['cats'][cat][ind]:
                                        ind += 1
                                        if ind >= maxx: break
                                    if ind >= maxx: break
                                    if i[0] == colsp[cspi]['cats'][cat][ind]:
                                        filterr.append(True)
                                    else:
                                        filterr.append(False)
                                    ind += 1
                                else:
                                    filterr.append(False)
                                if ind >= maxx: break
                            for i in range(len(colsp[ci]['split'][cspisp][catp])-len(filterr)):
                                filterr.append(False)
                            #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                            catn = catp + " - " + cat   # change " - " to user option
                            print("cspis", cspis, "catn", catn)
                            colsp[ci]['split'][cspis][catn] = colsp[ci]['split'][cspisp][catp][filterr]
                            '''
                            if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float":
                                print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["av"]['value'].mean(),2))
                            elif colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time":
                                print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["av"]['value'].max())
                            else:
                                print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5])
                            '''

    return colsp


def data_profile(data, columns, variables, colsp, rowsi, colsi, purge = False):
    #global data, variables, colsp
    #import numpy as np

    proc_old = 0
    nrows = len(rowsi)
    ncols = len(colsi)

    #print("Len rowsi", len(rowsi))
    #colsp = {}
    for i, ci in enumerate(colsi):
        colsp[ci] = {}
        rv = []
        mv = []
        rn = []
        colsp[ci]["name"] = columns[ci-1]
        colsp[ci]['split'] = {} #use in data_split
        colsp[ci]["type"] = "Integer"
        colsp[ci]["class"] = None
        colsp[ci]["fnq"] = None

        for ri, row in enumerate(rowsi):
            if data[ri][ci-1] is not None:
                a = data[ri][ci-1]
                #if colsp[ci]['v'] == 1: print(colsp[ci]['name'], a, a.__class__)
                if isinstance (a, int):
                    if len(rv) == 0:
                        colsp[ci]["type"] = "Integer"
                elif isinstance (a, float):
                    if len(rv) == 0:
                        colsp[ci]["type"] = "Float"
                elif isinstance (a, datetime.datetime):
                    if len(rv) == 0:
                        colsp[ci]["type"] = "Datetime"
                elif isinstance (a, datetime.date):
                    if len(rv) == 0:
                        colsp[ci]["type"] = "Date"
                elif isinstance (a, datetime.time):
                    if len(rv) == 0:
                        colsp[ci]["type"] = "Time"
                elif isinstance (a, datetime.timedelta):
                    a = datetime.datetime.strptime(str(datetime.datetime.min + data[ri][ci-1])[11:], variables["$time"]["user"]["value"]).time()
                    if len(rv) == 0:
                        colsp[ci]["type"] = "Time"
                else:
                    if colsp[ci]["type"] == "Float":
                        try:
                            if variables["$decimal_separator"]["user"]["value"] != ".": a = a.replace(variables["$decimal_separator"]["user"]["value"], '.')
                            if variables["$thousands_separator"]["user"]["value"] in a: a = a.replace(variables["$thousands_separator"]["user"]["value"], '')
                            a = float(a)
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["type"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]
                    elif colsp[ci]["type"] == "Integer":
                        try:
                            if variables["$decimal_separator"]["user"]["value"] != ".": a = a.replace(variables["$decimal_separator"]["user"]["value"], '.')
                            if variables["$thousands_separator"]["user"]["value"] in a: a = a.replace(variables["$thousands_separator"]["user"]["value"], '')
                            a = float(a)
                            if a == int(a):
                                a = int(a)  # check other way???
                            else:
                                colsp[ci]["type"] = "Float"
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["type"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]

                    if len(rv) == 0 and colsp[ci]["type"] == "Categorical":
                        # try parse date firsttime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$datetime"]["user"]["value"])
                            #print("Datime firsttime:", a)
                            colsp[ci]["type"] = "Datetime"
                            colsp[ci]['fnq'] = None
                        except Exception as e:
                            #traceback.print_exc()
                            try:
                                a = datetime.datetime.strptime(data[ri][ci-1], variables["$date"]["user"]["value"]).date()
                                #print("Datime firsttime:", a)
                                colsp[ci]["type"] = "Date"
                                colsp[ci]['fnq'] = None
                            except Exception as e:
                                #traceback.print_exc()
                                try:
                                    a = datetime.datetime.strptime(data[ri][ci-1], variables["$time"]["user"]["value"]).time()
                                    #print("Datime firsttime:", a.hour, a.minute, a.second)
                                    #a = datetime.timedelta(days = 0, hours = a.hour, minutes = a.minute, seconds = a.second)
                                    colsp[ci]["type"] = "Time"
                                    colsp[ci]['fnq'] = None
                                except Exception as e:
                                    #traceback.print_exc()
                                    pass

                    if len(rv) > 0 and colsp[ci]["type"] == "Datetime":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$datetime"]["user"]["value"])
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["type"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]
                    elif len(rv) > 0 and colsp[ci]["type"] == "Date":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$date"]["user"]["value"]).date()
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["type"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]
                    elif len(rv) > 0 and colsp[ci]["type"] == "Time":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$time"]["user"]["value"]).time()
                            #print("Datime:", a)
                            #a = datetime.timedelta(days = 0, hours = a.hour, minutes = a.minute, seconds = a.second)
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["type"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]

                if purge and data[ri][ci-1] != a:
                    if isinstance(data[ri], tuple): data[ri] = list(data[ri])
                    data[ri][ci-1] = a

                if len(rv) == 0:
                    colsp[ci]["class"] = type(data[ri][ci-1])
                elif colsp[ci]["class"] is not None:
                    if colsp[ci]["class"] != type(data[ri][ci-1]): colsp[ci]["class"] = None

                rv.append(row)
                mv.append(a)

            else:
                #count None
                rn.append(row)
                #colsp[ci]['n'] += 1

            #if order == maxorder:
            proc = int((i*nrows + ri)/(len(colsi)*nrows)*100)
            if proc > proc_old:
                sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
                sys.stdout.flush()
                proc_old = proc

        a = np.array(rv)
        b = np.array(mv)
        c = np.array(rn)
        d = np.empty(len(rn))
        #colsp[ci]["av"] = rfn.merge_arrays((A, B))
        colsp[ci]["array_valids"] = np.rec.fromarrays((a, b), names=('row', 'value'))
        colsp[ci]["array_nones"] = np.rec.fromarrays((c, d), names=('row', 'value'))
        #colsp[ci]["fnq"] = fnq
        #colsp[ci]["type"] = t
        #colsp[ci]["class"] = cl

        if len(colsp[ci]["array_valids"]) == 0: colsp[ci]["type"] = None   #"Categorical"???

        # same as in data_profile_mp, can copy be
        colsp[ci]["all"] = len(colsp[ci]["array_valids"]) + len(colsp[ci]["array_nones"])
        colsp[ci]["valid"] = len(colsp[ci]["array_valids"])
        colsp[ci]["none"] = len(colsp[ci]["array_nones"])

        colsp[ci]["unique"] = None
        colsp[ci]["categ_counts"] = None
        try:
            uv, uc = np.unique(colsp[ci]["array_valids"]['value'], return_counts=True)
        except Exception as e:
            #traceback.print_exc()
            #TypeError: '<' not supported between instances of 'str' and 'datetime.date'
            variables["$printRed"]["options"]["value"](f'''Mixed format detected in '{colsp[ci]["name"]}'. Check results carefully!''')
            uvd = {}    # calculate unique value dict with string cats only
            for val in colsp[ci]["array_valids"]['value']:
                if uvd.get(str(val)) is not None:
                    uvd[str(val)] += 1
                else:
                    uvd[str(val)] = 1
            uv = np.array(list(uvd.keys()))
            uc = np.array(list(uvd.values()))
            #print(uv, uc)
        finally:
            colsp[ci]["unique"] = len(uv)
            #print(colsp[ci]["name"])
            colsp[ci]["categ_counts"] = None
            if colsp[ci]["unique"] > 0:
                # only one category us minimal => probably bonominal ditribution, keep all cats
                uvp = uv[uc != min(uc)]
                if colsp[ci]["unique"] > variables["$profile_show_categorical"]["options"]["value"]:
                    ucp = uc[uc != min(uc)]
                else:
                    uvp = uv
                    ucp = uc
                # if 0 cats or max count is the same as min count, there are no modes
                if len(uvp) > 0:
                    colsp[ci]["categ_counts"] = np.flip(np.sort(np.rec.fromarrays((uvp, ucp), names=('value', 'count')), order = "count"))[:variables["$profile_show_categorical"]["options"]["value"]]
            #count_sort_ind = np.argsort(-count)
            #u[count_sort_ind]
            #print(cc)

        colsp[ci]["min"] = None
        colsp[ci]["max"] = None
        colsp[ci]["range"] = None
        colsp[ci]["sum"] = None
        colsp[ci]["mean"] = None
        colsp[ci]["q1"] = None
        colsp[ci]["q2"] = None
        colsp[ci]["q3"] = None
        colsp[ci]["iqr"] = None
        colsp[ci]["smd2"] = 0
        colsp[ci]["smd3"] = 0
        colsp[ci]["var"] = None
        colsp[ci]["std"] = None
        colsp[ci]["skew"] = None
        if colsp[ci]["type"] == "Integer" or colsp[ci]["type"] == "Float" or colsp[ci]["type"] == "Datetime" or colsp[ci]["type"] == "Date" or colsp[ci]["type"] == "Time":
            colsp[ci]["min"] = colsp[ci]["array_valids"]['value'].min()
            colsp[ci]["max"] = colsp[ci]["array_valids"]['value'].max()
        if colsp[ci]["type"] == "Integer" or colsp[ci]["type"] == "Float":
            colsp[ci]["range"] = colsp[ci]["max"] - colsp[ci]["min"]
            if colsp[ci]["type"] == "Integer":
                colsp[ci]["sum"] = colsp[ci]["array_valids"]['value'].sum(dtype=np.int64)
            else:
                colsp[ci]["sum"] = colsp[ci]["array_valids"]['value'].sum(dtype=np.float64)
            colsp[ci]["mean"] = colsp[ci]['array_valids']['value'].mean()
            lenc = len(colsp[ci]['array_valids'])
            if lenc > 0:
                #print(ci, sorted(colsp[ci]['m']))
                m = sorted(colsp[ci]['array_valids']["value"])
                if lenc >= 1 and lenc % 2:
                    colsp[ci]["q2"] = m[int((lenc+1)/2)-1]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]["q2"] = (m[int(lenc/2)-1] + m[int(lenc/2)])/2    #mean of mid cases
            lenc = int(len(m)/2)
            if lenc > 0:
                #print(ci, sorted(colsp[ci]['m']))
                #colsp[ci]['m'] = sorted(colsp[ci]['m'])
                if lenc >= 1 and lenc % 2:
                    colsp[ci]["q1"] = m[int((lenc+1)/2)-1]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]["q1"] = (m[int(lenc/2)-1] + m[int(lenc/2)])/2    #mean of mid cases
                if lenc >= 1 and lenc % 2:
                    colsp[ci]["q3"] = m[-1*int((lenc+1)/2)]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]["q3"] = (m[-1*int(lenc/2)] + m[-1*(int(lenc/2))-1])/2    #mean of mid cases
                colsp[ci]["iqr"] = colsp[ci]["q3"] - colsp[ci]["q1"]
            for mi in m:
                colsp[ci]["smd2"] += (mi - colsp[ci]["mean"])**2
                colsp[ci]["smd3"] += (mi - colsp[ci]["mean"])**3
            if colsp[ci]["valid"] > 0:
                colsp[ci]["var"] = colsp[ci]["smd2"] / colsp[ci]["valid"]
                colsp[ci]["std"] = (colsp[ci]["smd2"] / colsp[ci]["valid"])**0.5
            if colsp[ci]["valid"] > 0 and colsp[ci]["smd2"] > 0:
                colsp[ci]["skew"] = colsp[ci]["smd3"] / (colsp[ci]["valid"] * (colsp[ci]["smd2"] / colsp[ci]["valid"])**1.5)

        #print(colsp[ci]["name"], len(colsp[ci]["array_valids"]), colsp[ci]["type"], colsp[ci]["class"])

    proc = 100
    sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
    sys.stdout.flush()

    #print(colsp)
    return data, colsp


def data_profile_prep_mp(inn):

    #not direct copy from data_profile!!! only part colsp, final is constructed later
    data, rowsi, colsi, variables, order, maxorder = inn[0], inn[1], inn[2], inn[3], inn[4], inn[5]
    #global variables
    #print("Len rowsi", len(rowsi))
    colsp = {}
    for ci in colsi:
        colsp[ci] = {}
        colsp[ci]["rv"] = []
        colsp[ci]["mv"] = []
        colsp[ci]["rn"] = []
        colsp[ci]["t"] = "Integer"
        colsp[ci]["cl"] = None
        colsp[ci]["fnq"] = None

    for ri, row in enumerate(rowsi):
        for ci in colsi:
            if data[ri][ci-1] is not None:
                a = data[ri][ci-1]
                #if colsp[ci]['v'] == 1: print(colsp[ci]['name'], a, a.__class__)
                if isinstance (a, int):
                    if len(colsp[ci]["rv"]) == 0:
                        colsp[ci]["t"] = "Integer"
                elif isinstance (a, float):
                    if len(colsp[ci]["rv"]) == 0:
                        colsp[ci]["t"] = "Float"
                elif isinstance (a, datetime.datetime):
                    if len(colsp[ci]["rv"]) == 0:
                        colsp[ci]["t"] = "Datetime"
                elif isinstance (a, datetime.date):
                    if len(colsp[ci]["rv"]) == 0:
                        colsp[ci]["t"] = "Date"
                elif isinstance (a, datetime.time):
                    if len(colsp[ci]["rv"]) == 0:
                        colsp[ci]["t"] = "Time"
                elif isinstance (a, datetime.timedelta):
                    a = datetime.datetime.strptime(str(datetime.datetime.min + data[ri][ci-1])[11:], variables["$time"]["user"]["value"]).time()
                    if len(colsp[ci]["rv"]) == 0:
                        colsp[ci]["t"] = "Time"
                else:
                    if colsp[ci]["t"] == "Float":
                        try:
                            if variables["$decimal_separator"]["user"]["value"] != ".": a = a.replace(variables["$decimal_separator"]["user"]["value"], '.')
                            if variables["$thousands_separator"]["user"]["value"] in a: a = a.replace(variables["$thousands_separator"]["user"]["value"], '')
                            a = float(a)
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["t"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]
                    elif colsp[ci]["t"] == "Integer":
                        try:
                            if variables["$decimal_separator"]["user"]["value"] != ".": a = a.replace(variables["$decimal_separator"]["user"]["value"], '.')
                            if variables["$thousands_separator"]["user"]["value"] in a: a = a.replace(variables["$thousands_separator"]["user"]["value"], '')
                            a = float(a)
                            if a == int(a):
                                a = int(a)  # check other way???
                            else:
                                colsp[ci]["t"] = "Float"
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["t"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]

                    if len(colsp[ci]["rv"]) == 0 and colsp[ci]["t"] == "Categorical":
                        # try parse date firsttime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$datetime"]["user"]["value"])
                            #print("Datime firsttime:", a)
                            colsp[ci]["t"] = "Datetime"
                            colsp[ci]['fnq'] = None
                        except Exception as e:
                            #traceback.print_exc()
                            try:
                                a = datetime.datetime.strptime(data[ri][ci-1], variables["$date"]["user"]["value"]).date()
                                #print("Datime firsttime:", a)
                                colsp[ci]["t"] = "Date"
                                colsp[ci]['fnq'] = None
                            except Exception as e:
                                #traceback.print_exc()
                                try:
                                    a = datetime.datetime.strptime(data[ri][ci-1], variables["$time"]["user"]["value"]).time()
                                    #print("Datime firsttime:", a.hour, a.minute, a.second)
                                    #a = datetime.timedelta(days = 0, hours = a.hour, minutes = a.minute, seconds = a.second)
                                    colsp[ci]["t"] = "Time"
                                    colsp[ci]['fnq'] = None
                                except Exception as e:
                                    #traceback.print_exc()
                                    pass

                    if len(colsp[ci]["rv"]) > 0 and colsp[ci]["t"] == "Datetime":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$datetime"]["user"]["value"])
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["t"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]
                    elif len(colsp[ci]["rv"]) > 0 and colsp[ci]["t"] == "Date":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$date"]["user"]["value"]).date()
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["t"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]
                    elif len(colsp[ci]["rv"]) > 0 and colsp[ci]["t"] == "Time":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri][ci-1], variables["$time"]["user"]["value"]).time()
                            #print("Datime:", a)
                            #a = datetime.timedelta(days = 0, hours = a.hour, minutes = a.minute, seconds = a.second)
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]["t"] = "Categorical"
                            if colsp[ci]["fnq"] is None: colsp[ci]["fnq"] = data[ri][ci-1]

                '''
                if purge and data[ri][ci-1] != a:
                    if isinstance(data[ri], tuple): data[ri] = list(data[ri])
                    data[ri][ci-1] = a
                '''

                if len(colsp[ci]["rv"]) == 0:
                    colsp[ci]["cl"] = type(data[ri][ci-1])
                elif colsp[ci]["cl"] is not None:
                    if colsp[ci]["cl"] != type(data[ri][ci-1]): colsp[ci]["cl"] = None

                colsp[ci]["rv"].append(row)
                colsp[ci]["mv"].append(a)

            else:
                #count None
                colsp[ci]["rn"].append(row)
                #colsp[ci]['n'] += 1

        if order == maxorder:
            proc = int(ri/len(rowsi)*100)
            sys.stdout.write(u"\u001b[1000D" +  "Data prepare processed: " + str(proc) + "% ")
            sys.stdout.flush()

    if order == maxorder:
        proc = 100
        sys.stdout.write(u"\u001b[1000D" +  "Data prepare processed: " + str(proc) + "% ")
        sys.stdout.flush()

    #print(colsp)
    return colsp, order


def data_profile_mp(inn):
    colsp = {}
    ci = 0
    colsp[ci], cir, variables, i, imax = inn[0], inn[1], inn[2], inn[3], inn[4]

    RED, END = '\033[91m', '\033[0m'
    printRed = lambda sTxt: print(RED + sTxt + END)

    # copied from data_profile
    colsp[ci]["all"] = len(colsp[ci]["array_valids"]) + len(colsp[ci]["array_nones"])
    colsp[ci]["valid"] = len(colsp[ci]["array_valids"])
    colsp[ci]["none"] = len(colsp[ci]["array_nones"])

    colsp[ci]["unique"] = None
    colsp[ci]["categ_counts"] = None
    try:
        uv, uc = np.unique(colsp[ci]["array_valids"]['value'], return_counts=True)
    except Exception as e:
        #traceback.print_exc()
        #TypeError: '<' not supported between instances of 'str' and 'datetime.date'
        printRed(f'''Mixed format detected in '{colsp[ci]["name"]}'. Check results carefully!''')
        uvd = {}    # calculate unique value dict with string cats only
        for val in colsp[ci]["array_valids"]['value']:
            if uvd.get(str(val)) is not None:
                uvd[str(val)] += 1
            else:
                uvd[str(val)] = 1
        uv = np.array(list(uvd.keys()))
        uc = np.array(list(uvd.values()))
        #print(uv, uc)
    finally:
        colsp[ci]["unique"] = len(uv)
        #print(colsp[ci]["name"])
        colsp[ci]["categ_counts"] = None
        if colsp[ci]["unique"] > 0:
            # only one category us minimal => probably bonominal ditribution, keep all cats
            uvp = uv[uc != min(uc)]
            if colsp[ci]["unique"] > variables["$profile_show_categorical"]["options"]["value"]:
                ucp = uc[uc != min(uc)]
            else:
                uvp = uv
                ucp = uc
            # if 0 cats or max count is the same as min count, there are no modes
            if len(uvp) > 0:
                colsp[ci]["categ_counts"] = np.flip(np.sort(np.rec.fromarrays((uvp, ucp), names=('value', 'count')), order = "count"))[:variables["$profile_show_categorical"]["options"]["value"]]
        #count_sort_ind = np.argsort(-count)
        #u[count_sort_ind]
        #print(cc)

    colsp[ci]["min"] = None
    colsp[ci]["max"] = None
    colsp[ci]["range"] = None
    colsp[ci]["sum"] = None
    colsp[ci]["mean"] = None
    colsp[ci]["q1"] = None
    colsp[ci]["q2"] = None
    colsp[ci]["q3"] = None
    colsp[ci]["iqr"] = None
    colsp[ci]["smd2"] = 0
    colsp[ci]["smd3"] = 0
    colsp[ci]["var"] = None
    colsp[ci]["std"] = None
    colsp[ci]["skew"] = None
    if colsp[ci]["type"] == "Integer" or colsp[ci]["type"] == "Float" or colsp[ci]["type"] == "Datetime" or colsp[ci]["type"] == "Date" or colsp[ci]["type"] == "Time":
        colsp[ci]["min"] = colsp[ci]["array_valids"]['value'].min()
        colsp[ci]["max"] = colsp[ci]["array_valids"]['value'].max()
    if colsp[ci]["type"] == "Integer" or colsp[ci]["type"] == "Float":
        colsp[ci]["range"] = colsp[ci]["max"] - colsp[ci]["min"]
        if colsp[ci]["type"] == "Integer":
            colsp[ci]["sum"] = colsp[ci]["array_valids"]['value'].sum(dtype=np.int64)
        else:
            colsp[ci]["sum"] = colsp[ci]["array_valids"]['value'].sum(dtype=np.float64)
        colsp[ci]["mean"] = colsp[ci]['array_valids']['value'].mean()
        lenc = len(colsp[ci]['array_valids'])
        if lenc > 0:
            #print(ci, sorted(colsp[ci]['m']))
            m = sorted(colsp[ci]['array_valids']["value"])
            if lenc >= 1 and lenc % 2:
                colsp[ci]["q2"] = m[int((lenc+1)/2)-1]
            if lenc >= 2 and (lenc % 2) == 0:
                colsp[ci]["q2"] = (m[int(lenc/2)-1] + m[int(lenc/2)])/2    #mean of mid cases
        lenc = int(len(m)/2)
        if lenc > 0:
            #print(ci, sorted(colsp[ci]['m']))
            #colsp[ci]['m'] = sorted(colsp[ci]['m'])
            if lenc >= 1 and lenc % 2:
                colsp[ci]["q1"] = m[int((lenc+1)/2)-1]
            if lenc >= 2 and (lenc % 2) == 0:
                colsp[ci]["q1"] = (m[int(lenc/2)-1] + m[int(lenc/2)])/2    #mean of mid cases
            if lenc >= 1 and lenc % 2:
                colsp[ci]["q3"] = m[-1*int((lenc+1)/2)]
            if lenc >= 2 and (lenc % 2) == 0:
                colsp[ci]["q3"] = (m[-1*int(lenc/2)] + m[-1*(int(lenc/2))-1])/2    #mean of mid cases
            colsp[ci]["iqr"] = colsp[ci]["q3"] - colsp[ci]["q1"]
        for mi in m:
            colsp[ci]["smd2"] += (mi - colsp[ci]["mean"])**2
            colsp[ci]["smd3"] += (mi - colsp[ci]["mean"])**3
        if colsp[ci]["valid"] > 0:
            colsp[ci]["var"] = colsp[ci]["smd2"] / colsp[ci]["valid"]
            colsp[ci]["std"] = (colsp[ci]["smd2"] / colsp[ci]["valid"])**0.5
        if colsp[ci]["valid"] > 0 and colsp[ci]["smd2"] > 0:
            colsp[ci]["skew"] = colsp[ci]["smd3"] / (colsp[ci]["valid"] * (colsp[ci]["smd2"] / colsp[ci]["valid"])**1.5)

    proc = int(i/imax*100)
    sys.stdout.write(u"\u001b[1000D" +  "Data profile processed: " + str(proc) + "% ")
    sys.stdout.flush()

    return colsp[ci], cir


def data_profile_old(rowsi, colsi, purge = False):
    global variables
    #print("Len rowsi", len(rowsi))
    nrows = len(data)
    ncols = len(columns)
    for ci in colsi:
        colsp[ci] = {}
        colsp[ci]['name'] = columns[ci-1]
        colsp[ci]['split'] = {}
        colsp[ci]['w'] = 0
        #colsp[columns[ci-1]]['t'] = "Categorical"
        #colsp[ci]['t'] = "Quantitative"
        colsp[ci]['t'] = "Integer"
        #colsp[ci]['qt'] = "Int"
        colsp[ci]['cl'] = None
        colsp[ci]['fnq'] = None
        colsp[ci]['n'] = 0
        colsp[ci]['v'] = 0
        colsp[ci]['c'] = {}
        colsp[ci]['sum'] = 0
        colsp[ci]['r'] = []
        colsp[ci]['m'] = []
        colsp[ci]['q1'] = None
        colsp[ci]['q2'] = None
        colsp[ci]['q3'] = None
        colsp[ci]['smd2'] = 0
        colsp[ci]['smd3'] = 0
    for ri in rowsi:
        for ci in colsi:
            w = len(str(data[ri-1][ci-1]))
            if w > colsp[ci]['w']: colsp[ci]['w'] = w
            if data[ri-1][ci-1] is not None:
                colsp[ci]['v'] += 1
                a = data[ri-1][ci-1]
                #if colsp[ci]['v'] == 1: print(colsp[ci]['name'], a, a.__class__)
                if isinstance (a, int):
                    if colsp[ci]['v'] == 1:
                        colsp[ci]['min'] = a
                        colsp[ci]['max'] = a
                        colsp[ci]['t'] = "Integer"
                        #colsp[ci]['qt'] = "Int"
                    elif a < colsp[ci]['min']:
                        colsp[ci]['min'] = a
                    elif a > colsp[ci]['max']:
                        colsp[ci]['max'] = a
                    colsp[ci]['sum'] += a
                    #colsp[ci]['m'].append(a)
                elif isinstance (a, float):
                    if colsp[ci]['v'] == 1:
                        colsp[ci]['min'] = a
                        colsp[ci]['max'] = a
                        colsp[ci]['t'] = "Float"
                        #colsp[ci]['qt'] = "Float"
                    elif a < colsp[ci]['min']:
                        colsp[ci]['min'] = a
                    elif a > colsp[ci]['max']:
                        colsp[ci]['max'] = a
                    colsp[ci]['sum'] += a
                    #colsp[ci]['m'].append(a)
                elif isinstance (a, datetime.datetime):
                    if colsp[ci]['v'] == 1:
                        colsp[ci]['min'] = a
                        colsp[ci]['max'] = a
                        colsp[ci]['t'] = "Datetime"
                    elif a < colsp[ci]['min']:
                        colsp[ci]['min'] = a
                    elif a > colsp[ci]['max']:
                        colsp[ci]['max'] = a
                elif isinstance (a, datetime.date):
                    if colsp[ci]['v'] == 1:
                        colsp[ci]['min'] = a
                        colsp[ci]['max'] = a
                        colsp[ci]['t'] = "Date"
                    elif a < colsp[ci]['min']:
                        colsp[ci]['min'] = a
                    elif a > colsp[ci]['max']:
                        colsp[ci]['max'] = a
                elif isinstance (a, datetime.time):
                    if colsp[ci]['v'] == 1:
                        colsp[ci]['min'] = a
                        colsp[ci]['max'] = a
                        colsp[ci]['t'] = "Time"
                    elif a < colsp[ci]['min']:
                        colsp[ci]['min'] = a
                    elif a > colsp[ci]['max']:
                        colsp[ci]['max'] = a
                elif isinstance (a, datetime.timedelta):
                    a = datetime.datetime.strptime(str(datetime.datetime.min + data[ri-1][ci-1])[11:], variables["$time"]["user"]["value"]).time()
                    if colsp[ci]['v'] == 1:
                        colsp[ci]['min'] = a
                        colsp[ci]['max'] = a
                        colsp[ci]['t'] = "Time"
                    elif a < colsp[ci]['min']:
                        colsp[ci]['min'] = a
                    elif a > colsp[ci]['max']:
                        colsp[ci]['max'] = a
                else:
                    if colsp[ci]['t'] == "Float":
                        try:
                            if variables["$decimal_separator"]["user"]["value"] != ".": a = a.replace(variables["$decimal_separator"]["user"]["value"], '.')
                            if variables["$thousands_separator"]["user"]["value"] in a: a = a.replace(variables["$thousands_separator"]["user"]["value"], '')
                            a = float(a)
                            if colsp[ci]['v'] == 1:
                                colsp[ci]['min'] = a
                                colsp[ci]['max'] = a
                            elif a < colsp[ci]['min']:
                                colsp[ci]['min'] = a
                            elif a > colsp[ci]['max']:
                                colsp[ci]['max'] = a
                            colsp[ci]['sum'] += a
                            #colsp[ci]['m'].append(a)
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]['t'] = "Categorical"
                            if colsp[ci]['fnq'] is None:
                                colsp[ci]['fnq'] = data[ri-1][ci-1]
                    elif colsp[ci]['t'] == "Integer":
                        try:
                            if variables["$decimal_separator"]["user"]["value"] != ".": a = a.replace(variables["$decimal_separator"]["user"]["value"], '.')
                            if variables["$thousands_separator"]["user"]["value"] in a: a = a.replace(variables["$thousands_separator"]["user"]["value"], '')
                            a = float(a)
                            if a == int(a):
                                a = int(a)  # check other way???
                            else:
                                colsp[ci]['t'] = "Float"
                            #print(a)
                            if colsp[ci]['v'] == 1:
                                colsp[ci]['min'] = a
                                colsp[ci]['max'] = a
                            elif a < colsp[ci]['min']:
                                colsp[ci]['min'] = a
                            elif a > colsp[ci]['max']:
                                colsp[ci]['max'] = a
                            colsp[ci]['sum'] += a
                            #colsp[ci]['m'].append(a)
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]['t'] = "Categorical"
                            if colsp[ci]['fnq'] is None:
                                colsp[ci]['fnq'] = data[ri-1][ci-1]

                    if colsp[ci]['v'] == 1 and colsp[ci]['t'] == "Categorical":
                        # try parse date firsttime
                        try:
                            a = datetime.datetime.strptime(data[ri-1][ci-1], variables["$datetime"]["user"]["value"])
                            #print("Datime firsttime:", a)
                            colsp[ci]['t'] = "Datetime"
                            colsp[ci]['min'] = a
                            colsp[ci]['max'] = a
                            colsp[ci]['fnq'] = None
                        except Exception as e:
                            #traceback.print_exc()
                            try:
                                a = datetime.datetime.strptime(data[ri-1][ci-1], variables["$date"]["user"]["value"]).date()
                                #print("Datime firsttime:", a)
                                colsp[ci]['t'] = "Date"
                                colsp[ci]['min'] = a
                                colsp[ci]['max'] = a
                                colsp[ci]['fnq'] = None
                            except Exception as e:
                                #traceback.print_exc()
                                try:
                                    a = datetime.datetime.strptime(data[ri-1][ci-1], variables["$time"]["user"]["value"]).time()
                                    #print("Datime firsttime:", a.hour, a.minute, a.second)
                                    #a = datetime.timedelta(days = 0, hours = a.hour, minutes = a.minute, seconds = a.second)
                                    colsp[ci]['t'] = "Time"
                                    colsp[ci]['min'] = a
                                    colsp[ci]['max'] = a
                                    colsp[ci]['fnq'] = None
                                except Exception as e:
                                    #traceback.print_exc()
                                    pass

                    if colsp[ci]['v'] > 1 and colsp[ci]['t'] == "Datetime":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri-1][ci-1], variables["$datetime"]["user"]["value"])
                            #print("Datime:", a)
                            if a < colsp[ci]['min']:
                                colsp[ci]['min'] = a
                            elif a > colsp[ci]['max']:
                                colsp[ci]['max'] = a
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]['t'] = "Categorical"
                            if colsp[ci]['fnq'] is None:
                                colsp[ci]['fnq'] = data[ri-1][ci-1]
                    elif colsp[ci]['v'] > 1 and colsp[ci]['t'] == "Date":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri-1][ci-1], variables["$date"]["user"]["value"]).date()
                            #print("Datime:", a)
                            if a < colsp[ci]['min']:
                                colsp[ci]['min'] = a
                            elif a > colsp[ci]['max']:
                                colsp[ci]['max'] = a
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]['t'] = "Categorical"
                            if colsp[ci]['fnq'] is None:
                                colsp[ci]['fnq'] = data[ri-1][ci-1]
                    elif colsp[ci]['v'] > 1 and colsp[ci]['t'] == "Time":
                        #datetime
                        try:
                            a = datetime.datetime.strptime(data[ri-1][ci-1], variables["$time"]["user"]["value"]).time()
                            #print("Datime:", a)
                            #a = datetime.timedelta(days = 0, hours = a.hour, minutes = a.minute, seconds = a.second)
                            if a < colsp[ci]['min']:
                                colsp[ci]['min'] = a
                            elif a > colsp[ci]['max']:
                                colsp[ci]['max'] = a
                        except Exception as e:
                            #traceback.print_exc()
                            colsp[ci]['t'] = "Categorical"
                            if colsp[ci]['fnq'] is None:
                                colsp[ci]['fnq'] = data[ri-1][ci-1]

                if purge and data[ri-1][ci-1] != a:
                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                    data[ri-1][ci-1] = a

                colsp[ci]['r'].append(ri)
                colsp[ci]['m'].append(a)

                if colsp[ci]['v'] == 1:
                    colsp[ci]['cl'] = type(data[ri-1][ci-1])
                elif colsp[ci]['cl'] is not None:
                    if colsp[ci]['cl'] != type(data[ri-1][ci-1]): colsp[ci]['cl'] = None

                if data[ri-1][ci-1] not in colsp[ci]['c']:
                    colsp[ci]['c'][data[ri-1][ci-1]] = 1
                else:
                    colsp[ci]['c'][data[ri-1][ci-1]] += 1
            else:
                #count None
                colsp[ci]['n'] += 1
        proc = int(ri/len(rowsi)*90)
        sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
        sys.stdout.flush()

    for ci in colsi:
        a = np.array(colsp[ci]["r"])
        b = np.array(colsp[ci]["m"])
        #colsp[ci]["av"] = rfn.merge_arrays((A, B))
        colsp[ci]["av"] = np.rec.fromarrays((a, b), names=('row', 'value'))
        #print(colsp[ci]["av"][:5])
        if colsp[ci]['v'] > 0 and (colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float"):
            colsp[ci]['mean'] = colsp[ci]['sum'] / colsp[ci]['v']
            lenc = len(colsp[ci]['m'])
            if lenc > 0:
                #print(ci, sorted(colsp[ci]['m']))
                colsp[ci]['m'] = sorted(colsp[ci]['m'])
                if lenc >= 1 and lenc % 2:
                    colsp[ci]['q2'] = colsp[ci]['m'][int((lenc+1)/2)-1]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]['q2'] = (colsp[ci]['m'][int(lenc/2)-1] + colsp[ci]['m'][int(lenc/2)])/2    #mean of mid cases
            lenc = int(len(colsp[ci]['m'])/2)
            if lenc > 0:
                #print(ci, sorted(colsp[ci]['m']))
                #colsp[ci]['m'] = sorted(colsp[ci]['m'])
                if lenc >= 1 and lenc % 2:
                    colsp[ci]['q1'] = colsp[ci]['m'][int((lenc+1)/2)-1]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]['q1'] = (colsp[ci]['m'][int(lenc/2)-1] + colsp[ci]['m'][int(lenc/2)])/2    #mean of mid cases
                if lenc >= 1 and lenc % 2:
                    colsp[ci]['q3'] = colsp[ci]['m'][-1*int((lenc+1)/2)]
                if lenc >= 2 and (lenc % 2) == 0:
                    colsp[ci]['q3'] = (colsp[ci]['m'][-1*int(lenc/2)] + colsp[ci]['m'][-1*(int(lenc/2))-1])/2    #mean of mid cases
            for i in colsp[ci]['m']:
                colsp[ci]['smd2'] += (i - colsp[ci]['mean'])**2
                colsp[ci]['smd3'] += (i - colsp[ci]['mean'])**3
        elif colsp[ci]['v'] > 0 and (colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time"):
            #colsp[ci]['qt'] = None
            colsp[ci]['sum'] = None
            colsp[ci]['mean'] = None
            colsp[ci]['q1'] = None
            colsp[ci]['q2'] = None
            colsp[ci]['q3'] = None
        else:
            colsp[ci]['t'] = "Categorical"
            #colsp[ci]['qt'] = None
            colsp[ci]['min'] = None
            colsp[ci]['max'] = None
            colsp[ci]['sum'] = None
            colsp[ci]['mean'] = None
            colsp[ci]['q1'] = None
            colsp[ci]['q2'] = None
            colsp[ci]['q3'] = None
        if len(colsp[ci]['c']) > 0:
            colsp[ci]['c'] = {k:v for k, v in sorted(colsp[ci]['c'].items(), reverse = True, key = lambda x: x[1])[:profile_max_categorical]}

        proc = int(90+ci/len(colsi)*10)
        sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
        sys.stdout.flush()
        #print(colsp[ci]['name'], colsp[ci]['qt'], colsp[ci]['v'])

    print("\nQuantitative:", [colsp[ci]['name'] for ci in colsi if colsp[ci]['t'] == "Quantitative"])
    variables["$columns_quantitative"] = {}
    variables["$columns_quantitative"]["shorts"] = ["$columns_quant","$cq"]
    variables["$columns_quantitative"]["data"] = {}
    variables["$columns_quantitative"]["data"]["value"] = [colsp[ci]['name'] for ci in colsi if colsp[ci]['t'] == "Quantitative"]
    variables["$columns_quantitative"]["data"]["print"] = {}
    variables["$columns_quantitative"]["data"]["print data"] = {}
    variables["$columns_quantitative"]["data"]["print data all"] = {}
    variables["$columns_quantitative"]["data"]["print data easy"] = {}
    variables["$columns_quantitative"]["data"]["data"] = {}
    variables["$columns_quantitative"]["data"]["data select"] = {}
    variables["$columns_quantitative"]["data"]["data select easy"] = {}
    variables["$columns_quantitative"]["data"]["data fill"] = {}
    variables["$columns_quantitative"]["data"]["data fill easy"] = {}

    #print(colsp)
    return colsp



def data_width(rowsi, colsi, data, columns, rows, rows_label):
    #print("Len rowsi", len(rowsi))
    #print("Colsi", colsi)
    #print(data)
    nrows = len(data)
    ncols = len(columns)
    colsp = {}
    colsp[0] = {}
    colsp[0]['name'] = rows_label
    colsp[0]['w'] = len(str(rows_label)) + 1    # Columns 0 is Row number with header '(Row)' = 5 chars
    for ci in colsi:
        colsp[ci] = {}
        colsp[ci]['name'] = columns[ci-1]
        colsp[ci]['w'] = len(columns[ci-1]) + 1
    for ri in rowsi:
        if len(str(rows[ri-1])) >= colsp[0]['w']: colsp[0]['w'] = len(str(rows[ri-1])) +1
        for ci in colsi:
            #print(ri, ci)
            w = len(str(data[ri-1][ci-1]))
            if w >= colsp[ci]['w']: colsp[ci]['w'] = w + 1

    return colsp


def print_data(rowsi, colsi, data, columns, rows, rows_label, variables):
    #print(rows_show)
    colsp = data_width(rowsi, colsi, data, columns, rows, rows_label)
    terminal_resize(colsp)
    #print(row_format)
    #row_format = row_format_l(colsp)
    #print(row_format)
    #print(row_format.format(*[colsp[ci]['name'] for ci in colsp]))
    for ci in colsp:
        screen_max = colsp[ci]['screen']
    screen = 0
    while screen < screen_max:
        #print(row_format)
        colspart = {}
        if screen > 0:
            colspart[0] = colsp[0]
            print("...")
        for ci in colsp:
            if colsp[ci]['screen'] == screen + 1:
                colspart[ci] = colsp[ci]
        row_format = variables["$row_format_l"]["options"]["value"](colspart)
        print(row_format.format(*[colsp[ci]['name'] for ci in colspart]))
        for ri in rowsi:
            #print(row_format.format(profile_rows[i], *[str(col) for col in row if col in colspart]))    # Null to None
            print(row_format.format(str(rows[ri-1]), *[str(col) for ci, col in enumerate(data[ri-1]) if ci+1 in colspart]))    # Null to None
        screen += 1


def show_data(data, columns, variables, show_title = True):
    #global variables
    nrows = len(data)
    variables["$all"]["data"]["value"] = nrows
    variables["$columns_all"]["data"]["value"] = columns

    rows_label = variables["$rows_label"]["options"]["value"]
    ncols = len(columns)
    rows = range(1, nrows + 1)
    colsi = range(1, ncols + 1)
    if nrows <= variables["$show_cases"]["options"]["value"]*2:
        if show_title: variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing all cases with all columns.")
        rowsi = range(1, nrows + 1)
        print_data(rowsi, colsi, data, columns, rows, rows_label, variables)
    else:
        if show_title: variables["$printInvGreen"]["options"]["value"](f'''There are {nrows} rows, {ncols} columns. Printing first / last {variables["$show_cases"]["options"]["value"]} cases with all columns.''')
        data_show = list(data[:variables["$show_cases"]["options"]["value"]])
        #print("Data show",data_show)
        data_show += [["" for c in columns]]
        data_show += data[-variables["$show_cases"]["options"]["value"]:]
        #print("Data show",data_show)
        rows = list(range(1,variables["$show_cases"]["options"]["value"]+1))
        rows += ["..."]
        rows += list(range(nrows-variables["$show_cases"]["options"]["value"]+1, nrows +1))
        #print("Rows:", rows)
        rowsi = range(1, len(data_show) + 1)
        print_data(rowsi, colsi, data_show, columns, rows, rows_label, variables)


def find_columns(colss, columns):
    colsi = []
    for cols in colss:
        is_column = 0
        for i, col in enumerate(columns):
            if col == cols:
                colsi.append(i + 1)
                is_column += 1
        if is_column < 1:
            variables["$printRed"]["options"]["value"](f"Column '{cols}' not in columns!")
            print()
        elif is_column > 1:
            variables["$printRed"]["options"]["value"](f"Multiple columns '{cols}' are in columns!")
            print()
    return colsi



def parseValue(value, typestr):
    dstring = "."
    if typestr == "auto":
        if len(value) > 0:
            if value == 'True':
                value = True
            elif value == 'False':
                value = False
            elif value == 'None':
                value = None
            elif value[0] in ["-","0","1","2","3","4","5","6","7","8","9"] and dstring not in value:
                try:
                    value = int(value)
                except Exception as e:
                    traceback.print_exc()
                variables["$Assert"]["options"]["value"](isinstance(value, int), f"Tried parse int value {value} as {typestr} and failed. Check results carefully!!!")
            elif value[0] in ["-","0","1","2","3","4","5","6","7","8","9",dstring] and dstring in value:
                try:
                    value = float(value)
                except Exception as e:
                    traceback.print_exc()
                variables["$Assert"]["options"]["value"](isinstance(value, float), f"Tried parse float value {value} as {typestr} and failed. Check results carefully!!!")
    return value


def data_fill(variables, data, columns, fill_formats = {}, fill_nones = {}):

    temp_columns = set()
    if fill_formats is not None:
        for colss in fill_formats:
            temp_columns.add(colss)
    if fill_nones is not None:
        for colss in fill_nones:
            temp_columns.add(colss)

    fill_columns = {}
    for colss in temp_columns:
        fill_columns[colss] = {}
        if fill_formats is not None:
            if colss in fill_formats: fill_columns[colss]["fill_format"] = fill_formats[colss]
        if fill_nones is not None:
            if colss in fill_nones: fill_columns[colss]["fill_none"] = fill_nones[colss]

    print("fill_columns", fill_columns)

    ncols = len(fill_columns)
    nrows = len(data)

    if len(fill_columns) > 0:
        for i, colss in enumerate(fill_columns):
            colsi = find_columns([colss], columns)
            ncolsi = len(colsi)
            fill_format = fill_columns[colss].get("fill_format")
            fill_none = fill_columns[colss].get("fill_none")
            if len(colsi) > 0:
                #print(colss, colsi)
                for ri in range(1, len(data) + 1):
                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                    for ci in colsi:
                        # do format of columns ci - 1, fill_columns(colss)
                        #print(colss, columns[ci-1], fill_columns[colss])
                        value = data[ri-1][ci-1]
                        result = None
                        if isinstance(value, str):
                            if (fill_format == "int" or fill_format == "int." or fill_format == "int," \
                            or fill_format == "float" or fill_format == "float." or fill_format == "float," \
                            or fill_format == "auto") and len(value) > 0:
                                rsign = 1
                                rstring = ""
                                dstring = "."
                                if fill_format == "int": dstring = ""
                                if fill_format == "int," or fill_format == "float," or fill_format == "auto,": dstring = ","
                                if fill_format == "auto":
                                    if value[0] in ["-","0","1","2","3","4","5","6","7","8","9"] and dstring not in value:
                                        try:
                                            result = int(value)
                                        except Exception as e:
                                            pass
                                    elif value[0] in ["-","0","1","2","3","4","5","6","7","8","9",dstring] and dstring in value:
                                        try:
                                            result = float(value)
                                        except Exception as e:
                                            pass
                                else:
                                    for vi in range(len(value)):
                                        v = value[vi]
                                        if v in ["-","0","1","2","3","4","5","6","7","8","9",dstring]:
                                            if v == "-" and vi < len(value) and vi > 0:
                                                if value[vi+1] in ["0","1","2","3","4","5","6","7","8","9",dstring] and value[vi-1] not in ["0","1","2","3","4","5","6","7","8","9"]:
                                                    rsign = -1
                                            elif v == "-" and vi < len(value)-1:
                                                if value[vi+1] in ["0","1","2","3","4","5","6","7","8","9"]:
                                                    rsign = -1
                                            elif v == dstring and vi < len(value)-1:
                                                if value[vi+1] in ["0","1","2","3","4","5","6","7","8","9"]:
                                                    rstring += "."
                                            else:
                                                rstring += v
                                    try:
                                        #print(rstring)
                                        if fill_format[:1] == "i":
                                            result = int(float(rstring))*rsign
                                        elif fill_format[:1] == "f":
                                            result = float(rstring)*rsign
                                    except:
                                        #print("Error")
                                        result = None
                        if fill_none is not None:
                            #print(data[ri-1][ci-1])
                            if value is None:
                                result = fill_none

                        if result is not None: data[ri-1][ci-1] = result

                        proc = int((i * nrows + ri) / (ncols * nrows) * 100)
                        sys.stdout.write(u"\u001b[1000D" +  "Processed: " + str(proc) + "% ")
                        sys.stdout.flush()

    print()

    return data


def data_select(data, columns, fromm, too, stepp, randd, listt, colss, noness = [], noneso = ""):
    #global fromm, too, stepp, randd, listt, colss, listi
    nrows = len(data)
    ncols = len(columns)
    colsi = range(1, ncols + 1)
    if len(colss) > 0:
        colsi = find_columns(colss, columns)
    nonesi = []
    if len(noness) > 0:
        nonesi = find_columns(noness, columns)
    #columns_show = [columns[i] for i in colsi] # only existing
    rowsi = []
    listi = []
    if len(listt) > 0:
        if nrows > 0:
            #assert list in range of cases
            for l in listt:
                if l < 0: l += nrows + 1
                if l <= 0: l = 1    # if l was lower than -nrows
                if l > nrows: l = nrows
                if l not in listi: listi.append(l)
        else:
            listi = []
        #print("Listi", listi)
    if fromm < 0:
        fromm += nrows + 1
        if too == 0: too = nrows
    if too < 0:
        too += nrows + 1
        if fromm == 0: fromm = nrows
    if too < fromm:
        pom = fromm
        fromm = too
        too = pom
    if stepp <= 0: stepp = 1
    if too > nrows: too = nrows
    if fromm < 1: fromm = 1
    if len(nonesi) > 0:
        rowni = set()
        rowai = set()
        for ri in range(1, len(data) + 1):
            for ci in nonesi:
                if data[ri-1][ci-1] is None:
                    rowni.add(ri)
                else:
                    rowai.add(ri)
        # logika any, all, none
        #print("rowni", rowni)
        #print("rowai", rowai)
        rowsi = []
        if noneso == "all" or noneso == "any":
            for ri in range(1, len(data) + 1):
                if ri in rowni:
                    if noneso == "any":
                        rowsi.append(ri)
                    elif noneso == "all" and ri not in rowai:
                        rowsi.append(ri)

        elif noneso == "none":
            for ri in range(1, len(data) + 1):
                if ri not in rowni:
                    rowsi.append(ri)
        else:
            variables["$printInvRed"]["options"]["value"]("Error, none_option not recognized")
    elif randd > 0:
        if too == 0: too = nrows
        if len(listi) > 0:
            # select from listt
            # cannot select 2 same cases in list when 0,1 or >nrows => make set
            #listi = list(set(listi))
            if randd > len(listi): randd = len(listi)
            #print("Randd", randd)
            for i in range(randd):
                r = random.choice(listi)
                while r in rowsi:
                    r = random.choice(listi)
                rowsi.append(r)
        else:
            # select fromm-too-stepp
            randmax = int((too-fromm)/stepp) + 1
            #print(fromm, too, stepp, randd, randmax)
            if randd > randmax: randd = randmax
            #if randd == 0: randd = 1
            for i in range(randd):
                r = random.randrange(fromm, too+1, stepp)
                while r in rowsi:
                    r = random.randrange(fromm, too+1, stepp)
                rowsi.append(r)
        #print(listt_show)
    else:
        if len(listi) > 0:
            rowsi = listi
        else:
            rowsi = range(fromm, too+1, stepp)
    return rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss




def parseArgv(argument_list):

    parser = argparse.ArgumentParser()

    parser.add_argument("sql_files", metavar="(SQL_filenames)", type=str, nargs="*",
                    help="Optional list of *.sql filenames (strings) separated by space")
    parser.set_defaults(sql_files="")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument("--interactive", dest="interactive", action="store_true")
    feature_parser.add_argument("--no-interactive", dest="interactive", action="store_false")
    parser.set_defaults(interactive="")

    feature_parser1 = parser.add_mutually_exclusive_group(required=False)
    feature_parser1.add_argument("--multiprocessing", dest="do_mp", action="store_true")
    feature_parser1.add_argument("--no-multiprocessing", dest="do_mp", action="store_false")
    parser.set_defaults(do_mp="")

    return parser.parse_args(argument_list)


def parseText(myText, delimiter, text_qualifiers = ['"', "'", "[", "{"], do_strip = True):

    #print("Uvozovky", myText.count('"'), myText.count("'"))

    lst_new = []
    apos = None
    maxs = -1
    for i, chr in enumerate(myText):
        if not apos and (chr == delimiter):
            if do_strip:
                app_text = myText[maxs+1:i].strip()
                if app_text != "": lst_new.append(app_text)
            else:
                app_text = myText[maxs+1:i]
                lst_new.append(app_text)
            maxs = i
        #elif not apos and (chr == '"' or chr == "'" or chr == "["):
        elif not apos and chr in text_qualifiers:
            # Are there any items before the first apostrophe?
            #lst_new += [o.strip() for o in myText[maxx+1:i].split(spl) if o.strip() is not ""]
            apos = chr
            if apos == "[":
                apos = "]"
            elif apos == "{":
                apos = "}"
            #print(lst_new)
            #print(chr, i)
        elif chr == apos:
            # first line for strlistsplit, senond for sql parse
            #lst_new.append(myText[apos+1:i])
            #lst_new.append(myText[maxs+1:i].strip())
            #print(chr, i)
            apos = None
        # Are there any items after the last apostrophe?
        #if maxa < len(myText): lst_new += [o.strip() for o in myText[maxa+1:].split(spl) if o.strip() is not ""]

    if do_strip:
        app_text = myText[maxs+1:].strip()
        if app_text != "": lst_new.append(app_text)
    else:
        if maxs < len(myText): lst_new.append(myText[maxs+1:])

    #print("lst_new:", lst_new)

    return lst_new


def parseVariable(variables, command, options, n, vartest, logger = None):
    # get variables in context
    ret = None
    opt = None
    variable = None
    #print("vartest", vartest)
    #vartest = str(options[n])
    if len (vartest) > 0:
        if vartest[0] == "$":
            # variable
            #if vartest[0] == "'" and vartest[-1] == "'": vartest = vartest[1:-1]
            #if vartest[0] != "$": vartest = "$" + vartest #variable start with "$", user can omit like in print data all
            #print("vartest", vartest)
            contexts = []
            if vartest in variables:
                variable = vartest
            else:
                for var in variables:
                    if variables[var].get("shorts"):
                        if vartest in variables[var]["shorts"]:
                            variable = var
                            opt = 0
                            break
            if variable:
                #get context
                text = f"Getting context for variable '{variable}' in command '{command}' and option '{options[n]}':"
                logger.debug(text)
                for contexttest in variables[variable]:
                    #print(variables[variable][contexttest])
                    if command in variables[variable][contexttest] or contexttest == "user":
                        contexts.append(contexttest)
                for context in contexts:
                    text = f"Command '{command}' test passed with context '{context}'"
                    logger.debug(text + ":\n" + str(variables[variable][contexttest]))
                    #print(options)
                    opt = 1
                    if context != "user":
                        for optiontest in variables[variable][context][command]:
                            if optiontest in options:
                                if options[optiontest] in variables[variable][context][command][optiontest]:
                                    print(f"Option '{optiontest}' test passed with value '{options[optiontest]}'!")
                                else:
                                    opt = 0
                            else:
                                opt = 0
                    if opt:
                        if variable == "$now":
                            ret = str(variables["$now"]["user"]["value"](None))
                        else:
                            ret = str(variables[variable][context]["value"]) # must look like string input from user
        elif vartest[0] == "@":
            # function
            for f in functions:
                print("vartest[:len(f)]", vartest[:len(f)])
                if vartest[:len(f)] == f and vartest[-1] == ")":
                    print("vartest[len(f):-1]", vartest[len(f):-1])
                    ret, opt = call_function(vartest[len(f):-1], f)
    return ret, opt


def parseCommand(command_line, variables, command_options, logger = None):
    commands = []
    command = ""
    #options = {}
    #error = 0
    execute = False
    #command_line = command_line.replace(" ", "")
    command_line = command_line[1:].strip() #no slash
    #print (command_line)
    for c in command_options:
        #print(c)
        for a in command_options[c]["alternative"]:
            if command_line[:len(a)].lower() == a:
                commands.append((c,a))
                #command_line = command_line[len(a):]
                #command_line = "=".join(parseText(command_line, "="))
                #command_line = ",".join(parseText(command_line, " "))
                #print(command_line)
                #command_line_list = parseText(command_line, ",")
            #if command != "": break
            #print(a)
        #if command != "": break
        #print(c)

    command_line_original = command_line

    for c in commands:
        #print(c[0], c[1])
        command = c[0]
        command_line = command_line_original[len(c[1]):]
        command_line = "=".join(parseText(command_line, "="))
        #command_line = ",".join(parseText(command_line, " "))
        #print("Command line:", command_line)
        #command_line_list = parseText(command_line, ",")
        command_line_list = [l.strip() for l in parseText(command_line, ",", do_strip = False)]
        #print("Command line list:", command_line_list)

        execute = True
        options = {}

        # this should give key=option together
        #print(f"Parse command {command} with ',':", command_line_list)
        cll_final = []
        i = 0
        while i < len(command_line_list):
            if i < len(command_line_list)-2:
                if command_line_list[i+1] == "=":
                    cll_final.append("".join([command_line_list[i],"=",command_line_list[i+2]]))
                    i += 3
                else:
                    cll_final.append(command_line_list[i])
                    i += 1
            else:
                cll_final.append(command_line_list[i])
                i += 1
        #print(cll_final)

        #print(command)
        warnings = []
        errors = []
        for i, cl in enumerate(cll_final):
            #cl = cl.strip()
            #if "=" in cl:
                #cll = cl.split("=")
            cll = parseText(cl, "=", do_strip = False)
            #print("cll:", cll)
            if len(cll) > 1:
                does_exist = 0
                for j, o in enumerate(command_options[command]["name"]):
                    if cll[0].strip().lower() == o:
                        options[o] = cll[1]
                        does_exist = 1
                    else:
                        for a in command_options[command]["altoption"][j]:
                            if cll[0].strip().lower() == a:
                                options[o] = cll[1]
                                does_exist = 1
                            if does_exist: break
                            #print(a)
                if not does_exist:
                    text = f"Unknown option '{cll[0]}' for command '{command}'. I will not use your '{cll[1]}' value in any way."
                    logger.debug(text)
                    errors.append(text)
                    execute = False
            elif cl != "":
                if i < len (command_options[command]["name"]):
                    #print(f'''I will use '{cl}' for option '{command_options[c]["name"][i]}'.''')
                    options[command_options[command]["name"][i]] = cl
                else:
                    text = f"Too many options given for command '{command}'. I will not use your '{cl}' value in any way."
                    logger.debug(text)
                    warnings.append(text)

        for i, z in enumerate(zip(command_options[command]["name"], command_options[command]["required"], command_options[command]["default"], command_options[command]["type"])):
            n, r, d, t = z[0], z[1], z[2], z[3]
            #print(f'''i:{i}, name:{n}, required:{r}, default:{d}, type:{t}''')
            if r:
                #assert command_options[command]["name"][i] in options
                if n not in options:
                    text = f"Missing required argument '{n}' for command '{command}'."
                    logger.debug(text)
                    errors.append(text)
                    execute = False
                    break
            if n not in options and d is not None:
                #print(f'''Default argument '{n}' set to '{d}'.''')
                options[n] = d
            if n in options:
                if isinstance(t, list):
                    if len(options[n]) > 0:
                        if options[n][0] == '"' and options[n][-1] == '"':
                            options[n] = options[n].strip('"')
                        elif options[n][0] == "'" and options[n][-1] == "'":
                            options[n] = options[n].strip("'")
                    bCond = options[n] in t
                    #print(options[n], t, bCond)
                    #sTxt = f"Value '{options[n]}' is not valid for option '{n}'. Use one of these options: {t}."
                    #variables["$Assert"]["options"]["value"](bCond, sTxt)
                    if not bCond:
                        text = f"Value '{options[n]}' is not valid for option '{n}'. Use one of these options {t} for command '{command}'."
                        logger.debug(text)
                        errors.append(text)
                        execute = False
                        break
                elif t == "str":
                    #options[n] = options[n].strip('"')
                    #print("options[n]", options[n])
                    var, opt = parseVariable(variables, command, options, n, str(options[n]), logger)
                    if opt:
                        options[n] = var
                    if len(options[n]) > 0:
                        if options[n][0] == '"' and options[n][-1] == '"':
                            options[n] = options[n].strip('"')
                        elif options[n][0] == "'" and options[n][-1] == "'":
                            options[n] = options[n].strip("'")
                    #print(f"Parse option '{n}' as string:", options[n])
                    #command = "quit"
                elif t == "int":
                    #print(f"I am going to translate '{options[n]}' to 'int'")
                    # check variables first
                    var, opt = parseVariable(variables, command, options, n, str(options[n]), logger)
                    if opt:
                        options[n] = var
                    if opt == 0:
                        text = f"Option '{n}' should be integer but is '{options[n]}', which is not a variable in context of '{command}'. Probably not doing what expected!"
                    else:
                        text = f"Option '{n}' should be integer but is '{options[n]}' in command '{command}'. Probably not doing what expected!"
                    try:
                        options[n] = int(options[n])
                    except Exception as e:
                        #traceback.print_exc()
                        pass
                    #variables["$Assert"]["options"]["value"](isinstance(options[n], int), result_message)
                    if not isinstance(options[n], int):
                        #options[n] = d
                        logger.debug(text)
                        errors.append(text)
                        execute = False
                    #print(f"Parse option '{n}' as integer:", options[n])
                elif t == "intlist":
                    var, opt = parseVariable(variables, command, options, n, str(options[n]), logger)
                    if opt:
                        options[n] = var
                    if options[n][0] == "[" and options[n][-1] == "]":
                        options_list_line = options[n][1:-1]
                    else:
                        text = "Lists must be enclosed with []. Probably not doing what expected!"
                        logger.debug(text)
                        errors.append(text)
                        execute = False
                    #options_list_line = options[n][1:-1]
                    #options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = []
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        l_new = None
                        var, opt = parseVariable(variables, command, options, n, str(l_old), logger)
                        if opt:
                            l_old = var
                        if opt == 0:
                            text = f"Option '{n}' should be integer but is '{options[n]}', which is not a variable in context of '{command}'. Probably not doing what expected!"
                        else:
                            text = f"Option '{n}' should be integer but is '{options[n]}' in command '{command}'. Probably not doing what expected!"
                        try:
                            l_new = int(l_old)
                        except Exception as e:
                            #traceback.print_exc()
                            pass
                        #variables["$Assert"]["options"]["value"](isinstance(l_new, int), result_message)
                        if isinstance(l_new, int) and l_new not in lst_new:
                            lst_new.append(l_new)
                        elif not isinstance(l_new, int):
                            logger.debug(text)
                            errors.append(text)
                            execute = False
                    options[n] = lst_new
                elif t == "strlist":
                    var, opt = parseVariable(variables, command, options, n, str(options[n]), logger)
                    #print("var", var)
                    if opt:
                        options[n] = var
                    #variables["$Assert"]["options"]["value"](options[n][0] == "[" and options[n][-1] == "]", "Lists must be enclosed with []. Probably not doing what expected!")
                    if options[n][0] == "[" and options[n][-1] == "]":
                        options_list_line = options[n][1:-1]
                    else:
                        text = "Lists must be enclosed with []. Probably not doing what expected!"
                        logger.debug(text)
                        errors.append(text)
                        execute = False
                        options_list_line = ""
                    #print(options[n])
                    #options_list_line = options[n][1:-1]
                    #options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = []
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        var, opt = parseVariable(variables, command, options, n, str(l_old), logger)
                        if opt:
                            lst_new.append(var)
                        else:
                            if l_old[0] == '"' and l_old[-1] == '"':
                                lst_new.append(l_old.strip('"'))
                            elif l_old[0] == "'" and l_old[-1] == "'":
                                lst_new.append(l_old.strip("'"))
                            else:
                                lst_new.append(l_old)
                    options[n] = lst_new
                    #options[n] = lst_old
                elif t == "bool":
                    if options[n] == True or options[n] == "True" or options[n] == "true" or options[n] == "1":
                        options[n] = True
                    elif options[n] == False or options[n] == "False" or options[n] == "false" or options[n] == "0":
                        options[n] = False
                    else:
                        text = f"Command '{command}' invalid bool option '{options[n]}'. Using default option '{d}'."
                        logger.debug(text)
                        warnings.append(text)
                        options[n] = d
                elif t == "dictlist":
                    var, opt = parseVariable(variables, command, options, n, str(options[n]), logger)
                    if opt:
                        options[n] = var
                    #variables["$Assert"]["options"]["value"](options[n][0] == "{" and options[n][-1] == "}", "Dicts must be enclosed with {}. Probably not doing what expected!")
                    if options[n][0] == "{" and options[n][-1] == "}":
                        options_list_line = options[n][1:-1]
                    else:
                        text = "Dicsts must be enclosed with {}. Probably not doing what expected!"
                        logger.debug(text)
                        errors.append(text)
                        execute = False
                        options_list_line = ""
                    #options_list_line = options[n][1:-1]
                    #print("options_list_line", options_list_line)
                    options_list_line = ":".join(parseText(options_list_line, ":"))
                    #options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = {}
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        #lst = parseText(l_old, ":", do_strip = False)
                        lst = [l.strip() for l in parseText(l_old, ":", do_strip = False)]
                        #print("lst:", lst)
                        # check if list on any side
                        #print(lst[0].strip().__class__)
                        l, r, ll, rr = None, None, None, None
                        if len(lst) > 1:
                            #lst[0] = lst[0].strip()
                            #lst[1] = lst[1].strip()
                            var, opt = parseVariable(variables, command, options, n, str(lst[0]), logger)
                            if opt:
                                lst[0] = var
                                #parse list from var
                                if lst[0][0] == '[' and lst[0][-1] == ']':
                                    #its a list, mrs walker, its a list
                                    left_list_line = lst[0][1:-1]
                                    #left_list_line = ",".join(parseText(left_list_line, " "))
                                    ll = parseText(left_list_line, ",")
                                else:
                                    l = lst[0]
                            elif lst[0][0] == '[' and lst[0][-1] == ']':
                                #its a list, mrs walker, its a list
                                left_list_line = lst[0][1:-1]
                                #left_list_line = ",".join(parseText(left_list_line, " "))
                                ll = parseText(left_list_line, ",")
                            elif lst[0][0] == '"' and lst[0][-1] == '"':
                                l = lst[0].strip('"')
                            elif lst[0][0] == "'" and lst[0][-1] == "'":
                                l = lst[0].strip("'")
                            else:
                                l = lst[0]
                            var, opt = parseVariable(variables, command, options, n, str(lst[1]), logger)
                            if opt:
                                lst[1] = var
                                #parse list from var
                                if lst[1][0] == '[' and lst[1][-1] == ']':
                                    #its a list, mrs walker, its a list
                                    right_list_line = lst[1][1:-1]
                                    #right_list_line = ",".join(parseText(right_list_line, " "))
                                    rr = parseText(right_list_line, ",")
                                else:
                                    r = lst[1]
                            elif lst[1][0] == '[' and lst[1][-1] == ']':
                                #its a list, mrs walker, its a list
                                right_list_line = lst[1][1:-1]
                                #right_list_line = ",".join(parseText(right_list_line, " "))
                                rr = parseText(right_list_line, ",")
                            elif len(lst[1]) == 0:
                                r = ""
                            elif lst[1][0] == '"' and lst[1][-1] == '"':
                                r = lst[1].strip('"')
                            elif lst[1][0] == "'" and lst[1][-1] == "'":
                                r = lst[1].strip("'")
                            else:
                                r = parseValue(lst[1], variables["$parse_value_type"]["options"]["value"])
                            if l is not None and r is not None:
                                lst_new[l] = r
                            if ll is not None and r is not None:
                                for l in ll:
                                    var, opt = parseVariable(variables, command, options, n, str(l), logger)
                                    if opt:
                                        l = var
                                    elif l[0] == '"' and l[-1] == '"':
                                        l = l.strip('"')
                                    elif l[0] == "'" and l[-1] == "'":
                                        l = l.strip("'")
                                    lst_new[l] = r
                            elif ll is not None and rr is not None:
                                # make two lists
                                variables["$Assert"]["options"]["value"](len(ll) == len(rr), f"Lists {ll}:{rr} in dict '{n}' not of the same size. Check results carefully!!!")
                                #print(list(zip(ll, rr)))
                                for l, r in zip(ll, rr):
                                    var, opt = parseVariable(variables, command, options, n, str(l), logger)
                                    if opt:
                                        l = var
                                    elif l[0] == '"' and l[-1] == '"':
                                        l = l.strip('"')
                                    elif l[0] == "'" and l[-1] == "'":
                                        l = l.strip("'")
                                    var, opt = parseVariable(variables, command, options, n, str(r), logger)
                                    if opt:
                                        r = var
                                    elif len(r) == 0:
                                        r = ""
                                    elif r[0] == '"' and r[-1] == '"':
                                        r = r.strip('"')
                                    elif r[0] == "'" and r[-1] == "'":
                                        r = r.strip("'")
                                    else:
                                        r = parseValue(r, variables["$parse_value_type"]["options"]["value"])
                                    lst_new[l] = r
                        else:
                            variables["$printRed"]["options"]["value"](f"Error parsing dictlist option {lst}. Check results carefully!!!")
                    options[n] = lst_new

        #print("Command:", command)
        #print("Options:", options)
        #print("Execute:", execute)
        if not execute:
            logger.debug(f"Parse command '{command}' as NOT EXECUTED on command line:\n" + command_line_original)

        if execute: break

    if not execute:
        command = ""
        options = []
        #print errors
        print()
    else:
        printoptions = {}
        for op in options:
            if isinstance(options[op], str):
                printoptions[op] = "'" + options[op] + "'"
            else:
                printoptions[op] = options[op]
        variables["$printYellow"]["options"]["value"](f'''Command '{command}' with options [{', '.join([str(str(op) + "=" + str(printoptions[op])) for op in printoptions])}].''')
        print()

    return command, options

def get_sql_queries_dict(lst, foldername):
    sqls_local = {}
    OK_returned = 1
    for sql_filename in lst:
        #print("SQL file:", sql_file)
        full_filename, file_exists = check_filename(sql_filename, foldername)
        #print("Check if file exists:", sql_file_exists)
        if file_exists:
            with open(full_filename, mode="r", encoding="utf-8") as f:
                sql = f.read()
                #print("SQL file query:")
                #print(sql.strip(), sql.count(";"))
                sqls_local[full_filename] = parseText(sql, ";")
        else:
            variables["$printRed"]["options"]["value"](f'''! SQL file '{full_filename}' does not exist !''')
            OK_returned = 2
    return OK_returned, sqls_local

def check_foldername(foldername, foldername_old):
    folder_exists = False
    full_foldername = None
    if foldername == os.pardir:
        full_foldername = os.path.dirname(foldername_old)
    elif foldername.strip() != "":
        if os.path.isabs(foldername):
            full_foldername = foldername
        else:
            full_foldername = os.path.join(foldername_old, foldername)
    else:
        # foldername.strip() == "" => os.path.isdir(full_foldername) would fail
        full_foldername = foldername_old
    folder_exists = os.path.isdir(full_foldername)
    return full_foldername, folder_exists

def check_filename(filename, foldername):
    file_exists = False
    full_filename = None
    if os.path.isabs(filename):
        full_filename = filename
    else:
        full_filename = os.path.realpath(os.path.join(foldername, os.path.expanduser(filename)))
    file_exists = os.path.isfile(full_filename)
    #print(full_filename)
    return full_filename, file_exists


def do_sql(sql, command_options, variables, datas = {}, output = None, logger = None):

    data = None
    columns = None
    colsp = None
    data_old = None
    columns_old = None
    colsp_old = None

    if datas.get("data") is not None:
        data = datas.get("data").get("data")
        columns = datas.get("data").get("columns")
        colsp = datas.get("data").get("colsp")

    if datas.get("data_old") is not None:
        data_old = datas.get("data_old").get("data")
        columns_old = datas.get("data_old").get("columns")
        colsp_old = datas.get("data_old").get("colsp")

    if logger is None:
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
            logging.basicConfig(filename='log.txtx', encoding='utf-8', filemode='w', level=logging.DEBUG, format='%(asctime)s:%(name)s\n%(levelname)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')
        else:
            logging.basicConfig(filename='log.txtx', filemode='w', level=logging.DEBUG, format='%(asctime)s:%(name)s\n%(levelname)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')
        logger = logging.getLogger(__name__)
        logger.info('Started')

    OK = 1

    if sql.startswith("\\"):
        command, options = parseCommand(sql, variables, command_options, logger)
        #print(command, options)

        if command == "quit" or command == "q":
            logger.debug(f"Command '{command}' passed as executed with options:\n" + str(options))
            OK = 0

        elif command == "#":
            logger.debug(f"Command '{command}' passed as executed with options:\n" + str(options))
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            if title: # excluse empty string to show title
                    if title_color:
                        cc = colorCode(title_color)
                        variables["$printColor"]["options"]["value"](title, cc)
                    else:
                        cc = variables["$INVGREEN"]["options"]["value"]
                        variables["$printColor"]["options"]["value"](title, cc)
            if note:
                print()
                if note_color:
                    cc = colorCode(note_color)
                    variables["$printColor"]["options"]["value"](note, cc)
                else:
                    print(note)

        elif command == "connect sqlite3 easy" or command == "connect sqlite3":
            # , isolation_level=None == autocommit
            db_filename = options["filename"]
            parse_formats = options.get("parse_formats")
            if db_filename == ":memory:":
                variables["$printInvGreen"]["options"]["value"]("Using database in memory. Save or loose!")
                try:
                    if parse_formats:
                        variables["$conn"]["options"]["value"] = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
                    else:
                        variables["$conn"]["options"]["value"] = sqlite3.connect(":memory:")
                    variables["$db_version"]["options"]["value"] = "Sqlite3 (memory): "
                except Exception as e:
                    traceback.print_exc()
            else:
                full_filename, file_exists = check_filename(db_filename, variables["$foldername"]["options"]["value"])
                variables["$db_full_filename"]["options"]["value"] = os.path.join(variables["$foldername"]["options"]["value"], full_filename)
                if file_exists:
                    variables["$printInvGreen"]["options"]["value"](f'''Using database '{variables["$db_full_filename"]["options"]["value"]}'.''')
                else:
                    variables["$printInvGreen"]["options"]["value"](f'''Creating database '{variables["$db_full_filename"]["options"]["value"]}'.''')
                try:
                    #conn = sqlite3.connect(full_filename, isolation_level=None)
                    if parse_formats:
                        variables["$conn"]["options"]["value"] = sqlite3.connect(full_filename, detect_types=sqlite3.PARSE_DECLTYPES)
                    else:
                        variables["$conn"]["options"]["value"] = sqlite3.connect(full_filename)
                    variables["$db_version"]["options"]["value"] = f'''Sqlite3 ({variables["$db_full_filename"]["options"]["value"]}): '''
                except Exception as e:
                    traceback.print_exc()

        elif command == "connect mysql":
            #"database", "user", "password", "host", "port"
            database = options["database"]
            user = options["user"]
            password = options["password"]
            host = options["host"]
            port = options["port"]
            try:
                print("Using mysqlclient version:", version("mysqlclient"))
                import MySQLdb
                #import mysql.connector
                #from mysql.connector import errorcode
                #can use errno

                #cnx = mysql.connector.connect(user="scott", database="test")
                #cursor = cnx.cursor()
                #connpars = parse_connstring(connstring)
                #print(connpars["server"])
                #print(connpars["user"])
                #print(connpars["password"])
                try:
                    variables["$conn"]["options"]["value"] = MySQLdb.connect(database = database, \
                    user = user, password = password, host = host, \
                    port = port, use_unicode=True,charset="utf8")
                    #conn.autocommit(True)
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    variables["$db_version"]["options"]["value"] = f"MySQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()

            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "connect postgre":
            #"database", "user", "password", "host", "port"
            database = options["database"]
            user = options["user"]
            password = options["password"]
            host = options["host"]
            port = options["port"]
            try:
                print("Using psycopg2 version:", version("psycopg2"))
                import psycopg2
                try:
                    variables["$conn"]["options"]["value"] = psycopg2.connect(database = database, \
                    user = user, password = password, host = host, \
                    port = port)
                    #conn.set_session(autocommit=True)
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    variables["$db_version"]["options"]["value"] = f"PostgreSQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()
            except Exception as e:
                print("No MySQL support. Please run 'pip install mysqlclient'.\n")
                traceback.print_exc()

        elif command == "connect mssql":
            #"database", "user", "password", "host", "port"
            #"", "root", "admin", "localhost", 3306

            database = options.get("database")
            user = options.get("user")  #root
            password = options.get("password")  #admin
            host = options.get("host")  #socket.gethostname()
            port = options.get("port")  #3306
            driver = options.get("driver")  #"SQL Server"
            option = options.get("option")  #"trustedconn=true"
            autocommit = options.get("autocommit")  #"trustedconn=true"

            '''
            driver = "FreeTDS"
            server = "wvxxxgroup.cz"
            port = 1111
            database = "dbSPSS"
            user = "u"
            password = "p"
            option = "TDS_Version=8.0"
            #server = socket.gethostname()

            conn = pyodbc.connect('Driver={SQL Server};'
              f'Server={server}\SQLEXPRESS;'
              f'Database={database};'
              'Trusted_Connection=yes;')

            f'DRIVER={driver};'
              f'Server={host};'
              f'PORT={port}'
              f'Database={database};'
              f'UID={user};'
              f'PWD={password};'
              f'{option};'
            '''
            #print(database)
            connstring = ""
            if driver is not None: connstring += f'DRIVER={driver};'
            if host is not None: connstring += f'Server={host};'
            if port is not None: connstring += f'PORT={port};'
            if database is not None: connstring += f'Database={database};'
            if user is not None: connstring += f'UID={user};'
            if password is not None: connstring += f'PWD={password};'
            if option is not None: connstring += f'{option};'

            '''
            server = socket.gethostname()
            connstring = 'Driver={SQL Server};' + \
              f'Server={server}\SQLEXPRESS;' + \
              f'Database={database};' + \
              'Trusted_Connection=yes;'
            '''

            #print(connstring)

            try:
                print("Using pyodbc version:", version("pyodbc"))
                import pyodbc
                try:
                    variables["$conn"]["options"]["value"] = pyodbc.connect(connstring)
                    if autocommit: variables["$conn"]["options"]["value"].autocommit = True
                    #conn.autocommit = True
                    #conn = mysql.connector.connect(host = "localhost", user = "root", password="admin", use_unicode=True,charset="utf8")
                    variables["$db_version"]["options"]["value"] = f"MsSQL (Add schema!): "
                except Exception as e:
                    traceback.print_exc()
            except Exception as e:
                print("No MsSQL support. Please run 'pip install pyodbc'.\n")
                traceback.print_exc()


        elif command == "set variable easy" or command == "set variable":

            set_variable_names = options.get("names")
            #set_variable_type = variables["$parse_value_type"]["options"]["value"]

            for vn in set_variable_names:
                if len(vn) > 0:
                    print(vn + ": " + str(set_variable_names[vn]))
                    if vn[0] != "$":
                        v = "$" + vn
                    else:
                        v = vn
                if v not in variables:
                    variables[v] = {}
                    variables[v]["shorts"] = []
                variables[v]["user"] = {}
                variables[v]["user"]["value"] = set_variable_names[vn]


        elif command == "set option easy" or command == "set option":

            set_option_names = options.get("names")
            #set_option_type = variables["$parse_value_type"]["options"]["value"]

            for vn in set_option_names:
                if len(vn) > 0:
                    print(vn + ": " + str(set_option_names[vn]))
                    if vn[0] != "$":
                        v = "$" + vn
                    else:
                        v = vn
                if v not in variables:
                    variables[v] = {}
                    variables[v]["shorts"] = []
                variables[v]["options"] = {}
                variables[v]["options"]["value"] = set_option_names[vn]


        elif command == "print variables easy" or command == "print variables":

            print_variables_names = options.get("names")

            if print_variables_names is not None:
                pass
            else:
                #print(",\n".join(str(v) for v in [vi for vi in variables.items()]))
                # print except pure option (has keys "options" and "shorts", e.g. len == 2)
                print(",\n".join(str(v) for v in variables.items() if "options" not in v[1] or len(v[1]) > 2))


        elif command == "print options easy" or command == "print options":

            print_options_names = options.get("names")

            if print_options_names is not None:
                pass
            else:
                #print(",\n".join(str(v) for v in [vi for vi in variables.items()]))
                # print except pure option (has keys "options" and "shorts", e.g. len == 2)
                print(",\n".join(str(v) for v in variables.items() if "options" in v[1]))


        elif command == "folder":
            logger.debug(f"Command '{command}' passed as executed with options:\n" + str(options))
            foldername_old = variables["$foldername"]["options"]["value"]
            #foldername = sql[len("\folder:"):]
            foldername = options.get("foldername")
            foldername_lst = parseText(foldername, delimiter = os.sep, text_qualifiers = [], do_strip = True)
            #print(foldername_lst)
            #folder = os.path.isdir(foldername)
            if len(foldername_lst) > 0:
                foldername_old_part = foldername_old
                for foldername_part in foldername_lst:
                    if foldername_part[-1] == ":": foldername_part += "\\"  #e.g."c:"
                    if foldername_part[0] == "$" or foldername_part[0] == "%": foldername_part = os.path.expandvars(foldername_part)    #e.g. ${TEMP} or %HOMEPATH%
                    if foldername_part == ".": foldername_part = ""  #e.g."." for stay in the same directory
                    if foldername_part == "~": foldername_part = os.path.expanduser(foldername_part)    #e.g. "~: for go home
                    full_foldername, folder_exists = check_foldername(foldername_part, foldername_old_part)
                    if folder_exists:
                        foldername_old_part = full_foldername
                    else:
                        break
            else:
                foldername = foldername.strip()
                foldername = foldername.replace(os.sep, "")
                if len(foldername) > 0:
                    if foldername[-1] == ":": foldername += "\\"  #e.g."c:"
                    if foldername[0] == "$" or foldername[0] == "%": foldername = os.path.expandvars(foldername)
                    if foldername == ".": foldername = ""  #e.g."c:"
                    if foldername == "~": foldername = os.path.expanduser(foldername)
                #print(foldername)
                full_foldername, folder_exists = check_foldername(foldername, foldername_old)
            if folder_exists:
                text = f"Using folder '{full_foldername}'."
                variables["$printInvGreen"]["options"]["value"](text)
                variables["$foldername"]["options"]["value"] = full_foldername
                logger.info(text)
            else:
                text = f"Folder '{foldername}' does not exist. Using current folder '{foldername_old}'."
                variables["$printInvRed"]["options"]["value"](text)
                variables["$foldername"]["options"]["value"] = foldername_old
                logger.error(text)
                OK = 2

        elif command == "read":
            logger.debug(f"Command '{command}' passed as executed with options:\n" + str(options))
            colsp = {}  #reset columns profile
            read_filename = options.get("filename")
            read_delimiter = options.get("delimiter")
            read_lines = options.get("lines")
            if read_lines is None: read_lines = -1
            read_text_qualifier = options.get("text_qualifier")
            read_columns = options.get("read_columns")
            strip_columns = options.get("strip_columns")
            read_print_data = options.get("print_data")
            full_filename, file_exists = check_filename(read_filename, variables["$foldername"]["options"]["value"])
            #print("Read: '{}'".format(read_filename))
            try:
                with open(full_filename, "r", encoding = "utf-8") as f:
                    data_new = []
                    columns_new = []
                    is_error = False
                    error = 0
                    data_line = f.readline()
                    # line with column names
                    if data_line:
                        if data_line[-1] == "\n": data_line = data_line[:-1]
                        if read_text_qualifier:
                            parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], False)
                        else:
                            parsed_line = data_line.split(read_delimiter)
                        for i, c in enumerate(parsed_line):
                            if read_columns:
                                if read_text_qualifier and len(c) >= 2:
                                    if c[0] == read_text_qualifier and c[-1] == read_text_qualifier: c = c[1:-1]
                                    #print(c)
                                if strip_columns: c = c.strip()
                                columns_new.append(c)
                            else:
                                # add empty column name for later correction
                                columns_new.append("")
                        if read_columns: data_line = f.readline()
                        row = 0
                        len_columns = len(columns_new)
                        max_columns = len(columns_new)
                        while data_line and row != read_lines:
                            #print("."+data_line+".")
                            row += 1
                            row_new = []
                            if data_line[-1] == "\n": data_line = data_line[:-1]
                            if read_text_qualifier:
                                parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], False)
                            else:
                                parsed_line = data_line.split(read_delimiter)
                            if len(parsed_line) != max_columns:
                                is_error = True
                                if len(parsed_line) > max_columns: max_columns = len(parsed_line)
                            for c in parsed_line:
                                if len(c) >= 2:
                                    if c[0] == read_text_qualifier and c[-1] == read_text_qualifier: c = c[1:-1]
                                    #print(c)
                                if c != "":
                                    row_new.append(c)
                                else:
                                    row_new.append(None)
                            data_new.append(row_new)
                            #print(row_new)
                            #time.sleep(1)
                            data_line = f.readline()
                            if row % 10000 == 0:
                                sys.stdout.write(u"\u001b[1000D" +  "Lines read: " + str(row) + " ")
                                sys.stdout.flush()
                    #print(data_new)
                    cc = variables["$INVGREEN"]["options"]["value"]
                    text = variables["$strColor"]["options"]["value"]("Lines read: " + str(row) + ", with " + str(max_columns) + " columns.", cc)
                    sys.stdout.write(u"\u001b[1000D" + text)
                    sys.stdout.flush()
                    print()
                    # calculate cc for missing columns
                    cc = 0
                    rest = max_columns
                    while rest > 0:
                        rest = int(rest/(10**cc))
                        #print(rest)
                        cc += 1
                    if is_error:
                        # add new column names only; these columns has always artificial names
                        for i in range(len_columns, max_columns):
                            c = variables["$default_column_name"]["options"]["value"] + f"{(i+1):0{(cc-1)}}"
                            columns_new.append(c)
                        for row, d in enumerate(data_new):
                            if max_columns > len(d):
                                error +=1
                                if error >= 0 and error < 10:
                                    variables["$printRed"]["options"]["value"](f"ERROR on row {row+1}. Check carefully!!!")
                                elif error == 10:
                                    variables["$printRed"]["options"]["value"](f"Further ERROR messages surpressed!!!")
                                for i in range(max_columns - len(d)):
                                    d.append(None)
                    # correct empty column names
                    for i in range(len(columns_new)):
                        if columns_new[i] == "":
                            columns_new[i] = variables["$default_column_name"]["options"]["value"] + f"{(i+1):0{(cc-1)}}"
                    if error > 0:
                        variables["$printInvRed"]["options"]["value"](f"ERRORs in TOTAL {error}. Check carefully!!!")
                        print(max_columns, len_columns)
                    if len(data_new) > 0 or len(columns_new) > 0:
                        data = data_new
                        columns = columns_new
                        data_old = None
                        columns_old = None
                        if read_print_data:
                            print()
                            show_data(data, columns, variables)
                    else:
                        variables["$printInvRed"]["options"]["value"]("! There are no data returned from this file !")
                        OK = 2
            except Exception as e:
                traceback.print_exc()
                variables["$printInvRed"]["options"]["value"](str(e))
                OK = 2

        elif command == "export":
            export_filename = options["filename"]
            export_delimiter = options["delimiter"]
            if options.get("none") is not None:
                export_none = options["none"]
            else:
                export_none = None  # never happens, but was before, now is ""
            #print("export_none", export_none)
            full_filename, file_exists = check_filename(export_filename, variables["$foldername"]["options"]["value"])
            #print("Export: '{}'".format(export_filename))
            col_len = len(columns)-1
            try:
                with open(full_filename, mode="w", encoding="utf-8") as f:
                    for i, c in enumerate(columns):
                        if i < col_len:
                            f.write(str(c) + export_delimiter)
                        else:
                            f.write(str(c))
                    f.write("\n")
                    for d in data:
                        for i, c in enumerate(d):
                            if c is None: c = export_none
                            if i < col_len:
                                f.write(str(c) + export_delimiter)
                            else:
                                f.write(str(c))
                        f.write("\n")
            except Exception as e:
                traceback.print_exc()

        elif command == "load":
            #Vratit zpatky db_version a folder pred load
            foldername_return = variables["$foldername"]["options"]["value"]
            silent_mode_return = variables["$silent_mode"]["options"]["value"]
            sql_filename = options["filename"]
            if options.get("silent_mode"):
                variables["$silent_mode"]["options"]["value"] = True
            OK_returned, sqls_load = get_sql_queries_dict([sql_filename], variables["$foldername"]["options"]["value"])
            if OK_returned == 1:
                for full_filename in sqls_load.keys():
                    #OK_returned = 1
                    for i, sql_load in enumerate(sqls_load[full_filename]):
                        if not variables["$silent_mode"]["options"]["value"]:
                            variables["$printCom"]["options"]["value"](f"\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\")
                        #print(sql)
                        #print()
                        start = time.perf_counter()
                        variables, datas, output, logger = do_sql(sql_load, command_options, variables, datas, output, logger)
                        OK_returned = variables["$command_results"]["options"]["value"][-1]
                        end = time.perf_counter()
                        if OK_returned == 1:
                            if not variables["$silent_mode"]["options"]["value"]:
                                print()
                                print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                        elif OK_returned > 1:
                            print()
                            variables["$printRed"]["options"]["value"]("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                            print()
                            time.sleep(2)
                            OK = 2
                        else: break
            else:
                print()
                OK = 2
            variables["$foldername"]["options"]["value"] = foldername_return
            variables["$silent_mode"]["options"]["value"] = silent_mode_return
            if OK == 1:
                variables["$printInvGreen"]["options"]["value"]("LOAD SUMMARY: All commands from loaded file were OK.")
            else:
                variables["$printInvRed"]["options"]["value"]("! LOAD SUMMARY: Some commands from loaded file were KO !")


        elif command == "split":
            colss = options.get("columns")
            colssp = options.get("split")
            if colss is not None:
                colsi = find_columns(colss, columns)
            else:
                colsi = [ci for ci in range(1,len(columns)+1)]
            colsai = colsi
            if colssp is not None:
                colspi = find_columns(colssp, columns)
            colsai = colsi + colspi
            #data_profile(range(1, len(data) + 1), colsai)
            colsp = {}  #should check if not exists already
            data, colsp = data_profile(data, columns, variables, colsp, range(1, len(data) + 1), colsai, purge = False)
            colsif = [ci for ci in colsi if colsp[ci]['type'] == "Integer" or colsp[ci]['type'] == "Float"] #should check class
            print("colsif (final colsi):", colsif)
            colspif = [cspi for cspi in colspi if colsp[cspi]['type'] == "Categorical"]
            if variables["$do_mp"]["options"]["value"]:
                inn = [[colsp, [colspi]] for colspi in colspif]
                pool = mp.Pool()
                returns = pool.map(data_split_prep_mp, inn)
                #print(returns)
                pool.close()
                for ret in returns:
                    colsp[ret[0]]['cats'] = ret[1]
                inn = [[colsp, [ci], colspif, True] for ci in colsif]
                pool = mp.Pool()
                returns = pool.map(data_split_mp, inn)
                #print(returns)
                pool.close()
                for ret in returns:
                    colsp[ret[0]]['split'] = ret[1]
            else:
                colsp = data_split_prep(colsp, colspif)
                colsp = data_split(colsp, colsif, colspif, True)
            #print(colsp[colspif[0]]['cats'])
            #data_split0(colspiff)
            #data_split(colsif, colspif, True)

            split_data = []
            split_rows = []
            #profile_rows = ["Type", "Class", "Valids", "Nones", "Valid %", "Sum", "Min", "Max", "Range", "Mean", "Q1", "Median", "Q3", "IQR", "Variance", "STD", "Skew", "Unique", "FirstCat"]
            #profile_rows_label = '(Stat)'
            #stats = ["type", "class", "valid", "none", "valid%", "sum", "min", "max", "range", "mean", "q1", "q2", "q3", "iqr", "var", "std", "skew", "unique", "fnq"]
            split_rows_label = ' - '.join([colsp[cspi]['name'] for cspi in colspif])    #TODO: user split variable
            #stats = ["t", "cl", "v", "n", "v%", "sum", "min", "max", "mean", "q1", "q2", "q3", "ran", "iqr", "var", "std", "skw","uni", "fnq"]
            stats = ["type","valid","none"]
            split_columns = [colsp[ci[0]]['name']+ci[1] for ci in [(colsif[i],stats[j]) for i in range(len(colsif)) for j in range(len(stats))]]
            print(split_columns)

            cif = colsif[0] #are categories the same in all variables???
            for cspis in colsp[cif]['split']:
                for cat in colsp[cif]['split'][cspis]:
                    split_data.append([])
                    split_rows.append(cat)
                    for ci in [(colsif[i],stats[j]) for i in range(len(colsif)) for j in range(len(stats))]:
                        #print('ci', colsp[ci[0]]['split'][cspis][cat]['value'])
                        if len(colsp[ci[0]]['split'][cspis][cat]['value'])>0:
                            split_data[-1].append(len(colsp[ci[0]]['split'][cspis][cat]['value']))
                        else:
                            split_data[-1].append("-")
                        '''
                        #if ci > 0:  # rows_label, all profiled columns
                        if ci > 0 and (ci in colsi or print_all):  # rows_label, all or last profiled columns
                            if stat == "v%":
                                if (colsp[ci]["v"] + colsp[ci]["n"]) > 0:
                                    split_data[i].append(round(100 * colsp[ci]["v"] / (colsp[ci]["v"] + colsp[ci]["n"]), 2))
                                else:
                                    split_data[i].append("-")
                        '''

            nrows = len(split_data)
            ncols = len(split_columns)

            colsi = range(1, ncols + 1)
            rowsi = range(1, nrows + 1)

            print("ncols", ncols)

            print()
            print()

            print_data(rowsi, colsi, split_data, split_columns, split_rows, split_rows_label, variables)


        elif command == "data memory" or command == "data memory easy":
            memory_name = options.get("name")
            print("data memory", memory_name)
            if data_memory.get(memory_name) is None and columns_memory.get(memory_name) is None and colsp_memory.get(memory_name) is None:
                data_memory[memory_name] = copy.deepcopy(data)
                columns_memory[memory_name] = copy.deepcopy(columns)
                colsp_memory[memory_name] = copy.deepcopy(colsp)


        elif command == "data activate" or command == "data activate easy":
            print("data activate")
            memory_name = options.get("name")
            if data_memory.get(memory_name) is not None and columns_memory.get(memory_name) is not None and colsp_memory.get(memory_name) is not None:
                data = copy.deepcopy(data_memory.get(memory_name))
                columns = copy.deepcopy(columns_memory.get(memory_name))
                colsp = copy.deepcopy(colsp_memory.get(memory_name))
                data_old = None
                columns_old = None
            show_data(data, columns, variables)


        elif command == "graph histogram":
            colss = options.get("columns")
            colssp = options.get("split")
            title = options.get("title")
            if colss is not None:
                colsi = find_columns(colss, columns)
            else:
                colsi = [ci for ci in range(1,len(columns)+1)]
            colsai = colsi
            colspi = []
            if colssp is not None:
                colspi = find_columns(colssp, columns)
            colsai = colsi + colspi
            data, colsp = data_profile(data, columns, variables, colsp, range(1, len(data) + 1), colsai)
            colsif = [ci for ci in colsi if colsp[ci]['type'] == "Integer" or colsp[ci]['type'] == "Float"]
            print("colsif (final colsi):", colsif)
            colspif = [cspi for cspi in colspi if colsp[cspi]['type'] == "Categorical"]
            print("colspif (final colspi):", colspif)
            if len(colspif) > 0:
                colsp = data_split_prep(colsp, colspif)
                colsp = data_split(colsp, colsif, colspif, True)

            if is_mpl:
                print("Go to plot window...")
                for ci in colsif:
                    if title is not None:
                        titlee = title + ": " + colsp[ci]["name"]
                    else:
                        titlee = colsp[ci]["name"]
                    if len(colspif) > 0:
                        for cspi in colspif:
                            getHistogram(colsp, ci, cspi, titlee)
                    else:
                        getHistogram(colsp, ci, None, titlee)
                print("All windows closed...")
            else:
                print("Go plot support...")

        elif command == "graph linechart":
            colss = options.get("columns")
            title = options.get("title")
            if colss is not None:
                colsi = find_columns(colss, columns)
            else:
                colsi = [ci for ci in range(1,len(columns)+1) if colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time"]
            #print(colsi)
            if is_mpl:
                for ci in colsi:
                    if title is not None:
                        titlee = title + ": " + colsp[ci]["name"]
                    else:
                        titlee = colsp[ci]["name"]
                    getLineChartI(colsp, ci, titlee)


        elif command == "graph boxplot":
            colss = options.get("columns")
            title = options.get("title")
            boxplot_showfliers = options.get("show_fliers")
            if colss is not None:
                colsi = find_columns(colss, columns)
            else:
                colsi = [ci for ci in range(1,len(columns)+1) if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float"]
            #print("Colsi", colsi)
            if is_mpl:
                getBoxplotI(colsp, colsi, title, boxplot_showfliers)


        elif command == "graph barchart":
            colss = options.get("columns")
            title = options.get("title")
            if colss is not None:
                colsi = find_columns(colss, columns)
            else:
                colsi = [ci for ci in range(1,len(columns)+1) if colsp[ci]['t'] == "Categorical"]
            #print(colsi)
            if is_mpl:
                for ci in colsi:
                    if title is not None:
                        titlee = title + ": " + colsp[ci]["name"]
                    else:
                        titlee = colsp[ci]["name"]
                    getBarChartI(colsp, ci, titlee)


        elif command == "table":
            tablename = options["tablename"]
            table_drop = options["drop_if_exists"]
            table_id = options.get("id")
            #print(columns)
            #print("\n" + "Insert:", tablename)

            part1 = ""
            part2 = ""
            columns_create = ""
            columns_print = []
            sql1 = ""
            sql2 = ""
            sql3 = ""

            if variables["$db_version"]["options"]["value"][:7] == "Sqlite3":
                sql1 = f'''drop table if exists "{tablename}"'''
                #columns_create += "ida INTEGER PRIMARY KEY AUTOINCREMENT"
                if table_id is not None:
                    columns_create += table_id + " INTEGER PRIMARY KEY AUTOINCREMENT"
                for i, ci in enumerate(colsp):
                    col = colsp[ci]['name']
                    columns_print.append(f'''"{col}"''')
                    if table_id is None and i == 0:
                        columns_create += f'''"{col}" '''
                    else:
                        columns_create += f''', "{col}" '''
                    if colsp[ci]["type"] == "Integer":
                        columns_create += "int"
                    elif colsp[ci]["type"] == "Float":
                        columns_create += "real"
                    elif colsp[ci]["type"] == "Datetime":
                        columns_create += "datetime"
                    elif colsp[ci]["type"] == "Date":
                        columns_create += "date"
                    elif colsp[ci]["type"] == "Time":
                        # sqlite does not use timedelta for time format, min datetime is 0001-01-01 0:0:0:
                        columns_create += "time"
                        if colsp[ci]["class"] is not variables["$class_str"]["options"]["value"]:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    data[ri-1][ci-1] = str(data[ri-1][ci-1])
                        '''
                        for ri in range(1, len(data) + 1):
                            if data[ri-1][ci-1] is not None:
                                if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                data[ri-1][ci-1] = str(data[ri-1][ci-1])
                        '''
                    else:
                        columns_create += "text"
                    if i == 0:
                        #part1 += '''{{0[{}]}}'''.format(str(i))
                        part1 += f"{{0[{str(i)}]}}"
                        #part2 += '''?'''.format(str(i))
                        part2 += "?"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",?"
                    #print(i)
                sql2 = f'''create table "{tablename}" ({columns_create})'''
                sql3 = f'''insert into "{tablename}" ({part1}) values ({part2})'''

            elif variables["$db_version"]["options"]["value"][:5] == "MySQL":
                sql1 = f'''drop table if exists `{tablename}`'''
                #columns_create += "ida INTEGER PRIMARY KEY AUTOINCREMENT"
                if table_id is not None:
                    columns_create += table_id + " INTEGER PRIMARY KEY AUTO_INCREMENT"
                for i, ci in enumerate(colsp):
                    col = colsp[ci]['name']
                    columns_print.append(f'''`{col}`''')
                    if table_id is None and i == 0:
                        columns_create += f'''`{col}` '''
                    else:
                        columns_create += f''', `{col}` '''
                    if colsp[ci]["type"] == "Integer":
                        columns_create += "int"
                    elif colsp[ci]["type"] == "Float":
                        columns_create += "real"
                    elif colsp[ci]["type"] == "Datetime":
                        columns_create += "datetime"
                    elif colsp[ci]["type"] == "Date":
                        columns_create += "date"
                    elif colsp[ci]["type"] == "Time":
                        columns_create += "time"
                    else:
                        columns_create += "text"
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "%s"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",%s"
                    #print(i)
                sql2 = f'''create table `{tablename}` ({columns_create})'''
                sql3 = f'''insert into `{tablename}` ({part1}) values ({part2})'''

            elif variables["$db_version"]["options"]["value"][:10] == "PostgreSQL":
                sql1 = f'''drop table if exists "{tablename}"'''
                #columns_create += "ida INTEGER PRIMARY KEY AUTOINCREMENT"
                if table_id is not None:
                    columns_create += table_id + " SERIAL PRIMARY KEY"
                for i, ci in enumerate(colsp):
                    col = colsp[ci]['name']
                    columns_print.append(f'''"{col}"''')
                    if table_id is None and i == 0:
                        columns_create += f'''"{col}" '''
                    else:
                        columns_create += f''', "{col}" '''
                    if colsp[ci]["type"] == "Integer":
                        columns_create += "int"
                    elif colsp[ci]["type"] == "Float":
                        columns_create += "real"
                    elif colsp[ci]["type"] == "Datetime":
                        columns_create += "timestamp"
                    elif colsp[ci]["type"] == "Date":
                        columns_create += "date"
                    elif colsp[ci]["type"] == "Time":
                        columns_create += "time"
                    else:
                        columns_create += "text"
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "%s"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",%s"
                    #print(i)
                sql2 = f'''create table "{tablename}" ({columns_create})'''
                sql3 = f'''insert into "{tablename}" ({part1}) values ({part2})'''

            elif variables["$db_version"]["options"]["value"][:5] == "MsSQL":
                sql1 = f'''drop table if exists "{tablename}"'''
                #columns_create += "ida INTEGER PRIMARY KEY AUTOINCREMENT"
                if table_id is not None:
                    columns_create += table_id + " INT NOT NULL IDENTITY(1,1) PRIMARY KEY"
                for i, ci in enumerate(colsp):
                    col = colsp[ci]['name']
                    columns_print.append(f'''"{col}"''')
                    if table_id is None and i == 0:
                        columns_create += f'''"{col}" '''
                    else:
                        columns_create += f''', "{col}" '''
                    if colsp[ci]["type"] == "Integer":
                        columns_create += "bigint"
                    elif colsp[ci]["type"] == "Float":
                        columns_create += "real"   # this format is Approximate numerics
                        #columns_create += "decimal(10,3)"
                    elif colsp[ci]["type"] == "Datetime":
                        columns_create += "datetime"
                        if colsp[ci]["class"] is not variables["$class_str"]["options"]["value"]:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    data[ri-1][ci-1] = str(data[ri-1][ci-1])
                    elif colsp[ci]["type"] == "Date":
                        columns_create += "date"
                        if colsp[ci]["class"] is not variables["$class_str"]["options"]["value"]:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    data[ri-1][ci-1] = str(data[ri-1][ci-1])
                    elif colsp[ci]["type"] == "Time":
                        columns_create += "time"
                        if colsp[ci]["class"] is not variables["$class_str"]["options"]["value"]:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    if isinstance(data[ri-1][ci-1], datetime.timedelta):
                                        data[ri-1][ci-1] = str(datetime.datetime.min + data[ri-1][ci-1])[11:]    #time without date starting 0/1/2 (02:02:02, not 2:02:02)
                                    else:
                                        data[ri-1][ci-1] = str(data[ri-1][ci-1])
                    else:
                        # this leads to crash if instance is not str
                        columns_create += "nvarchar(max)"
                        if colsp[ci]["class"] is not variables["$class_str"]["options"]["value"]:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    data[ri-1][ci-1] = str(data[ri-1][ci-1])

                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "?"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",?"
                    #print(i)
                sql2 = f'''create table "{tablename}" ({columns_create})'''
                sql3 = f'''insert into "{tablename}" ({part1}) values ({part2})'''

            #print()
            #print(db_version + sql)
            #print(db_version + sql.format(columns_print))
            #print(columns, data)

            if table_drop:
                print(sql1)
                try:
                    c = variables["$conn"]["options"]["value"].cursor()
                    #print(columns_print)
                    #print(sql.format(columns_print))
                    c.execute(sql1)
                    variables["$conn"]["options"]["value"].commit()
                    #print()
                    #variables["$printInvGreen"]["options"]["value"]("! There are no data returned from this sql query !")
                except Exception as e:
                    traceback.print_exc()
                    variables["$printInvRed"]["options"]["value"](str(e))
                    if OK: OK = 2

            try:
                print(sql2)
                c = variables["$conn"]["options"]["value"].cursor()
                #print(columns_print)
                #print(sql.format(columns_print))
                c.execute(sql2)
                variables["$conn"]["options"]["value"].commit()
                #print()
                #variables["$printInvGreen"]["options"]["value"]("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()
                variables["$printInvRed"]["options"]["value"](str(e))
                if OK: OK = 2

            if OK == 1:
                print(sql3)
                try:
                    c = variables["$conn"]["options"]["value"].cursor()
                    #print(columns_print)
                    #print(sql.format(columns_print))
                    c.executemany(sql3.format(columns_print), data)
                    variables["$conn"]["options"]["value"].commit()
                    print()
                    variables["$printInvGreen"]["options"]["value"]("! There are no data returned from this sql query !")
                except Exception as e:
                    traceback.print_exc()
                    variables["$printInvRed"]["options"]["value"](str(e))
                    if OK: OK = 2


        elif command == "insert":
            tablename = options["tablename"]
            #print(columns)
            #print("\n" + "Insert:", tablename)
            part1 = ""
            part2 = ""
            if variables["$db_version"]["options"]["value"][:7] == "Sqlite3":
                for i, c in enumerate(columns):
                    if i == 0:
                        #part1 += '''{{0[{}]}}'''.format(str(i))
                        part1 += f"{{0[{str(i)}]}}"
                        #part2 += '''?'''.format(str(i))
                        part2 += "?"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",?"
                    for ri in range(1, len(data) + 1):
                        if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                        if isinstance(data[ri-1][i], datetime.timedelta):
                            data[ri-1][i] = str(datetime.datetime.min + data[ri-1][i])[11:]    #time without date starting 0/1/2 (02:02:02, not 2:02:02)
                        elif isinstance(data[ri-1][i], datetime.time):
                            data[ri-1][i] = str(data[ri-1][i])
                    #print(i)
                sql = f'''insert into "{tablename}" ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''"{col}"''')

            elif variables["$db_version"]["options"]["value"][:5] == "MySQL":
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "%s"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",%s"
                    #print(i)
                sql = f'''insert into `{tablename}` ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''`{col}`''')

            elif variables["$db_version"]["options"]["value"][:10] == "PostgreSQL":
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "%s"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",%s"
                    #print(i)
                sql = f'''insert into "{tablename}" ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''"{col}"''')

            elif variables["$db_version"]["options"]["value"][:5] == "MsSQL":
                for i, c in enumerate(columns):
                    if i == 0:
                        part1 += f"{{0[{str(i)}]}}"
                        part2 += "?"
                    else:
                        part1 += f",{{0[{str(i)}]}}"
                        part2 += ",?"
                    for ri in range(1, len(data) + 1):
                        if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                        if isinstance(data[ri-1][i], datetime.timedelta):
                            data[ri-1][i] = str(datetime.datetime.min + data[ri-1][i])[11:]    #time without date starting 0/1/2 (02:02:02, not 2:02:02)
                        elif isinstance(data[ri-1][i], datetime.datetime):
                            data[ri-1][i] = str(data[ri-1][i])
                        elif isinstance(data[ri-1][i], datetime.date):
                            data[ri-1][i] = str(data[ri-1][i])
                        elif isinstance(data[ri-1][i], datetime.time):
                            data[ri-1][i] = str(data[ri-1][i])
                    #print(i)
                sql = f'''insert into "{tablename}" ({part1}) values ({part2})'''
                columns_print = []
                for col in columns:
                    columns_print.append(f'''"{col}"''')

            #print()
            #print(db_version + sql)
            print(variables["$db_version"]["options"]["value"] + sql.format(columns_print))
            #print(columns, data)
            try:
                c = variables["$conn"]["options"]["value"].cursor()
                #print(columns_print)
                #print(sql.format(columns_print))
                c.executemany(sql.format(columns_print), data)
                variables["$conn"]["options"]["value"].commit()
                print()
                variables["$printInvGreen"]["options"]["value"]("! There are no data returned from this sql query !")
            except Exception as e:
                traceback.print_exc()
                variables["$printInvRed"]["options"]["value"](str(e))
                if OK: OK = 2

        elif command == "print" or command == "print data" or command == "print data all" or command == "print data easy" or command == "print columns" or command == "print history":
            if command == "print columns": options["what"] = "columns"
            if command == "print" or command == "print data" or command == "print data all" or command == "print data easy": options["what"] = "data"
            if command == "print history": options["what"] = "history"
            if options["what"] == "c": options["what"] = "columns"
            if options["what"] == "d": options["what"] = "data"
            if options["what"] == "h": options["what"] = "history"

            logger.debug(f"Command '{command}' passed as executed with options:\n" + str(options))

            if options["what"] == "columns":

                print_columns_how = options.get("how")
                if print_columns_how == "n": print_columns_how = "name"
                if print_columns_how == "i": print_columns_how = "index"

                if print_columns_how == "name":
                    print(columns)
                else:
                    # print_columns_how == "index"
                    print("{" + ", ".join([f"{i+1}:'{c}'" for i, c in enumerate(columns)]) + "}")

            elif options["what"] == "history":

                print(";\n".join([str(c) for c in variables["$command_history"]["options"]["value"]]) + ";")

            elif options["what"] == "data":

                fromm = options["from"]
                too = options["to"]
                stepp = options["step"]
                listt = options["list"]
                randd = options["random"]
                colss = options["columns"]
                noness = options.get("nones")
                noneso = options.get("nones_option")
                title = options.get("title")
                note = options.get("note")
                title_color = options.get("title_color")
                note_color = options.get("note_color")
                #print("Title:", title)
                #print(fromm, too, stepp)

                nrows = len(data)
                ncols = len(columns)

                rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss)
                #print(rows_show)

                columns_show = [columns[ci-1] for ci in colsi]

                title_text = ""

                if title is not None:   # include empty string to show no title
                    title_text = title
                    #variables["$printInvGreen"]["options"]["value"](title)
                elif len(listt) > 0 and randd == 0:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns.")
                elif len(listt) > 0 and randd > 0:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns.")
                elif randd > 0:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns.")
                else:
                    if len(colss) > 0:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                    else:
                        title_text = f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns."
                        #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns.")

                if title_text: # excluse empty string to show title
                    if title_color:
                        cc = colorCode(title_color)
                        variables["$printColor"]["options"]["value"](title_text, cc)
                    else:
                        cc = variables["$INVGREEN"]["options"]["value"]
                        variables["$printColor"]["options"]["value"](title_text, cc)

                rows = range(1, nrows + 1)
                rows_label = variables["$rows_label"]["options"]["value"]
                #print(rows)
                print_data(rowsi, colsi, data, columns, rows, rows_label, variables)

                if note:
                    print()
                    if note_color:
                        cc = colorCode(note_color)
                        variables["$printColor"]["options"]["value"](note, cc)
                    else:
                        print(note)


        elif command == "data columns rename":

            if not data_old and not columns_old:
                data_old = data.copy()
                columns_old = columns.copy()
                #data_old = copy.deepcopy(data)
                #columns_old = copy.deepcopy(columns)

            data_columns_rename_columns = options.get("columns")
            data_columns_rename_how = options.get("how")

            print(f"Columns: '{data_columns_rename_columns}', How: '{data_columns_rename_how}'.")

            if data_columns_rename_how == "n": data_columns_rename_how = "name"
            if data_columns_rename_how == "i": data_columns_rename_how = "index"

            if data_columns_rename_how == "name":
                if data_columns_rename_columns is not None:
                    colsi = find_columns(data_columns_rename_columns, columns)
                    for ci in colsi:
                        columns[ci-1] = data_columns_rename_columns[columns[ci-1]]
                else:
                    # throw error
                    pass
            else:
                # data_columns_rename_how == "index"
                for ci_str in data_columns_rename_columns:
                    try:
                        ci = int(ci_str)
                        if ci == 0:
                            variables["$printRed"]["options"]["value"](f"Column index '{ci}' out of range '1' - '{len(columns)}'!")
                        elif ci > len(columns):
                            variables["$printRed"]["options"]["value"](f"Column index '{ci}' out of range '1' - '{len(columns)}'!")
                        elif ci < -len(columns):
                            variables["$printRed"]["options"]["value"](f"Column index '{ci}' out of range '1' - '{len(columns)}'!")
                        else:
                            ci -= 1
                            columns[ci] = data_columns_rename_columns[ci_str]
                    except Exception as e:
                        #traceback.print_exc()
                        variables["$printRed"]["options"]["value"](str(e))



        elif command == "data fill easy" or command == "data fill":

            if not data_old and not columns_old:
                data_old = copy.deepcopy(data)
                columns_old = copy.deepcopy(columns)

            fill_formats = options.get("formats")
            fill_nones = options.get("nones")
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            #print("Title:", title)
            #print(fromm, too, stepp)

            nrows = len(data)
            ncols = len(columns)

            data = data_fill(variables, data, columns, fill_formats, fill_nones)
            #print(rows_show)

            title_text = ""

            if title is not None:   # include empty string to show no title
                title_text = title
                #variables["$printInvGreen"]["options"]["value"](title)
            else:
                title_text = f"Format data {fill_formats}"

            if title_text: # excluse empty string to show title
                if title_color:
                    cc = colorCode(title_color)
                    variables["$printColor"]["options"]["value"](title_text, cc)
                else:
                    cc = variables["$INVGREEN"]["options"]["value"]
                    variables["$printColor"]["options"]["value"](title_text, cc)

            #rows = range(1, nrows + 1)
            #print(rows)
            #print_data(rowsi, colsi, data, columns, rows, rows_label)
            show_data(data, columns, variables, False)

            if note:
                print()
                if note_color:
                    cc = colorCode(note_color)
                    variables["$printColor"]["options"]["value"](note, cc)
                else:
                    print(note)

            #print(columns, data)


        elif command == "data reset":
            if data_old and columns_old:
                data = copy.deepcopy(data_old)
                columns = copy.deepcopy(columns_old)
            show_data(data, columns, variables)


        elif command == "data select easy" or command == "data select":

            if not data_old and not columns_old:
                data_old = data.copy()
                columns_old = columns.copy()
                #data_old = copy.deepcopy(data)
                #columns_old = copy.deepcopy(columns)

            fromm = options["from"]
            too = options["to"]
            stepp = options["step"]
            listt = options["list"]
            randd = options["random"]
            colss = options["columns"]
            noness = options.get("nones")
            noneso = options.get("nones_option")
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            #print("Title:", title)
            #print(fromm, too, stepp)

            nrows = len(data)
            ncols = len(columns)

            rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss, noness, noneso)
            #print(rows_show)

            columns_selected = [columns[ci-1] for ci in colsi]
            data_selected = [[data[ri-1][ci-1] for ci in colsi] for ri in rowsi]

            title_text = ""

            if title is not None:   # include empty string to show no title
                title_text = title
                #variables["$printInvGreen"]["options"]["value"](title)
            elif len(listt) > 0 and randd == 0:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} listed cases {listi} with selected columns {columns_selected}."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} listed cases {listi} with all columns."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} listed cases {listi} with all columns.")
            elif len(listt) > 0 and randd > 0:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {listi} with selected columns {columns_selected}."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {listi} with all columns."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {listi} with all columns.")
            elif randd > 0:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_selected}."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} random cases from {fromm} to {too} step {stepp} with all columns.")
            else:
                if len(colss) > 0:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_selected}."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with selected columns {columns_show}.")
                else:
                    title_text = f"There are {nrows} rows, {ncols} columns. Selected {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns."
                    #variables["$printInvGreen"]["options"]["value"](f"There are {nrows} rows, {ncols} columns. Printing {len(rowsi)} cases from {fromm} to {too} step {stepp} with all columns.")

            if title_text: # excluse empty string to show title
                if title_color:
                    cc = colorCode(title_color)
                    variables["$printColor"]["options"]["value"](title_text, cc)
                else:
                    cc = variables["$INVGREEN"]["options"]["value"]
                    variables["$printColor"]["options"]["value"](title_text, cc)

            #rows = range(1, nrows + 1)
            #print(rows)
            #print_data(rowsi, colsi, data, columns, rows, rows_label)
            show_data(data_selected, columns_selected, variables, False)

            if note:
                print()
                if note_color:
                    cc = colorCode(note_color)
                    variables["$printColor"]["options"]["value"](note, cc)
                else:
                    print(note)

            # do I need deepcopy?
            data = data_selected.copy()
            columns = columns_selected.copy()
            colsp = {}

            #print(columns, data)


        elif command == "data profile easy" or command == "data profile":

            fromm = options["from"]
            too = options["to"]
            stepp = options["step"]
            listt = options["list"]
            randd = options["random"]
            colss = options["columns"]
            noness = options.get("nones")
            noneso = options.get("nones_option")
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            print_all = options.get("print_all")
            purge = options.get("purge")
            #print("Title:", title)
            #print(fromm, too, stepp)

            #nrows = len(data)
            #ncols = len(columns)

            rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss, noness, noneso)

            #TODO: option to print only if closp exists
            if variables["$do_mp"]["options"]["value"]:
                inn = []
                #spli = 4
                spli = mp.cpu_count()
                splr = int(len(rowsi)/spli)
                rowsins = []
                for i in range(spli):
                    if i < spli-1:
                        rowsins.append(rowsi[i*splr:(i+1)*splr])
                    else:
                        rowsins.append(rowsi[i*splr:])
                varins = {}
                for var in variables:
                    if var in ["$time", "$decimal_separator", "$thousands_separator", "$datetime", "$date", "$profile_show_categorical"]:
                        varins[var] = variables[var]
                for order, rowsin in enumerate(rowsins):
                    print("order", order)
                    print("rowsin", rowsin)
                    inndata = [data[ri-1] for ri in rowsin]
                    inn.append([inndata, rowsin, colsi, varins, order, spli-1])

                pool = mp.Pool(processes = spli)
                returns = pool.map(data_profile_prep_mp, inn)
                #print(returns)
                pool.close()

                for i, ci in enumerate(colsi):
                    colsp[ci] = {}
                    nonone = False
                    for order in range(len(rowsins)):
                        for ret in returns:
                            #colsp[ret[0]]['cats'] = ret[1]
                            if ret[1] == order:
                                #print(order)
                                if order == 0:
                                    rv = ret[0][ci]["rv"]
                                    mv = ret[0][ci]["mv"]
                                    rn = ret[0][ci]["rn"]
                                    fnq = ret[0][ci]["fnq"]
                                    if len(rv) > 0:
                                        t = ret[0][ci]["t"]
                                        nonone = True
                                    else:
                                        # ret[0][ci]["t"] == "Integer"
                                        t = None
                                    cl = ret[0][ci]["cl"]
                                else:
                                    rv += ret[0][ci]["rv"]
                                    mv += ret[0][ci]["mv"]
                                    rn += ret[0][ci]["rn"]
                                    if fnq is None:
                                        fnq = ret[0][ci]["fnq"]
                                    if len(rv) > 0:
                                        if t != ret[0][ci]["t"] and nonone:
                                            t = None
                                        else:
                                            t = ret[0][ci]["t"]
                                        if cl != ret[0][ci]["cl"] and nonone:
                                            cl = None
                                        else:
                                            cl = ret[0][ci]["cl"]
                                        nonone = True
                    a = np.array(rv)
                    b = np.array(mv)
                    c = np.array(rn)
                    d = np.empty(len(rn))
                    #colsp[ci]["av"] = rfn.merge_arrays((A, B))
                    colsp[ci]["array_valids"] = np.rec.fromarrays((a, b), names=('row', 'value'))
                    colsp[ci]["array_nones"] = np.rec.fromarrays((c, d), names=('row', 'value'))
                    colsp[ci]["fnq"] = fnq
                    colsp[ci]["type"] = t
                    colsp[ci]["class"] = cl
                    colsp[ci]["name"] = columns[ci-1]
                    colsp[ci]['split'] = {} #use in data_split
                    if len(colsp[ci]["array_valids"]) == 0: colsp[ci]["type"] = None   #"Categorical"???
                    #print(colsp[ci]["name"], len(colsp[ci]["array_valids"]), colsp[ci]["type"], colsp[ci]["class"])
                    proc = int(i/len(colsp)*100)
                    sys.stdout.write(u"\u001b[1000D" +  "Data concat processed: " + str(proc) + "% ")
                    sys.stdout.flush()
                proc = 100
                sys.stdout.write(u"\u001b[1000D" +  "Data concat processed: " + str(proc) + "% ")
                sys.stdout.flush()

                inn = [(colsp[ci], ci, varins, i, len(colsp)) for i, ci in enumerate(colsp)]
                pool = mp.Pool(processes = spli)
                returns = pool.map(data_profile_mp, inn)
                #print(returns)
                pool.close()
                # it is not necessary copy colsp[ci] incl av, an, fnq, type, name
                # TODO: optimize
                for ret in returns:
                    colsp[ret[1]] = ret[0]
                proc = 100
                sys.stdout.write(u"\u001b[1000D" +  "Data profile processed: " + str(proc) + "% ")
                sys.stdout.flush()
            else:
                data, colsp = data_profile(data, columns, variables, colsp, rowsi, colsi, purge)

            if print_all:
                profile_columns = [colsp[ci]["name"] for ci in colsp ] # print all profiled columns
            else:
                profile_columns = [colsp[ci]["name"] for ci in colsp if ci in colsi] # print last profiled columns
            profile_rows = ["Type", "Class", "Valids", "Nones", "Valid %", "Sum", "Min", "Max", "Range", "Mean", "Q1", "Median", "Q3", "IQR", "Variance", "STD", "Skew", "Unique", "FirstCat"]
            profile_rows_label = '(Stat)'
            stats = ["type", "class", "valid", "none", "valid%", "sum", "min", "max", "range", "mean", "q1", "q2", "q3", "iqr", "var", "std", "skew", "unique", "fnq"]

            for i in range(variables["$profile_show_categorical"]["options"]["value"]):
                for j in range(3):
                    if j == 0: profile_rows.append("Cat" + str(i + 1) + " (v)")
                    elif j == 1: profile_rows.append("Cat" + str(i + 1) + " (n)")
                    elif j == 2: profile_rows.append("Cat" + str(i + 1) + " (%)")
                    stats.append("cat_" + str(i) + "_" + str(j))

            profile_data = []

            for i, stat in enumerate(stats):
                profile_data.append([])
                for ci in colsp:
                    #if ci > 0:  # rows_label, all profiled columns
                    if ci > 0 and (ci in colsi or print_all):  # rows_label, all or last profiled columns
                        if stat == "type":
                            if isinstance(colsp[ci]["type"], str):
                                profile_data[i].append(colsp[ci]["type"][:5])    # Quant, Categ
                            else:
                                profile_data[i].append("-")
                        elif stat == "class":
                            if isinstance(colsp[ci]["class"], type):
                                cla = str(colsp[ci]["class"])[8:-2]
                                if cla.startswith("datetime."): cla = cla[9:]
                                profile_data[i].append(cla)    # <class 'xxx'>
                            else:
                                profile_data[i].append("-")
                        elif stat == "valid":
                            if colsp[ci]["valid"] is not None:
                                profile_data[i].append(colsp[ci]["valid"])
                            else:
                                profile_data[i].append("0")
                        elif stat == "none":
                            if colsp[ci]["none"] is not None:
                                profile_data[i].append(colsp[ci]["none"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "valid%":
                            if colsp[ci]["valid"] is not None and colsp[ci]["all"] > 0:
                                profile_data[i].append(round(100 * colsp[ci]["valid"] / colsp[ci]["all"], 2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "sum":
                            if colsp[ci]["sum"] is not None:
                                profile_data[i].append(round(colsp[ci]["sum"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "min":
                            if colsp[ci]["min"] is not None:
                                profile_data[i].append(colsp[ci]["min"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "max":
                            if colsp[ci]["max"] is not None:
                                profile_data[i].append(colsp[ci]["max"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "range":
                            if colsp[ci]["range"] is not None:
                                profile_data[i].append(colsp[ci]["range"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "mean":
                            if colsp[ci]["mean"] is not None:
                                profile_data[i].append(round(colsp[ci]["mean"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "q1":
                            if colsp[ci]["q1"] is not None:
                                #np.percentile(colsp[ci]["av"]['value'],25,interpolation='midpoint'
                                profile_data[i].append(round(colsp[ci]["q1"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "q2":
                            if colsp[ci]["q2"] is not None:
                                profile_data[i].append(round(colsp[ci]["q2"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "q3":
                            if colsp[ci]["q3"] is not None:
                                profile_data[i].append(round(colsp[ci]["q3"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "iqr":
                            if colsp[ci]["iqr"] is not None:
                                profile_data[i].append(round(colsp[ci]["iqr"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "var":
                            if colsp[ci]["var"] is not None:
                                profile_data[i].append(round(colsp[ci]["var"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "std":
                            if colsp[ci]["std"] is not None:
                                profile_data[i].append(round(colsp[ci]["std"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "skew":
                            if colsp[ci]["skew"] is not None:
                                profile_data[i].append(round(colsp[ci]["skew"],2))
                            else:
                                profile_data[i].append("-")
                        elif stat == "unique":
                            if colsp[ci]["unique"] is not None:
                                profile_data[i].append(colsp[ci]["unique"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "fnq":
                            if colsp[ci]["fnq"] is not None:
                                profile_data[i].append(colsp[ci]["fnq"])
                            else:
                                profile_data[i].append("-")
                        elif stat[:3] == "cat":
                            ii = stat[stat.find("_")+1:-2]
                            try:
                                ii = int(ii)
                                if colsp[ci]["unique"] is not None:
                                    if ii < colsp[ci]["unique"]:
                                        if stat[-1] == "0":
                                            profile_data[i].append(colsp[ci]["categ_counts"][ii][0])
                                        elif stat[-1] == "1":
                                            profile_data[i].append(colsp[ci]["categ_counts"][ii][1])
                                        elif stat[-1] == "2" and colsp[ci]["valid"] > 0:
                                            profile_data[i].append(round(100*colsp[ci]["categ_counts"][ii][1]/colsp[ci]["valid"],2))
                                        else:
                                            profile_data[i].append("-")
                                    else:
                                        profile_data[i].append("-")
                                else:
                                        profile_data[i].append("-")
                            except Exception as e:
                                #traceback.print_exc()
                                profile_data[i].append("-")
                        else:
                            profile_data[i].append("-")

            #print(profile_data)

            nrows = len(profile_data)
            ncols = len(profile_columns)

            colsi = range(1, ncols + 1)
            rowsi = range(1, nrows + 1)

            #print("ncols", ncols)

            print()
            print()
            #colsp = data_profile(rowsi, colsi, profile_data, profile_columns, profile_rows, profile_rows_label)
            print_data(rowsi, colsi, profile_data, profile_columns, profile_rows, profile_rows_label, variables)


        elif command == "data profile easy old" or command == "data profile old":

            fromm = options["from"]
            too = options["to"]
            stepp = options["step"]
            listt = options["list"]
            randd = options["random"]
            colss = options["columns"]
            noness = options.get("nones")
            noneso = options.get("nones_option")
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            print_all = options.get("print_all")
            purge = options.get("purge")
            #print("Title:", title)
            #print(fromm, too, stepp)

            #nrows = len(data)
            #ncols = len(columns)

            rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss, noness, noneso)

            '''
            nrows = len(data)
            ncols = len(columns)
            colsi = range(1, ncols + 1)
            rowsi = range(1, nrows + 1)
            rows = range(1, nrows + 1)
            '''

            #TODO: option to print only if closp exists
            if variables["$do_mp"]["options"]["value"]:
                inn = []
                spli = 4
                splr = int(len(rowsi)/spli)
                rowsins = []
                for i in range(spli):
                    if i < spli-1:
                        rowsins.append(rowsi[i*splr:(i+1)*splr])
                    else:
                        rowsins.append(rowsi[i*splr:])
                varins = {}
                for var in variables:
                    if var != "$now": varins[var] = variables[var]
                for order, rowsin in enumerate(rowsins):
                    print("order", order)
                    print("rowsin", rowsin)
                    inndata = [data[ri-1] for ri in rowsin]
                    inn.append([inndata, rowsin, colsi, varins, order, spli-1])
                pool = mp.Pool()
                returns = pool.map(data_profile_mp, inn)
                #print(returns)
                pool.close()
                colspnew = {}
                for ci in colsi:
                    colspnew[ci] = {}
                    nonone = False
                    for order in range(len(rowsins)):
                        for ret in returns:
                            #colsp[ret[0]]['cats'] = ret[1]
                            if ret[1] == order:
                                #print(order)
                                if order == 0:
                                    rv = ret[0][ci]["rv"]
                                    mv = ret[0][ci]["mv"]
                                    rn = ret[0][ci]["rn"]
                                    fnq = ret[0][ci]["fnq"]
                                    if len(rv) > 0:
                                        t = ret[0][ci]["t"]
                                        nonone = True
                                    else:
                                        # ret[0][ci]["t"] == "Integer"
                                        t = None
                                    cl = ret[0][ci]["cl"]
                                else:
                                    rv += ret[0][ci]["rv"]
                                    mv += ret[0][ci]["mv"]
                                    rn += ret[0][ci]["rn"]
                                    if fnq is None:
                                        fnq = ret[0][ci]["fnq"]
                                    if len(rv) > 0:
                                        if t != ret[0][ci]["t"] and nonone:
                                            t = None
                                        else:
                                            t = ret[0][ci]["t"]
                                        if cl != ret[0][ci]["cl"] and nonone:
                                            cl = None
                                        else:
                                            cl = ret[0][ci]["cl"]
                                        nonone = True
                    a = np.array(rv)
                    b = np.array(mv)
                    c = np.array(rn)
                    d = np.empty(len(rn))
                    #colsp[ci]["av"] = rfn.merge_arrays((A, B))
                    colspnew[ci]["av"] = np.rec.fromarrays((a, b), names=('row', 'value'))
                    colspnew[ci]["an"] = np.rec.fromarrays((c, d), names=('row', 'value'))
                    if fnq is None: fnq = "None"
                    colspnew[ci]["fnq"] = fnq
                    colspnew[ci]["t"] = t
                    colspnew[ci]["cl"] = cl
                    colspnew[ci]["name"] = columns[ci-1]
                    if len(colspnew[ci]["av"]) == 0: colspnew[ci]["t"] = None   #"Categorical"???
                    print(colspnew[ci]["name"], len(colspnew[ci]["av"]), colspnew[ci]["t"], colspnew[ci]["cl"])

                    #no mp compare
                    colsp = {}
                    colsp = data_profile(rowsi, colsi, purge)

            else:
                colsp = {}
                colsp = data_profile(rowsi, colsi, purge)

            profile_data = []
            if print_all:
                profile_columns = [colsp[ci]["name"] for ci in colsp ] # print all profiled columns
            else:
                profile_columns = [colsp[ci]["name"] for ci in colsp if ci in colsi] # print last profiled columns
            profile_rows = ["Type", "Class", "Valids", "Nones", "Valid %", "Sum", "Min", "Max", "Mean", "Q1", "Median", "Q3", "Range", "IQR", "Variance", "STD", "Skew", "Unique", "FirstCat"]
            profile_rows_label = '(Stat)'
            stats = ["t", "cl", "v", "n", "v%", "sum", "min", "max", "mean", "q1", "q2", "q3", "ran", "iqr", "var", "std", "skw", "uni", "fnq"]
            #stats = ["t", "cl", "v", "n", "v%", "sum", "min", "max", "mean", "q1", "q2", "q3", "ran", "iqr", "var", "std", "skw"]

            for i in range(variables["$profile_show_categorical"]["options"]["value"]):
                for j in range(3):
                    if j == 0: profile_rows.append("Cat" + str(i + 1) + " (v)")
                    elif j == 1: profile_rows.append("Cat" + str(i + 1) + " (n)")
                    elif j == 2: profile_rows.append("Cat" + str(i + 1) + " (%)")
                    stats.append("c_" + str(i) + "_" + str(j))

            for i, stat in enumerate(stats):
                profile_data.append([])
                for ci in colsp:
                    v = len(colspnew[ci]["av"])
                    n = len(colspnew[ci]["an"])
                    c = len(np.unique(colsp[ci]["av"]['value']))
                    uv, uc = np.unique(colsp[ci]["av"]['value'], return_counts=True)
                    #count_sort_ind = np.argsort(-count)
                    #u[count_sort_ind]
                    cc = np.flip(np.sort(np.rec.fromarrays((uv, uc), names=('value', 'count')), order = "count"))
                    #print(cc)
                    if colsp[ci]["t"] == "Integer" or colsp[ci]["t"] == "Float" or colsp[ci]["t"] == "Datetime" or colsp[ci]["t"] == "Date" or colsp[ci]["t"] == "Time":
                        min = colspnew[ci]["av"]['value'].min()
                        max = colspnew[ci]["av"]['value'].max()
                    if colsp[ci]["t"] == "Integer" or colsp[ci]["t"] == "Float":
                        sum = colspnew[ci]["av"]['value'].sum()
                        mean = colsp[ci]['av']['value'].mean()
                        lenc = len(colsp[ci]['av'])
                        if lenc > 0:
                            #print(ci, sorted(colsp[ci]['m']))
                            m = sorted(colsp[ci]['av']["value"])
                            if lenc >= 1 and lenc % 2:
                                q2 = m[int((lenc+1)/2)-1]
                            if lenc >= 2 and (lenc % 2) == 0:
                                q2 = (m[int(lenc/2)-1] + m[int(lenc/2)])/2    #mean of mid cases
                        lenc = int(len(m)/2)
                        if lenc > 0:
                            #print(ci, sorted(colsp[ci]['m']))
                            #colsp[ci]['m'] = sorted(colsp[ci]['m'])
                            if lenc >= 1 and lenc % 2:
                                q1 = m[int((lenc+1)/2)-1]
                            if lenc >= 2 and (lenc % 2) == 0:
                                q1 = (m[int(lenc/2)-1] + m[int(lenc/2)])/2    #mean of mid cases
                            if lenc >= 1 and lenc % 2:
                                q3 = m[-1*int((lenc+1)/2)]
                            if lenc >= 2 and (lenc % 2) == 0:
                                q3 = (m[-1*int(lenc/2)] + m[-1*(int(lenc/2))-1])/2    #mean of mid cases
                        smd2 = 0
                        smd3 = 0
                        for mi in m:
                            smd2 += (mi - mean)**2
                            smd3 += (mi - mean)**3

                    #if ci > 0:  # rows_label, all profiled columns
                    if ci > 0 and (ci in colsi or print_all):  # rows_label, all or last profiled columns
                        if stat == "t":
                            if isinstance(colsp[ci]["t"], str):
                                profile_data[i].append(colsp[ci]["t"][:5] + "(" + colspnew[ci]["t"][:5] + ")")    # Quant, Categ
                            else:
                                profile_data[i].append("-")
                        elif stat == "cl":
                            if isinstance(colsp[ci]["cl"], type):
                                cla = str(colsp[ci]["cl"])[8:-2]
                                if cla.startswith("datetime."): cla = cla[9:]
                                cla1 = str(colspnew[ci]["cl"])[8:-2]
                                if cla1.startswith("datetime."): cla1 = cla1[9:]
                                profile_data[i].append(cla + "(" + cla1 + ")")    # <class 'xxx'>
                            else:
                                profile_data[i].append("-")
                        elif stat == "v":
                            if colsp[ci]["v"] is not None:
                                profile_data[i].append(str(colsp[ci]["v"]) + "(" + str(v) + ")")
                            else:
                                profile_data[i].append("0")
                        elif stat == "n":
                            if colsp[ci]["n"] is not None:
                                profile_data[i].append(str(colsp[ci]["n"]) + "(" + str(n) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "v%":
                            if (colsp[ci]["v"] + colsp[ci]["n"]) > 0 and (v + n) > 0:
                                profile_data[i].append(str(round(100 * colsp[ci]["v"] / (colsp[ci]["v"] + colsp[ci]["n"]), 2)) + "(" + str(round(100 * v / (v + n), 2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "sum":
                            if colsp[ci]["sum"] is not None:
                                profile_data[i].append(str(round(colsp[ci]["sum"],2)) + "(" + str(round(sum,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "min":
                            if colsp[ci]["min"] is not None:
                                profile_data[i].append(str(colsp[ci]["min"]) + "(" + str(min) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "max":
                            if colsp[ci]["max"] is not None:
                                profile_data[i].append(str(colsp[ci]["max"]) + "(" + str(max) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "mean":
                            if colsp[ci]["mean"] is not None:
                                profile_data[i].append(str(round(colsp[ci]["mean"],2)) + "(" + str(round(mean,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "q1":
                            if colsp[ci]["q1"] is not None:
                                #np.percentile(colsp[ci]["av"]['value'],25,interpolation='midpoint'
                                profile_data[i].append(str(round(colsp[ci]["q1"],2)) + "(" + str(round(q1,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "q2":
                            if colsp[ci]["q2"] is not None:
                                profile_data[i].append(str(round(colsp[ci]["q2"],2)) + "(" + str(round(q2,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "q3":
                            if colsp[ci]["q3"] is not None:
                                profile_data[i].append(str(round(colsp[ci]["q3"],2)) + "(" + str(round(q3,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "ran":
                            if colsp[ci]["min"] is not None and colsp[ci]["max"] is not None and (colsp[ci]["t"] == "Integer" or colsp[ci]["t"] == "Float"):
                                profile_data[i].append(str(round(colsp[ci]["max"] - colsp[ci]["min"], 2)) + "(" + str(round(max - min,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "iqr":
                            if colsp[ci]["q3"] is not None and colsp[ci]["q1"] is not None:
                                profile_data[i].append(str(round(colsp[ci]["q3"] - colsp[ci]["q1"], 2)) + "(" + str(round(q3 - q1,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "var":
                            if colsp[ci]["smd2"] is not None and colsp[ci]["v"] > 0 and (colsp[ci]["t"] == "Integer" or colsp[ci]["t"] == "Float"):
                                profile_data[i].append(str(round(colsp[ci]["smd2"] / colsp[ci]["v"], 2)) + "(" + str(round(smd2 / v,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "std":
                            if colsp[ci]["smd2"] is not None and colsp[ci]["v"] > 0 and (colsp[ci]["t"] == "Integer" or colsp[ci]["t"] == "Float"):
                                profile_data[i].append(str(round((colsp[ci]["smd2"] / colsp[ci]["v"])**0.5, 2)) + "(" + str(round((smd2 / v)**0.5,2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "skw":
                            if colsp[ci]["smd3"] is not None and colsp[ci]["smd2"] > 0 and colsp[ci]["v"] > 0 and (colsp[ci]["t"] == "Integer" or colsp[ci]["t"] == "Float"):
                                profile_data[i].append(str(round(colsp[ci]["smd3"] / (colsp[ci]["v"] * (colsp[ci]["smd2"] / colsp[ci]["v"])**1.5), 2)) + "(" + str(round(smd3 / (v * (smd2 / v)**1.5),2)) + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat == "uni":
                            if len(colsp[ci]["c"]) < profile_max_categorical:
                                profile_data[i].append(str(len(colsp[ci]["c"])) + "(" + str(c) + ")")
                                #if len(colsp[ci]["c"]) > maxc: maxc = len(colsp[ci]["c"])
                            else:
                                profile_data[i].append("-")
                        elif stat == "fnq":
                            if colsp[ci]["fnq"] is not None:
                                profile_data[i].append(colsp[ci]["fnq"] + "(" + colspnew[ci]["fnq"] + ")")
                            else:
                                profile_data[i].append("-")
                        elif stat[0] == "c":
                            ii = stat[stat.find("_")+1:-2]
                            try:
                                ii = int(ii)
                                if ii < len(colsp[ci]["c"]):
                                    if stat[-1] == "0":
                                        profile_data[i].append(str(list(colsp[ci]["c"].keys())[ii]) + "(" + str(cc[ii][0]) + ")")
                                    elif stat[-1] == "1":
                                        profile_data[i].append(str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[ii]]) + "(" + str(cc[ii][1]) + ")")
                                    elif stat[-1] == "2":
                                        profile_data[i].append(str(round(100*colsp[ci]["c"][list(colsp[ci]["c"].keys())[ii]]/colsp[ci]["v"],2)) + "(" + str(round(100*cc[ii][1]/v,2)) + ")")
                                    else:
                                        profile_data[i].append("-")
                                else:
                                    profile_data[i].append("-")
                            except Exception as e:
                                traceback.print_exc()
                                profile_data[i].append("-")
                        else:
                            profile_data[i].append("-")
                            '''
                            for c in colsp[ci]:
                                #print(c, stat)
                                if c == stat:
                                    if isinstance(colsp[ci][c], float):
                                        profile_data[i].append(round(colsp[ci][c],2))
                                    elif isinstance(colsp[ci][c], str):
                                        profile_data[i].append(colsp[ci][c][:5])    # Quant, Categ
                                    elif isinstance(colsp[ci][c], type):
                                        cl = str(colsp[ci][c])[8:-2]
                                        if cl.startswith("datetime."): cl = cl[9:]
                                        profile_data[i].append(cl)    # <class 'xxx'>
                                    elif colsp[ci][c] is None:
                                        profile_data[i].append("-")
                                    else:
                                        profile_data[i].append(colsp[ci][c])
                            '''

            '''
            if maxc > profile_show_categorical:
                maxc = profile_show_categorical

            minc = len(profile_data)

            for i in range(maxc):
                profile_rows.append("Cat " + str(i + 1) + "_1")
                profile_data.append([])
                for ci in colsp:

                    if ci > 0 and (ci in colsi or print_all):  # rows_label, all or last profiled columns
                        if i < len(colsp[ci]["c"]):
                            profile_data[i*3 + minc].append(str(list(colsp[ci]["c"].keys())[i]) + "(" + str(cc[0][i]) + ")")
                        else:
                            profile_data[i*3 + minc].append("-")
                profile_rows.append("Cat " + str(i + 1) + "_2")
                profile_data.append([])
                for ci in colsp:
                    if ci > 0 and (ci in colsi or print_all):  # rows_label, all or last profiled columns
                        if i < len(colsp[ci]["c"]):
                            #profile_data[i + minc].append(str(list(colsp[ci]["c"].keys())[i]) + "(" + str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]) + ")")
                            profile_data[i*3 + minc + 1].append(str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]))
                        else:
                            profile_data[i*3 + minc + 1].append("-")
                profile_rows.append("Cat " + str(i + 1) + "_3")
                profile_data.append([])
                for ci in colsp:
                    if ci > 0 and (ci in colsi or print_all):  # rows_label, all or last profiled columns
                        if i < len(colsp[ci]["c"]):
                            #profile_data[i + minc].append(str(list(colsp[ci]["c"].keys())[i]) + "(" + str(colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]) + ")")
                            profile_data[i*3 + minc + 2].append(str(round(100*colsp[ci]["c"][list(colsp[ci]["c"].keys())[i]]/colsp[ci]["v"],2)) + "%")
                        else:
                            profile_data[i*3 + minc + 2].append("-")
            '''

            #print(profile_data)

            nrows = len(profile_data)
            ncols = len(profile_columns)

            colsi = range(1, ncols + 1)
            rowsi = range(1, nrows + 1)

            print("ncols", ncols)

            print()
            print()
            #colsp = data_profile(rowsi, colsi, profile_data, profile_columns, profile_rows, profile_rows_label)
            print_data(rowsi, colsi, profile_data, profile_columns, profile_rows, profile_rows_label, variables)


        elif sql.startswith("\pause:"):
            if "ask" in sql:
                asked = ""
                while asked != "c" and asked != "q":
                    asked = input("Paused. C for continue, D for data view, Q for quit: ").lower()
                    print(asked)
                    if asked == "d":
                        show = "Error"
                        if data:
                            #columns = [col[0] for col in c.description]
                            row_format = "{:>15}" * (len(columns) + 1)
                            nrows = len(data)
                            if nrows > 0:   #< 100
                                show = "There are {} rows. Showing all cases.".format(str(nrows))
                                show += "\n"
                                show += row_format.format("(Row)", *columns)
                                show += "\n"
                                for i, row in enumerate(data):
                                    #print(row_format.format(str(i), *row)) # not posiible to pass None (Null in db)
                                    show += row_format.format(str(i+1), *[str(r) if len(str(r)) <= 15 else str(r)[:13]+".." for r in row])    # Null to None
                                    show += "\n"
                            else:
                                print("There are {} rows. Showing first / last {} cases.".format(str(nrows), str(10)))
                                print(row_format.format("(Row)", *columns))
                                for i, row in enumerate(data[:10]):
                                    print(row_format.format(str(i+1), *[str(r) for r in row]))    # Null to None
                                print("\n","...","\n")
                                for i, row in enumerate(data[-10:]):
                                    print(row_format.format(str(nrows-10+i+1), *[str(r) for r in row]))
                        zobraz(show)
                    elif asked == "q":
                        OK = 0

        else:
            variables["$printInvRed"]["options"]["value"]("! Command was not recognized or missing arguments !")
            OK = 3

    else:
        if not variables["$silent_mode"]["options"]["value"]:
            variables["$printBlue"]["options"]["value"](variables["$db_version"]["options"]["value"] + sql + "\n")
        data_new = None
        columns_new = None
        error = 0
        try:
            c = variables["$conn"]["options"]["value"].cursor()
            #c.execute(""'{}'"".format(sql))
            c.execute(f"{sql}")
        except Exception as e:
            traceback.print_exc()
            print()
            error = 1
        if variables["$fetchall"]["options"]["value"]:
            try:
                #conn.commit()
                #print(c.statusmessage)
                data_new = c.fetchall()
                if c.description:
                    columns_new = [col[0] for col in c.description]
                #conn.close()
            except Exception as e:
                #traceback.print_exc()
                #error = 1
                pass
            finally:
                if variables["$conn"]["options"]["value"]: variables["$conn"]["options"]["value"].commit()
        if data_new or columns_new:
            if isinstance(data_new, tuple):
                #print("Converting to list")
                data = list(data_new)
            else:
                data = data_new
            columns = columns_new
            data_old = None
            columns_old = None
            colsp = {}  #reset columns profile
            # mysql returns data as tuples, not lists as sqlite3
            # this causes problems in show_data if nrows > variables["$show_cases"]["options"]["value"]*2
            # (cannoct add anzthing to tuple, probably)
            #if len(data) > 0: print("Data class", data[0].__class__)
            #print("Columns class", columns.__class__)
            show_data(data, columns, variables)
        elif not error:
            if not variables["$silent_mode"]["options"]["value"]:
                variables["$printInvGreen"]["options"]["value"]("! There are no data returned from this sql query !")
        else:
            variables["$printInvRed"]["options"]["value"]("! Error exexuting this sql query !")
            if OK: OK = 2

    # this checks dtb
    if variables["$db_version"]["options"]["value"][:5] == "MySQL":
        #print(conn.get_proto_info())
        try:
            c = variables["$conn"]["options"]["value"].cursor()
            c.execute("SELECT database();")
            data_new = c.fetchall()
            variables["$db_schema"]["options"]["value"] = data_new[0][0]
            variables["$db_version"]["options"]["value"] = f'''MySQL (`{variables["$db_schema"]["options"]["value"]}`): '''
        except Exception as e:
            traceback.print_exc()
    if variables["$db_version"]["options"]["value"][:5] == "MsSQL":
        #print(conn.get_proto_info())
        try:
            c = variables["$conn"]["options"]["value"].cursor()
            c.execute("SELECT DB_NAME();")
            data_new = c.fetchall()
            variables["$db_schema"]["options"]["value"] = data_new[0][0]
            variables["$db_version"]["options"]["value"] = f'''MsSQL ("{variables["$db_schema"]["options"]["value"]}"): '''
            #print(variables["$db_version"]["options"]["value"])
        except Exception as e:
            traceback.print_exc()
    if variables["$db_version"]["options"]["value"][:10] == "PostgreSQL":
        #print(conn.get_proto_info())
        try:
            c = variables["$conn"]["options"]["value"].cursor()
            c.execute("SELECT current_database();")
            data_new = c.fetchall()
            variables["$db_schema"]["options"]["value"] = data_new[0][0]
            variables["$db_version"]["options"]["value"] = f'''PostgreSQL ("{variables["$db_schema"]["options"]["value"]}"): '''
        except Exception as e:
            variables["$db_version"]["options"]["value"] = "None: "
            variables["$db_schema"]["options"]["value"] = None
            variables["$conn"]["options"]["value"] = None
            traceback.print_exc()
    # SELECT current_database();
    variables["$command_history"]["options"]["value"].append(sql)
    variables["$all"]["print history"]["value"] = len(variables["$command_history"]["options"]["value"])
    variables["$command_results"]["options"]["value"].append(OK)
    #sql = ""

    datas["data"] = {}
    datas["data_old"] = {}

    datas["data"]["data"] = data
    datas["data"]["columns"] = columns
    datas["data"]["colsp"] = colsp
    datas["data_old"]["data"] = data_old
    datas["data_old"]["columns"] = columns_old
    datas["data_old"]["colsp"] = colsp_old

    return variables, datas, output, logger

def main(argv):

    '''
    global conn, data, columns, data_old, columns_old, db_full_filename, folder_exists, foldername, db_version, db_schema, \
            fromm, too, stepp, randd, listt, colss, noness, noneso, command_history, colsp, \
            data_memory, columns_memory, colsp_memory, sqls, command_options, printYellow, printInvGreen, Assert, \
            printInvRed, printCom, printBlue, printRed, show_cases, rows_label, row_format_l, profile_max_categorical, \
            is_np, is_mpl, np, plt, do_mp, profile_show_categorical, default_columns_name, \
            printColor, RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END, variables
    '''

    global variables

    os.system('color')

    if is_np: print("Using numpy version:", version("numpy"))
    if is_mpl: print("Using matplotlib version:", version("matplotlib"))

    row_format_l = lambda columns: "".join([f"{{:>{columns[c]['w']}}}" for c in columns]) if isinstance(columns, dict) else "{:>15}" * (len(columns) + 1)

    conn = None
    sqls = {}
    datas  = {}
    datas["data"] = {}
    datas["data"]["data"] = None
    datas["data"]["columns"] = None
    datas["data_old"] = {}
    datas["data_old"]["data"] = None
    datas["data_old"]["columns"] = None
    folder_exists = False
    foldername = ""
    db_version = "None: "
    show_cases = 5
    print_max_default = 10
    profile_max_categorical = 100
    profile_show_categorical = 5
    rows_label = "(Row)"
    command_history = []
    default_columns_name = "Column_"
    commands = {}
    colsp = {}
    data_memory = {}
    columns_memory = {}
    colsp_memory = {}
    class_str = type("")
    class_int = type(0)
    class_float = type(0.0)

    output = None
    logger = None

    functions = set()
    functions.add("@(")
    functions.add("@int(")

    def general_function(vartest):
        ret = None
        opt = None
        print("general_function", vartest)
        return ret, opt

    def int_function(vartest):
        ret = None
        opt = None
        print("int_function", vartest)
        try:
            vartest = float(vartest)
            ret = int(vartest)
            opt = 1
        except Exception as e:
            traceback.print_exc()
        return ret, opt

    def call_function(vartest, f):
        ret = None
        opt = None
        if f == "@(":
            ret, opt = general_function(vartest)
        if f == "@int(":
            ret, opt = int_function(vartest)
        return ret, opt

    default_options = 8
    for key1 in command_options.keys():
        assert len(command_options[key1].keys()) == default_options, \
f'''Command {key1} has {len(command_options[key1].keys())} options \
instead of default {default_options}.'''
        for key2 in command_options[key1].keys():
            if key2 != "help1" and key2 != "alternative":
                assert len(command_options[key1]["name"]) == len(command_options[key1][key2]), \
f'''Command option {key1} has {len(command_options[key1]["name"])} names \
but {len(command_options[key1][key2])} '{key2}'.'''
        for key2 in command_options.keys():
            if key1 != key2:
                for a1 in command_options[key1]["alternative"]:
                    for a2 in command_options[key2]["alternative"]:
                        #assert a1 != a2, f"Command '{key1}' has the same alternative as command '{key2}': '{a1}'."
                        pass

    namespace = parseArgv(argv)
    """
    for k,v in vars(namespace).items():
        print(k, v)
    """

    #variables["$do_mp"]["options"]["value"] = False
    if isinstance(vars(namespace)["do_mp"], bool):
        variables["$do_mp"]["options"]["value"] = vars(namespace)["do_mp"]

    if variables["$do_mp"]["options"]["value"]:
        print("Multiprocessing:", variables["$do_mp"]["options"]["value"], f"(using {mp.cpu_count()} processes)")
    else:
        print("Multiprocessing:", variables["$do_mp"]["options"]["value"])

    #printInvRed("KO")
    variables["$printInvGreen"]["options"]["value"]("OK")

    if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
        logging.basicConfig(filename='log.txtx', encoding='utf-8', filemode='w', level=logging.DEBUG, format='%(asctime)s:%(name)s\n%(levelname)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')
    else:
        logging.basicConfig(filename='log.txtx', filemode='w', level=logging.DEBUG, format='%(asctime)s:%(name)s\n%(levelname)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')
    logger = logging.getLogger(__name__)
    logger.info(f'Started')


    if len(vars(namespace)["sql_files"]) > 0:
        foldername_return = variables["$foldername"]["options"]["value"]
        variables["$foldername"]["options"]["value"] = os.getcwd()  #temporarily specify default folder
        sqls = get_sql_queries_dict(vars(namespace)["sql_files"], variables["$foldername"]["options"]["value"])
        #print(sqls)
        for full_filename in sqls.keys():
            #OK_returned = 1
            for i, sql in enumerate(sqls[full_filename]):
                variables["$printCom"]["options"]["value"](f"\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\")
                #print(sql)
                #print()
                start = time.perf_counter()
                variables, datas, output, logger = do_sql(sql, command_options, variables, datas, output, logger)
                OK_returned = variables["$command_results"]["options"]["value"][-1]
                end = time.perf_counter()
                if OK_returned == 1:
                    print()
                    print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                    print()
                elif OK_returned > 1:
                    print()
                    variables["$printRed"]["options"]["value"]("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                    print()
                    time.sleep(2)
                else: break
        variables["$foldername"]["options"]["value"] = foldername_return


    if len(vars(namespace)["sql_files"]) == 0 and isinstance(vars(namespace)["interactive"], str) or vars(namespace)["interactive"]:
        print("\nEntering interactive mode. Type '\quit' to quit.")

        if variables["$conn"]["options"]["value"]:
            if variables["$db_version"]["options"]["value"][:7] == "Sqlite3":
                print(f'''Using Sqlite3 filename "{variables["$db_full_filename"]["options"]["value"]}". Use \connect sqlite3 filename' for change.''')
            elif variables["$db_version"]["options"]["value"][:5] == "MySQL":
                print(f'''Using MySQL database `{variables["$db_schema"]["options"]["value"]}`. Use '\connect mysql database' for change.''')
            elif variables["$db_version"]["options"]["value"][:5] == "MsSQL":
                print(f'''Using MsSQL database "{variables["$db_schema"]["options"]["value"]}". Use '\connect mssql database' for change.''')
            elif variables["$db_version"]["options"]["value"][:10] == "PostgreSQL":
                print(f'''Using PostgreSQL database "{variables["$db_schema"]["options"]["value"]}". Use '\connect mysql database' for change.''')
            else:
                variables["$printRed"]["options"]["value"]("Sorry, no db_version.")
        else:
            print("Database is not specified. Please use '\sqlite3 filename' for example.")

        if variables["$foldername"]["options"]["value"] != "":
            foldername = variables["$foldername"]["options"]["value"]
            print(f'''Using folder '{foldername}'.''')
        else:
            variables["$foldername"]["options"]["value"] = os.getcwd()
            foldername = variables["$foldername"]["options"]["value"]
            print(f'''Folder is not specified. Using working directory '{foldername}'.''')
        print()

        interactive_pass = 0
        sql = input(variables["$db_version"]["options"]["value"])
        OK_returned = 1

        while OK_returned:

            interactive_pass += 1

            sql_filename = "interactive pass " + str(interactive_pass)
            sqls[sql_filename] = parseText(sql, ";")
            #OK_returned = 1
            for i, sql in enumerate(sqls[sql_filename]):
                variables["$printCom"]["options"]["value"](f'''\n\\\\ SQL file '{sql_filename}' command no {str(i+1)} \\\\''')
                #print(sql)
                #print()
                start = time.perf_counter()
                variables, datas, output, logger = do_sql(sql, command_options, variables, datas, output, logger)
                OK_returned = variables["$command_results"]["options"]["value"][-1]
                end = time.perf_counter()
                if OK_returned == 1:
                    print()
                    print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                    print()
                elif OK_returned > 1:
                    print()
                    variables["$printRed"]["options"]["value"]("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                    print()
                    time.sleep(1)
                else: break
            if OK_returned:
                #print()
                #printGlobals()
                sql = input(variables["$db_version"]["options"]["value"])

    try:
        variables["$conn"]["options"]["value"].close()
    except Exception as e:
        #traceback.print_exc()
        pass
    print()


if __name__ == "__main__":

    main(sys.argv[1:])
