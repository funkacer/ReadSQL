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

def getHistogram(ci, cspi, title='Graf'):
    '''
    Takes disctionary of labels and np arrays for boxplots
    '''
    #print("Split:", colsp[ci]['split'])
    if cspi is None:
        fig, ax = plt.subplots()
        n, bins, patches = ax.hist(colsp[ci]['m'], 50, density=True, facecolor='g', alpha=0.75)
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


def getLineChartI(ci, title='Graf'):
    '''Tato funkce akceptuje df a nazvy sloupcu, vraci HTML kod vertikalniho grafu'''
    rotation = 90
    #sort_values = True
    #sort_ascending = True
    precision = 0
    cols = [col for col in sorted(colsp[ci]['c'].keys())]
    print(len(cols))
    '''
    if len(cols) > 0:
        width = 0.8/len(cols)
    else:
        width = 1
    '''
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(range(len(cols)), [colsp[ci]['c'][col] for col in cols])
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


def getBarChartI(ci, title='Graf'):
    '''Tato funkce akceptuje df a nazvy sloupcu, vraci HTML kod vertikalniho grafu'''
    rotation = 90
    #sort_values = True
    #sort_ascending = True
    precision = 0
    cols = list(colsp[ci]['c'].keys())
    if len(cols) > 0:
        width = 0.8/len(cols)
    else:
        width = 1
    fig, ax = plt.subplots(figsize = (10,5))
    rects = plt.bar(range(len(cols)), [colsp[ci]['c'][col] for col in cols])
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


def getBoxplotI(colsi, title = 'Box Plot', boxplot_showfliers = True):
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
        data_part_np = colsp[ci]['m']
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
        for cat in colsp[cspi]['c']:
            colsp[cspi]['cats'][cat] = []  #find rows for every category
            #print(cat)
        for av in colsp[cspi]["av"]:
            colsp[cspi]['cats'][av['value']].append(av['row'])

    return [cspi, colsp[cspi]['cats']]


def data_split_prep(colspi):
    global colsp
    for cspi in colspi:
        colsp[cspi]['cats'] = {}
        for cat in colsp[cspi]['c']:
            colsp[cspi]['cats'][cat] = []  #find rows for every category
            #print(cat)
        for av in colsp[cspi]["av"]:
            colsp[cspi]['cats'][av['value']].append(av['row'])


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
                    for i in colsp[ci]["av"]:
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
                    for i in range(len(colsp[ci]["av"])-len(filterr)):
                        filterr.append(False)
                    #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                    colsp[ci]['split'][cspis][cat] = colsp[ci]["av"][filterr]
                    if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["av"]['value'].mean(),2))
                    elif colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["av"]['value'].max())
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
                for i in colsp[ci]["av"]:
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
                for i in range(len(colsp[ci]["av"])-len(filterr)):
                    filterr.append(False)
                #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                colsp[ci]['split'][cspis][cat] = colsp[ci]["av"][filterr]
                if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["av"]['value'].mean(),2))
                elif colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["av"]['value'].max())
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


def data_split(colsi, colspi, combine = True):
    global colsp

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
                    for i in colsp[ci]["av"]:
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
                    for i in range(len(colsp[ci]["av"])-len(filterr)):
                        filterr.append(False)
                    #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                    colsp[ci]['split'][cspis][cat] = colsp[ci]["av"][filterr]
                    if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["av"]['value'].mean(),2))
                    elif colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time":
                        print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["av"]['value'].max())
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
                for i in colsp[ci]["av"]:
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
                for i in range(len(colsp[ci]["av"])-len(filterr)):
                    filterr.append(False)
                #colsp[ci]['split'][cspi][cat] = colsp[ci]["av"][filterr]
                colsp[ci]['split'][cspis][cat] = colsp[ci]["av"][filterr]
                if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],round(colsp[ci]['split'][cspis][cat]['value'].mean(),2),round(colsp[ci]["av"]['value'].mean(),2))
                elif colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time":
                    print(colsp[ci]['name'], cat, colsp[ci]['split'][cspis][cat][:5],colsp[ci]['split'][cspis][cat]['value'].max(),colsp[ci]["av"]['value'].max())
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


def data_profile(data, columns, variables, colsp, rowsi, colsi, purge = False):
    #global data, variables, colsp
    import numpy as np

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
        colsp[ci]["smd2"] = None
        colsp[ci]["smd3"] = None
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
            colsp[ci]["smd2"] = 0
            colsp[ci]["smd3"] = 0
            for mi in m:
                colsp[ci]["smd2"] += (mi - colsp[ci]["mean"])**2
                colsp[ci]["smd3"] += (mi - colsp[ci]["mean"])**3
            colsp[ci]["var"] = None
            colsp[ci]["std"] = None
            if colsp[ci]["valid"] > 0:
                colsp[ci]["var"] = colsp[ci]["smd2"] / colsp[ci]["valid"]
                colsp[ci]["std"] = (colsp[ci]["smd2"] / colsp[ci]["valid"])**0.5
            colsp[ci]["skew"] = None
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
    import numpy as np

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
    colsp[ci]["smd2"] = None
    colsp[ci]["smd3"] = None
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
        colsp[ci]["smd2"] = 0
        colsp[ci]["smd3"] = 0
        for mi in m:
            colsp[ci]["smd2"] += (mi - colsp[ci]["mean"])**2
            colsp[ci]["smd3"] += (mi - colsp[ci]["mean"])**3
        colsp[ci]["var"] = None
        colsp[ci]["std"] = None
        if colsp[ci]["valid"] > 0:
            colsp[ci]["var"] = colsp[ci]["smd2"] / colsp[ci]["valid"]
            colsp[ci]["std"] = (colsp[ci]["smd2"] / colsp[ci]["valid"])**0.5
        colsp[ci]["skew"] = None
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


def find_columns(colss):
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
            if value[0] in ["-","0","1","2","3","4","5","6","7","8","9"] and dstring not in value:
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


def data_fill(fill_formats = {}, fill_nones = {}):
    global data

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
            colsi = find_columns([colss])
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
    print()


def data_select(data, columns, fromm, too, stepp, randd, listt, colss):
    #global fromm, too, stepp, randd, listt, colss, listi
    nrows = len(data)
    ncols = len(columns)
    colsi = range(1, ncols + 1)
    if len(colss) > 0:
        colsi = find_columns(colss)
    nonesi = []
    if len(noness) > 0:
        nonesi = find_columns(noness)
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


def parseVariable(variables, command, options, n, vartest):
    # get variables in context
    ret = None
    opt = None
    variable = None
    print("vartest", vartest)
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
                print(f"Getting context for variable '{variable}' in command '{command}' and option '{options[n]}':")
                for contexttest in variables[variable]:
                    #print(variables[variable][contexttest])
                    if command in variables[variable][contexttest] or contexttest == "user":
                        contexts.append(contexttest)
                for context in contexts:
                    print(f"Command '{command}' test passed with context '{context}'!")
                    print(variables[variable][contexttest])
                    print(options)
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
                        if variables[variable][context]["value"] is not None:
                            if variable == "$now":
                                ret = str(variables["$now"]["user"]["value"](None))
                            else:
                                ret = str(variables[variable][context]["value"]) # must look like string input from user
                        else:
                            ret = None
        elif vartest[0] == "@":
            # function
            for f in functions:
                print("vartest[:len(f)]", vartest[:len(f)])
                if vartest[:len(f)] == f and vartest[-1] == ")":
                    print("vartest[len(f):-1]", vartest[len(f):-1])
                    ret, opt = call_function(vartest[len(f):-1], f)
    return ret, opt


def parseCommand(command_line, variables, command_options):
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
        print(c[0], c[1])
        command = c[0]
        command_line = command_line_original[len(c[1]):]
        command_line = "=".join(parseText(command_line, "="))
        #command_line = ",".join(parseText(command_line, " "))
        print("Command line:", command_line)
        #command_line_list = parseText(command_line, ",")
        command_line_list = [l.strip() for l in parseText(command_line, ",", do_strip = False)]
        print("Command line list:", command_line_list)

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
                    variables["$printRed"]["options"]["value"](f'''Unknown option '{cll[0]}'. I will not use your '{cll[1]}' value in any way.''')
                    execute = False
            elif cl != "":
                if i < len (command_options[command]["name"]):
                    #print(f'''I will use '{cl}' for option '{command_options[c]["name"][i]}'.''')
                    options[command_options[command]["name"][i]] = cl
                else:
                    variables["$printRed"]["options"]["value"](f'''Too many options given. I will not use your '{cl}' value in any way.''')

        for i, z in enumerate(zip(command_options[command]["name"], command_options[command]["required"], command_options[command]["default"], command_options[command]["type"])):
            n, r, d, t = z[0], z[1], z[2], z[3]
            #print(f'''i:{i}, name:{n}, required:{r}, default:{d}, type:{t}''')
            if r:
                #assert command_options[command]["name"][i] in options
                if n not in options:
                    variables["$printRed"]["options"]["value"](f'''Missing required argument '{n}'. Command not executed.''')
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
                    sTxt = f"Value '{options[n]}' is not valid for option '{n}'. Use one of these options: {t}."
                    variables["$Assert"]["options"]["value"](bCond, sTxt)
                    if not bCond:
                        execute = False
                        break
                elif t == "str":
                    #options[n] = options[n].strip('"')
                    #print("options[n]", options[n])
                    var, opt = parseVariable(variables, command, options, n, str(options[n]))
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
                    var, opt = parseVariable(variables, command, options, n, str(options[n]))
                    if opt:
                        options[n] = var
                    if opt == 0:
                        result_message = f"Option '{n}' should be integer but is '{options[n]}', which is not a variable in context of {command}. Probably not doing what expected!"
                    else:
                        result_message = f"Option '{n}' should be integer but is '{options[n]}'. Probably not doing what expected!"
                    try:
                        options[n] = int(options[n])
                    except Exception as e:
                        traceback.print_exc()
                    variables["$Assert"]["options"]["value"](isinstance(options[n], int), result_message)
                    if not isinstance(options[n], int):
                        #options[n] = d
                        execute = False
                    #print(f"Parse option '{n}' as integer:", options[n])
                elif t == "intlist":
                    var, opt = parseVariable(variables, command, options, n, str(options[n]))
                    if opt:
                        options[n] = var
                    variables["$Assert"]["options"]["value"](options[n][0] == "[" and options[n][-1] == "]", "Lists must be enclosed with []. Probably not doing what expected!")
                    options_list_line = options[n][1:-1]
                    #options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = []
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        l_new = None
                        var, opt = parseVariable(variables, command, options, n, str(l_old))
                        if opt:
                            l_old = var
                        if opt == 0:
                            result_message = f"Option '{n}' should be integer but is '{options[n]}', which is not a variable in context of {command}. Probably not doing what expected!"
                        else:
                            result_message = f"Option '{n}' should be integer but is '{options[n]}'. Probably not doing what expected!"
                        try:
                            l_new = int(l_old)
                        except Exception as e:
                            traceback.print_exc()
                        variables["$Assert"]["options"]["value"](isinstance(l_new, int), result_message)
                        if isinstance(l_new, int) and l_new not in lst_new: lst_new.append(l_new)
                    options[n] = lst_new
                elif t == "strlist":
                    var, opt = parseVariable(variables, command, options, n, str(options[n]))
                    #print("var", var)
                    if opt:
                        options[n] = var
                    variables["$Assert"]["options"]["value"](options[n][0] == "[" and options[n][-1] == "]", "Lists must be enclosed with []. Probably not doing what expected!")
                    #print(options[n])
                    options_list_line = options[n][1:-1]
                    #options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = []
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        var, opt = parseVariable(variables, command, options, n, str(l_old))
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
                        options[n] = d
                elif t == "dictlist":
                    var, opt = parseVariable(variables, command, options, n, str(options[n]))
                    if opt:
                        options[n] = var
                    variables["$Assert"]["options"]["value"](options[n][0] == "{" and options[n][-1] == "}", "Dicts must be enclosed with {}. Probably not doing what expected!")
                    options_list_line = options[n][1:-1]
                    #print("options_list_line", options_list_line)
                    options_list_line = ":".join(parseText(options_list_line, ":"))
                    #options_list_line = ",".join(parseText(options_list_line, " "))
                    lst_old = parseText(options_list_line, ",")
                    lst_new = {}
                    #print("lst_old", lst_old)
                    for l_old in lst_old:
                        #lst = parseText(l_old, ":", do_strip = False)
                        lst = [l.strip() for l in parseText(l_old, ":", do_strip = False)]
                        print("lst:", lst)
                        # check if list on any side
                        #print(lst[0].strip().__class__)
                        l, r, ll, rr = None, None, None, None
                        if len(lst) > 1:
                            #lst[0] = lst[0].strip()
                            #lst[1] = lst[1].strip()
                            var, opt = parseVariable(variables, command, options, n, str(lst[0]))
                            if opt:
                                lst[0] = var
                            if lst[0][0] == '[' and lst[0][-1] == ']':
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
                            var, opt = parseVariable(variables, command, options, n, str(lst[1]))
                            if opt:
                                lst[1] = var
                            if lst[1] is not None:
                                if lst[1][0] == '[' and lst[1][-1] == ']':
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
                            if l is not None and rr is None:
                                lst_new[l] = r
                            if ll is not None and rr is None:
                                for l in ll:
                                    var, opt = parseVariable(variables, command, options, n, str(l))
                                    if opt:
                                        l = var
                                    if l[0] == '"' and l[-1] == '"':
                                        l = l.strip('"')
                                    elif l[0] == "'" and l[-1] == "'":
                                        l = l.strip("'")
                                    lst_new[l] = r
                            elif ll is not None and rr is not None:
                                # make two lists
                                variables["$Assert"]["options"]["value"](len(ll) == len(rr), f"Lists {ll}:{rr} in dict '{n}' not of the same size. Check results carefully!!!")
                                print(list(zip(ll, rr)))
                                for l, r in zip(ll, rr):
                                    var, opt = parseVariable(variables, command, options, n, str(l))
                                    if opt:
                                        l = var
                                    if l[0] == '"' and l[-1] == '"':
                                        l = l.strip('"')
                                    elif l[0] == "'" and l[-1] == "'":
                                        l = l.strip("'")
                                    var, opt = parseVariable(variables, command, options, n, str(r))
                                    if opt:
                                        r = var
                                    if len(r) == 0:
                                        r = ""
                                    elif r[0] == '"' and r[-1] == '"':
                                        r = r.strip('"')
                                    elif r[0] == "'" and r[-1] == "'":
                                        r = r.strip("'")
                                    lst_new[l] = r
                        else:
                            variables["$printRed"]["options"]["value"](f"Error parsing dictlist option {lst}. Check results carefully!!!")
                    options[n] = lst_new

        print("Command:", command)
        print("Options:", options)
        print("Execute:", execute)

        if execute: break

    if not execute:
        command = ""
        options = []
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

def get_sql_queries_dict(lst, folder_exists, foldername):
    sqls_local = {}
    for sql_filename in lst:
        #print("SQL file:", sql_file)
        file_exists, full_filename = check_filename(sql_filename, folder_exists, foldername)
        #print("Check if file exists:", sql_file_exists)
        if file_exists:
            with open(full_filename, mode="r", encoding="utf-8") as f:
                sql = f.read()
                #print("SQL file query:")
                #print(sql.strip(), sql.count(";"))
                sqls_local[full_filename] = parseText(sql, ";")
        else:
            variables["$printRed"]["options"]["value"](f'''! SQL file '{full_filename}' does not exist !''')
    return sqls_local

def check_foldername(foldername, foldername_old):
    folder_exists = False
    full_foldername = None
    if not os.path.isabs(foldername):
        if foldername_old:
            full_foldername = os.path.join(foldername_old, foldername)
            folder_exists = os.path.isdir(full_foldername)
        else:
            full_foldername = os.path.join(os.getcwd(), foldername)
            folder_exists = os.path.isdir(full_foldername)
    else:
        folder_exists = os.path.isdir(foldername)
        full_foldername = foldername
    return folder_exists, full_foldername

def check_filename(filename, folder_exists, folder_name):
    file_exists = False
    full_filename = None
    if folder_exists and not os.path.isabs(filename):
        full_filename = os.path.realpath(os.path.join(folder_name, os.path.expanduser(filename)))
    else:
        full_filename = filename
    file_exists = os.path.isfile(full_filename)
    #print(full_filename)
    return file_exists, full_filename

def printGlobals():
    print()
    print("conn", variables["$conn"]["options"]["value"].__class__, variables["$conn"]["options"]["value"])
    print("data", data.__class__)
    print("columns", columns.__class__)
    print("data_old", data_old.__class__)
    print("columns_old", columns_old.__class__)
    print("folder_exists", variables["$folder_exists"]["options"]["value"].__class__, variables["$folder_exists"]["options"]["value"])
    print("folder_name", variables["$folder_name"]["options"]["value"].__class__, variables["$folder_name"]["options"]["value"])
    print("db_version", variables["$db_version"]["options"]["value"].__class__, variables["$db_version"]["options"]["value"])

def do_sql(sql, variables, command_options, data, columns):

    '''
    Perform sql query or user command
    Inputs:
    sql - string - (sql) querry or command (starting with "\")

    global variable description:
    conn: Connection variable (conn = sqlite3.connect(":memory:"), c = conn.cursor(), c.execute(f"{sql}"))
    data: tuple or list of data rows
    columns: tuple or list of data columns
    data_old: tuple or list of data rows (shallow or deep copy)
    columns_old: tuple or list of columns (shallow or deep copy)
    db_full_filename: filename incl folder of sqlite3 db (Using Sqlite3 filename "{db_full_filename}". Use \connect sqlite3 filename' for change)
    folder_exists: bool (folder_exists = os.path.isdir(foldername))
    folder_name: string (f"Using folder '{folder_name}'.")
    db_version: string prompting user with db name (db_version = f"Sqlite3 ({db_full_filename}): ")
    db_schema, \
            fromm, too, stepp, randd, listt, colss, noness, noneso, variables, command_history, colsp, \
            data_memory, columns_memory, colsp_memory


    global conn, data, columns, data_old, columns_old, folder_exists, folder_name, db_version, \
            fromm, too, stepp, randd, listt, colss, noness, noneso, variables, command_history, colsp, \
            data_memory, columns_memory, colsp_memory
    '''

    global data_old, columns_old, \
           fromm, too, stepp, randd, listt, colss, noness, noneso, colsp, \
           data_memory, columns_memory, colsp_memory

    time.sleep(variables["$sleep"]["options"]["value"])

    OK = 1
    if sql.startswith("\\"):
        command, options = parseCommand(sql, variables, command_options)
        print(command, options)

        if command == "quit" or command == "q":
            OK = 0

        elif command == "#":
            title = options.get("title")
            note = options.get("note")
            title_color = options.get("title_color")
            note_color = options.get("note_color")
            if title: # excluse empty string to show title
                    if title_color:
                        cc = colorCode(title_color)
                        variables["$printColor"]["options"]["value"](title, cc)
                    else:
                        cc = INVGREEN
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
                file_exists, full_filename = check_filename(db_filename, variables["$folder_exists"]["options"]["value"], variables["$folder_name"]["options"]["value"])
                variables["$db_full_filename"]["options"]["value"] = os.path.join(variables["$folder_name"]["options"]["value"], full_filename)
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
            if port is not None: connstring += f'PORT={port}'
            if database is not None: connstring += f'Database={database};'
            if user is not None: connstring += f'UID={user};'
            if password is not None: connstring += f'PWD={password};'
            if option is not None: connstring += f'{option};'

            try:
                print("Using pyodbc version:", version("pyodbc"))
                import pyodbc
                try:
                    variables["$conn"]["options"]["value"] = pyodbc.connect(connstring)
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
            set_variable_type = variables["$parse_value_type"]["options"]["value"]

            for vn in set_variable_names:
                if len(vn) > 0:
                    print(vn)
                    if vn[0] != "$":
                        v = "$" + vn
                    else:
                        v = vn
            if v not in variables:
                variables[v] = {}
                variables[v]["shorts"] = []
            variables[v]["user"] = {}
            variables[v]["user"]["value"] = set_variable_names[vn]


        elif command == "print variables easy" or command == "print variables":

            print_variable_names = options.get("names")

            if print_variable_names is not None:
                pass
            else:
                #print(",\n".join(str(v) for v in [vi for vi in variables.items()]))
                print(",\n".join(str(v) for v in variables.items()))



        elif command == "folder":
            variables["$folder_exists_old"]["options"]["value"] = variables["$folder_exists"]["options"]["value"]
            variables["$folder_name_old"]["options"]["value"] = variables["$folder_name"]["options"]["value"]
            #folder_name = sql[len("\folder:"):]
            variables["$folder_name"]["options"]["value"] = options["foldername"]
            #folder = os.path.isdir(folder_name)
            variables["$folder_exists"]["options"]["value"], full_foldername = check_foldername(variables["$folder_name"]["options"]["value"], variables["$folder_name_old"]["options"]["value"])
            if variables["$folder_exists"]["options"]["value"]:
                variables["$printInvGreen"]["options"]["value"](f'''Using folder '{full_foldername}'.''')
                variables["$folder_name"]["options"]["value"] = full_foldername
            else:
                if variables["$folder_exists_old"]["options"]["value"]:
                    variables["$printInvRed"]["options"]["value"](f'''Folder '{variables["$folder_name"]["options"]["value"]}' does not exist. Using current folder '{variables["$folder_name_old"]["options"]["value"]}'.''')
                    variables["$folder_exists"]["options"]["value"] = variables["$folder_exists_old"]["options"]["value"]
                    variables["$folder_name"]["options"]["value"] = variables["$folder_name_old"]["options"]["value"]
                else:
                    # folder_name_old is None if sql imported file has wrong \folder command
                    variables["$printInvRed"]["options"]["value"](f'''Folder '{variables["$folder_name"]["options"]["value"]}' does not exist. Using working directory '{os.getcwd()}'.''')
                    variables["$folder_name"]["options"]["value"] = os.getcwd()
                OK = 2

        elif command == "read":
            colsp = {}  #reset columns profile
            read_filename = options["filename"]
            read_delimiter = options["delimiter"]
            if options.get("lines"):
                read_lines = options["lines"]
            else:
                read_lines = 0
            if options.get("text_qualifier"):
                read_text_qualifier = options["text_qualifier"]
            else:
                read_text_qualifier = None
            read_columns = options.get("read_columns")
            strip_columns = options.get("strip_columns")
            file_exists, full_filename = check_filename(read_filename, variables["$folder_exists"]["options"]["value"], variables["$folder_name"]["options"]["value"])
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
                        cc = 0
                        rest = len(parsed_line)
                        while rest > 0:
                            rest = int(rest/(10**cc))
                            #print(rest)
                            cc += 1
                        for i, c in enumerate(parsed_line):
                            if read_text_qualifier and len(c) >= 2:
                                if c[0] == read_text_qualifier and c[-1] == read_text_qualifier: c = c[1:-1]
                                #print(c)
                            if strip_columns: c = c.strip()
                            if read_columns and c != "":
                                columns_new.append(c)
                            else:
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
                                columns_new.append(c)
                            #columns_new.append(c)
                        if read_columns: data_line = f.readline()
                        '''
                        else:
                            # just determine number of columns from the first row
                            # column names are created at the end (in case more columns occure)
                            if data_line[-1] == "\n": data_line = data_line[:-1]
                            if read_text_qualifier:
                                parsed_line = parseText(data_line, read_delimiter, [read_text_qualifier], False)
                            else:
                                parsed_line = data_line.split(read_delimiter)
                            cc = 0
                            rest = len(parsed_line)
                            while rest > 0:
                                rest = int(rest/(10**cc))
                                #print(rest)
                                cc += 1
                            for i in range(len(parsed_line)):
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
                                columns_new.append(c)
                        '''
                        row = 1
                        len_columns = len(columns_new)
                        max_columns = len(columns_new)
                        #print("."+data_line+".")
                        while data_line:
                            sys.stdout.write(u"\u001b[1000D" +  "Lines read: " + str(row) + " ")
                            sys.stdout.flush()
                            #print("."+data_line+".")
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
                            if read_lines == row: break
                            #print(row_new)
                            row += 1
                            #time.sleep(1)
                            data_line = f.readline()
                    #print(data_new)
                    print()
                    if is_error:
                        if read_columns:
                            # add new column names only
                            for i in range(len_columns, max_columns):
                                cc = 0
                                rest = max_columns
                                while rest > 0:
                                    rest = int(rest/(10**cc))
                                    #print(rest)
                                    cc += 1
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
                                columns_new.append(c)
                        else:
                            # create all column names again
                            columns_new = []
                            for i in range(max_columns):
                                cc = 0
                                rest = max_columns
                                while rest > 0:
                                    rest = int(rest/(10**cc))
                                    #print(rest)
                                    cc += 1
                                c = default_columns_name + f"{(i+1):0{(cc-1)}}"
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
                    if error > 0:
                        variables["$printInvRed"]["options"]["value"](f"ERRORs in TOTAL {error}. Check carefully!!!")
                        print(max_columns, len_columns)
                    if len(data_new) > 0 or len(columns_new) > 0:
                        data = data_new
                        columns = columns_new
                        data_old = None
                        columns_old = None
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
            file_exists, full_filename = check_filename(export_filename, variables["$folder_exists"]["options"]["value"], variables["$folder_name"]["options"]["value"])
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
            sql_filename = options["filename"]
            '''
            file_exists, full_filename = check_filename(sql_filename)
            #print("Check if file exists:", sql_file_exists)
            if file_exists:
                with open(full_filename, mode="r", encoding="utf-8") as f:
                    sql = f.read()
                    #print("SQL file query:")
                    #print(sql.strip(), sql.count(";"))
                    sqls_load = parseText(sql, ";")
                for i, sql in enumerate(sqls_load):
                    variables["$printCom"]["options"]["value"](f"\n\\\\ SQL file '{full_filename}' loaded command no {str(i+1)} \\\\")
                    do_sql(sql)
            else:
                variables["$printRed"]["options"]["value"](f"! SQL file '{full_filename}' does not exist !")
            '''
            sqls_load = get_sql_queries_dict([sql_filename], variables["$folder_exists"]["options"]["value"], variables["$folder_name"]["options"]["value"])
            for full_filename in sqls_load.keys():
                #OK_returned = 1
                for i, sql_load in enumerate(sqls_load[full_filename]):
                    variables["$printCom"]["options"]["value"](f"\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\")
                    #print(sql)
                    #print()
                    start = time.perf_counter()
                    variables, data, columns = do_sql(sql_load, variables, command_options, data, columns)
                    OK_returned = variables["$command_results"]["options"]["value"][-1]
                    end = time.perf_counter()
                    print()
                    if OK_returned == 1:
                        print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                    elif OK_returned > 1:
                        variables["$printRed"]["options"]["value"]("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                        time.sleep(2)
                    else: break


        elif command == "split":
            colss = options.get("columns")
            colssp = options.get("split")
            if colss is not None:
                colsi = find_columns(colss)
            else:
                colsi = [ci for ci in range(1,len(columns)+1)]
            colsai = colsi
            if colssp is not None:
                colspi = find_columns(colssp)
            colsai = colsi + colspi
            data_profile(range(1, len(data) + 1), colsai)
            colsif = [ci for ci in colsi if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float"]
            print("colsif (final colsi):", colsif)
            colspif = [cspi for cspi in colspi if colsp[cspi]['t'] == "Categorical"]
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
                data_split_prep(colspif)
                data_split(colsif, colspif, True)
            #print(colsp[colspif[0]]['cats'])
            #data_split0(colspiff)
            #data_split(colsif, colspif, True)

            split_data = []
            split_rows = []
            #split_rows = ["Type", "Class", "Valids", "Nones", "Valid %", "Sum", "Min", "Max", "Mean", "Q1", "Median", "Q3", "Range", "IQR", "Variance", "STD", "Skew", "Unique", "FirstCat"]
            split_rows_label = ' - '.join([colsp[cspi]['name'] for cspi in colspif])    #TODO: user split variable
            #stats = ["t", "cl", "v", "n", "v%", "sum", "min", "max", "mean", "q1", "q2", "q3", "ran", "iqr", "var", "std", "skw","uni", "fnq"]
            stats = ["t","v","n"]
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
                colsi = find_columns(colss)
            else:
                colsi = [ci for ci in range(1,len(columns)+1)]
            colsai = colsi
            if colssp is not None:
                colspi = find_columns(colssp)
            colsai = colsi + colspi
            data_profile(range(1, len(data) + 1), colsai)
            colsif = [ci for ci in colsi if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float"]
            print("colsif (final colsi):", colsif)
            colspif = [cspi for cspi in colspi if colsp[cspi]['t'] == "Categorical"]
            data_split(colsif, colspif, True)

            if is_mpl:
                print("Go to plot window...")
                for ci in colsif:
                    if title is not None:
                        titlee = title + ": " + colsp[ci]["name"]
                    else:
                        titlee = colsp[ci]["name"]
                    if colspif is None:
                        getHistogram(ci, None, titlee)
                    else:
                        for cspi in colspif:
                            getHistogram(ci, cspi, titlee)
                print("All windows closed...")
            else:
                print("Go plot support...")

        elif command == "graph linechart":
            colss = options.get("columns")
            title = options.get("title")
            if colss is not None:
                colsi = find_columns(colss)
            else:
                colsi = [ci for ci in range(1,len(columns)+1) if colsp[ci]['t'] == "Datetime" or colsp[ci]['t'] == "Date" or colsp[ci]['t'] == "Time"]
            #print(colsi)
            if is_mpl:
                for ci in colsi:
                    if title is not None:
                        titlee = title + ": " + colsp[ci]["name"]
                    else:
                        titlee = colsp[ci]["name"]
                    getLineChartI(ci, titlee)


        elif command == "graph boxplot":
            colss = options.get("columns")
            title = options.get("title")
            boxplot_showfliers = options.get("show_fliers")
            if colss is not None:
                colsi = find_columns(colss)
            else:
                colsi = [ci for ci in range(1,len(columns)+1) if colsp[ci]['t'] == "Integer" or colsp[ci]['t'] == "Float"]
            #print("Colsi", colsi)
            if is_mpl:
                getBoxplotI(colsi, title, boxplot_showfliers)


        elif command == "graph barchart":
            colss = options.get("columns")
            title = options.get("title")
            if colss is not None:
                colsi = find_columns(colss)
            else:
                colsi = [ci for ci in range(1,len(columns)+1) if colsp[ci]['t'] == "Categorical"]
            #print(colsi)
            if is_mpl:
                for ci in colsi:
                    if title is not None:
                        titlee = title + ": " + colsp[ci]["name"]
                    else:
                        titlee = colsp[ci]["name"]
                    getBarChartI(ci, titlee)


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
                        if colsp[ci]["class"] is not class_str:
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
                        columns_create += "int"
                    elif colsp[ci]["type"] == "Float":
                        columns_create += "real"   # this format is Approximate numerics
                        #columns_create += "decimal(10,3)"
                    elif colsp[ci]["type"] == "Datetime":
                        columns_create += "datetime"
                        if colsp[ci]["class"] is not class_str:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    data[ri-1][ci-1] = str(data[ri-1][ci-1])
                    elif colsp[ci]["type"] == "Date":
                        columns_create += "date"
                        if colsp[ci]["class"] is not class_str:
                            #print("'" + colsp[ci]["name"] + "'", "is not class string - converting...")
                            for ri in range(1, len(data) + 1):
                                if data[ri-1][ci-1] is not None and not isinstance(data[ri-1][ci-1], str):
                                    if isinstance(data[ri-1], tuple): data[ri-1] = list(data[ri-1])
                                    data[ri-1][ci-1] = str(data[ri-1][ci-1])
                    elif colsp[ci]["type"] == "Time":
                        columns_create += "time"
                        if colsp[ci]["class"] is not class_str:
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
                        columns_create += "ntext"
                        if colsp[ci]["class"] is not class_str:
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

            if options["what"] == "columns":

                #print(", ".join([str(c) for c in columns]))
                print(columns)

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
                        cc = INVGREEN
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

            data_fill(fill_formats, fill_nones)
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
                    cc = INVGREEN
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

            rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss)
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
                    cc = INVGREEN
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

            rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss)

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
                    if var in ["$time", "$decimal_separator", "$thousands_separator", "$datetime", "$date"]:
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

            rowsi, colsi, listi, fromm, too, stepp, randd, listt, colss = data_select(data, columns, fromm, too, stepp, randd, listt, colss)

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
    return variables, data, columns

def main(argv):

    global conn, data, columns, data_old, columns_old, db_full_filename, folder_exists, folder_name, db_version, db_schema, \
            fromm, too, stepp, randd, listt, colss, noness, noneso, variables, command_history, colsp, \
            data_memory, columns_memory, colsp_memory, sqls, command_options, printYellow, printInvGreen, Assert, \
            printInvRed, printCom, printBlue, printRed, show_cases, rows_label, row_format_l, profile_max_categorical, \
            is_np, is_mpl, np, plt, do_mp, profile_show_categorical, default_columns_name, \
            printColor, RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END

    #do_mp = True
    #do_mp = False

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

    if is_np: print("Using numpy version:", version("numpy"))
    if is_mpl: print("Using matplotlib version:", version("matplotlib"))

    #from okno import zobraz

    #\033[34m too dark blue text
    os.system('color')
    RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END = '\033[91m', '\033[33m', '\033[92m', '\033[96m', '\033[4m', '\033[97m\033[42m', '\033[97m\033[101m', '\033[0m'
    printRed = lambda sTxt: print(RED + sTxt + END)
    printGreen = lambda sTxt: print(GREEN + sTxt + END)
    printYellow = lambda sTxt: print(YELLOW + sTxt + END)
    printBlue = lambda sTxt: print(BLUE + sTxt + END)
    printCom = lambda sTxt: print(COM + sTxt + END)
    printInvGreen = lambda sTxt: print(INVGREEN + sTxt + END)
    printInvRed = lambda sTxt: print(INVRED + sTxt + END)
    Assert = lambda bCond=False, sTxt='': printRed(sTxt) if not bCond else None

    printColor = lambda sTxt, mColor: print(mColor + sTxt + END)

    #printInvRed("KO")
    printInvGreen("OK")

    row_format_l = lambda columns: "".join([f"{{:>{columns[c]['w']}}}" for c in columns]) if isinstance(columns, dict) else "{:>15}" * (len(columns) + 1)

    conn = None
    sqls = {}
    data = None
    columns = None
    data_old = None
    columns_old = None
    folder_exists = False
    folder_name = ""
    db_version = "None: "
    show_cases = 5
    print_max_default = 10
    profile_max_categorical = 100
    profile_show_categorical = 5
    rows_label = "(Row)"
    command_history = []
    default_columns_name = "Column_"
    commands = {}
    variables = {}
    colsp = {}
    data_memory = {}
    columns_memory = {}
    colsp_memory = {}
    class_str = type("")
    class_int = type(0)
    class_float = type(0.0)

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


    variables["$db_full_filename"] = {}
    variables["$db_full_filename"]["shorts"] = []
    variables["$db_full_filename"]["options"] = {}
    variables["$db_full_filename"]["options"]["value"] = ""

    variables["$mssql_host"] = {}
    variables["$mssql_host"]["shorts"] = []
    variables["$mssql_host"]["options"] = {}
    variables["$mssql_host"]["options"]["value"] = socket.gethostname()

    variables["$profile_show_categorical"] = {}
    variables["$profile_show_categorical"]["shorts"] = []
    variables["$profile_show_categorical"]["options"] = {}
    variables["$profile_show_categorical"]["options"]["value"] = 5

    variables["$do_mp"] = {}
    variables["$do_mp"]["shorts"] = []
    variables["$do_mp"]["options"] = {}
    variables["$do_mp"]["options"]["value"] = False

    variables["$row_format_l"] = {}
    variables["$row_format_l"]["shorts"] = []
    variables["$row_format_l"]["options"] = {}
    variables["$row_format_l"]["options"]["value"] = lambda columns: "".join([f"{{:>{columns[c]['w']}}}" for c in columns]) if isinstance(columns, dict) else "{:>15}" * (len(columns) + 1)

    variables["$rows_label"] = {}
    variables["$rows_label"]["shorts"] = []
    variables["$rows_label"]["options"] = {}
    variables["$rows_label"]["options"]["value"] = "(Row)"

    variables["$show_cases"] = {}
    variables["$show_cases"]["shorts"] = []
    variables["$show_cases"]["options"] = {}
    variables["$show_cases"]["options"]["value"] = 5

    variables["$command_history"] = {}
    variables["$command_history"]["shorts"] = []
    variables["$command_history"]["options"] = {}
    variables["$command_history"]["options"]["value"] = []

    variables["$command_results"] = {}
    variables["$command_results"]["shorts"] = []
    variables["$command_results"]["options"] = {}
    variables["$command_results"]["options"]["value"] = []


    RED, YELLOW, GREEN, BLUE, COM, INVGREEN, INVRED, END = '\033[91m', '\033[33m', '\033[92m', '\033[96m', '\033[4m', '\033[97m\033[42m', '\033[97m\033[101m', '\033[0m'

    variables["$printRed"] = {}
    variables["$printRed"]["shorts"] = []
    variables["$printRed"]["options"] = {}
    variables["$printRed"]["options"]["value"] = lambda sTxt: print(RED + sTxt + END)

    variables["$printGreen"] = {}
    variables["$printGreen"]["shorts"] = []
    variables["$printGreen"]["options"] = {}
    variables["$printGreen"]["options"]["value"] = lambda sTxt: print(GREEN + sTxt + END)

    variables["$printYellow"] = {}
    variables["$printYellow"]["shorts"] = []
    variables["$printYellow"]["options"] = {}
    variables["$printYellow"]["options"]["value"] = lambda sTxt: print(YELLOW + sTxt + END)

    variables["$printBlue"] = {}
    variables["$printBlue"]["shorts"] = []
    variables["$printBlue"]["options"] = {}
    variables["$printBlue"]["options"]["value"] = lambda sTxt: print(BLUE + sTxt + END)

    variables["$printCom"] = {}
    variables["$printCom"]["shorts"] = []
    variables["$printCom"]["options"] = {}
    variables["$printCom"]["options"]["value"] = lambda sTxt: print(COM + sTxt + END)

    variables["$printInvGreen"] = {}
    variables["$printInvGreen"]["shorts"] = []
    variables["$printInvGreen"]["options"] = {}
    variables["$printInvGreen"]["options"]["value"] = lambda sTxt: print(INVGREEN + sTxt + END)

    variables["$printInvRed"] = {}
    variables["$printInvRed"]["shorts"] = []
    variables["$printInvRed"]["options"] = {}
    variables["$printInvRed"]["options"]["value"] = lambda sTxt: print(INVRED + sTxt + END)

    variables["$printColor"] = {}
    variables["$printColor"]["shorts"] = []
    variables["$printColor"]["options"] = {}
    variables["$printColor"]["options"]["value"] = lambda sTxt, mColor: print(mColor + sTxt + END)


    variables["$Assert"] = {}
    variables["$Assert"]["shorts"] = []
    variables["$Assert"]["options"] = {}
    variables["$Assert"]["options"]["value"] = lambda bCond=False, sTxt='': variables["$printRed"]["options"]["value"](sTxt) if not bCond else None


    variables["$conn"] = {}
    variables["$conn"]["shorts"] = []
    variables["$conn"]["options"] = {}
    variables["$conn"]["options"]["value"] = None

    variables["$db_schema"] = {}
    variables["$db_schema"]["shorts"] = []
    variables["$db_schema"]["options"] = {}
    variables["$db_schema"]["options"]["value"] = ""

    variables["$db_version"] = {}
    variables["$db_version"]["shorts"] = []
    variables["$db_version"]["options"] = {}
    variables["$db_version"]["options"]["value"] = "None: "

    variables["$folder_name_old"] = {}
    variables["$folder_name_old"]["shorts"] = []
    variables["$folder_name_old"]["options"] = {}
    variables["$folder_name_old"]["options"]["value"] = ""

    variables["$folder_name"] = {}
    variables["$folder_name"]["shorts"] = []
    variables["$folder_name"]["options"] = {}
    variables["$folder_name"]["options"]["value"] = ""

    variables["$folder_exists_old"] = {}
    variables["$folder_exists_old"]["shorts"] = []
    variables["$folder_exists_old"]["options"] = {}
    variables["$folder_exists_old"]["options"]["value"] = False

    variables["$folder_exists"] = {}
    variables["$folder_exists"]["shorts"] = []
    variables["$folder_exists"]["options"] = {}
    variables["$folder_exists"]["options"]["value"] = False

    variables["$parse_value_type"] = {}
    variables["$parse_value_type"]["shorts"] = []
    variables["$parse_value_type"]["options"] = {}
    variables["$parse_value_type"]["options"]["value"] = "auto"

    variables["$sleep"] = {}
    variables["$sleep"]["shorts"] = []
    variables["$sleep"]["options"] = {}
    variables["$sleep"]["options"]["value"] = 1

    variables["$all"] = {}
    variables["$all"]["shorts"] = ["$a","$al"]
    variables["$all"]["data"] = {}
    variables["$all"]["data"]["value"] = 0
    variables["$all"]["data"]["print"] = {}
    variables["$all"]["data"]["print data"] = {}
    variables["$all"]["data"]["print data all"] = {}
    variables["$all"]["data"]["print data easy"] = {}
    #variables["$all"]["print data"]["print data easy"]["what"] = []
    variables["$all"]["data"]["data"] = {}
    variables["$all"]["data"]["data select"] = {}
    variables["$all"]["data"]["data select easy"] = {}
    variables["$all"]["data"]["data fill"] = {}
    variables["$all"]["data"]["data fill easy"] = {}
    variables["$all"]["data"]["data profile"] = {}
    variables["$all"]["data"]["data profile easy"] = {}

    variables["$all"]["print history"] = {}
    variables["$all"]["print history"]["value"] = 0
    variables["$all"]["print history"]["print history"] = {}
    variables["$columns_all"] = {}
    variables["$columns_all"]["shorts"] = ["$columns_a","$ca"]
    variables["$columns_all"]["data"] = {}
    variables["$columns_all"]["data"]["value"] = []
    variables["$columns_all"]["data"]["print"] = {}
    variables["$columns_all"]["data"]["print data"] = {}
    variables["$columns_all"]["data"]["print data easy"] = {}
    variables["$columns_all"]["data"]["data"] = {}
    variables["$columns_all"]["data"]["data select"] = {}
    variables["$columns_all"]["data"]["data select easy"] = {}
    variables["$columns_all"]["data"]["data fill"] = {}
    variables["$columns_all"]["data"]["data fill easy"] = {}
    variables["$columns_all"]["data"]["graph boxplot"] = {}
    variables["$columns_all"]["data"]["graph barchart"] = {}
    variables["$columns_all"]["data"]["graph linechart"] = {}

    variables["$red"] = {}
    variables["$red"]["shorts"] = ["$r"]
    variables["$red"]["user"] = {}
    variables["$red"]["user"]["value"] = 1
    variables["$green"] = {}
    variables["$green"]["shorts"] = ["$g"]
    variables["$green"]["user"] = {}
    variables["$green"]["user"]["value"] = 2
    variables["$invGreen"] = {}
    variables["$invGreen"]["shorts"] = ["$invgreen","$invg","$ig"]
    variables["$invGreen"]["user"] = {}
    variables["$invGreen"]["user"]["value"] = 20255
    variables["$invRed"] = {}
    variables["$invRed"]["shorts"] = ["$invred","$invr","$ir"]
    variables["$invRed"]["user"] = {}
    variables["$invRed"]["user"]["value"] = 10255
    variables["$list"] = {}
    variables["$list"]["shorts"] = ["$l"]
    variables["$list"]["user"] = {}
    #a = "a"
    variables["$list"]["user"]["value"] = "[1,2,a]"

    variables["$date"] = {}
    variables["$date"]["shorts"] = ["$d"]
    variables["$date"]["user"] = {}
    variables["$date"]["user"]["value"] = "%Y-%m-%d"
    variables["$time"] = {}
    variables["$time"]["shorts"] = ["$t"]
    variables["$time"]["user"] = {}
    variables["$time"]["user"]["value"] = "%H:%M:%S"
    variables["$mstime"] = {}
    variables["$mstime"]["shorts"] = ["$t"]
    variables["$mstime"]["user"] = {}
    variables["$mstime"]["user"]["value"] = "%H:%M:%S.%f0"
    #variables["$time"]["user"]["value"] = "%H:%M:%S.%f0"
    #variables["$time"]["user"]["value"] = "%H:%M:%S.%f"
    variables["$datetime"] = {}
    variables["$datetime"]["shorts"] = ["$dt"]
    variables["$datetime"]["user"] = {}
    variables["$datetime"]["user"]["value"] = "%Y-%m-%d %H:%M:%S"

    variables["$decimal_separator"] = {}
    variables["$decimal_separator"]["shorts"] = ["$ds"]
    variables["$decimal_separator"]["user"] = {}
    variables["$decimal_separator"]["user"]["value"] = "."
    variables["$thousands_separator"] = {}
    variables["$thousands_separator"]["shorts"] = ["$ts"]
    variables["$thousands_separator"]["user"] = {}
    variables["$thousands_separator"]["user"]["value"] = ","

    variables["$none"] = {}
    variables["$none"]["shorts"] = ["$n", "$no"]
    variables["$none"]["user"] = {}
    variables["$none"]["user"]["value"] = None

    variables["$now"] = {}
    variables["$now"]["shorts"] = ["$now"]
    variables["$now"]["user"] = {}
    variables["$now"]["user"]["value"] = lambda x: datetime.datetime.now()

    print(variables["$now"]["user"]["value"].__class__)
    print(variables["$now"]["user"]["value"](None))

    '''
    import datetime
    datetime.datetime.strptime('24052010', "%d%m%Y").date()
    '''


    #variables["$a"] = 0

    command_options = {}

    command_options["#"] = {}
    command_options["#"]["name"] = ["title", "note", "title_color", "note_color"]
    command_options["#"]["required"] = [False, False, False, False]
    command_options["#"]["type"] = ["str", "str", "int", "int"]
    command_options["#"]["default"] = [None, None, None, None]
    command_options["#"]["help1"] = "Help for command '#'"
    command_options["#"]["help2"] = ["Bla1","Bla2","Bla3","Bla4"]
    command_options["#"]["alternative"] = ["#"]
    command_options["#"]["altoption"] = [["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["quit"] = {}
    command_options["quit"]["name"] = []
    command_options["quit"]["required"] = []
    command_options["quit"]["type"] = []
    command_options["quit"]["default"] = []
    command_options["quit"]["help1"] = "Help for command 'folder'"
    command_options["quit"]["help2"] = []
    command_options["quit"]["alternative"] = ["q"]
    command_options["quit"]["altoption"] = []

    command_options["folder"] = {}
    command_options["folder"]["name"] = ["foldername"]
    command_options["folder"]["required"] = [True]
    command_options["folder"]["type"] = ["str"]
    command_options["folder"]["default"] = [None]
    command_options["folder"]["help1"] = "Help for command 'folder'"
    command_options["folder"]["help2"] = ["Blabla1"]
    command_options["folder"]["alternative"] = ["folder", "f"]
    command_options["folder"]["altoption"] = [["fn","f"]]


    command_options["set variable easy"] = {}
    command_options["set variable easy"]["name"] = ["names"]
    command_options["set variable easy"]["required"] = [True]
    command_options["set variable easy"]["type"] = ["dictlist"]
    command_options["set variable easy"]["default"] = [None]
    command_options["set variable easy"]["help1"] = "Help for command 'set'"
    command_options["set variable easy"]["help2"] = ["Bla1"]
    command_options["set variable easy"]["alternative"] = ["set variable", "sv"]
    command_options["set variable easy"]["altoption"] = [["n"]]


    command_options["set variable"] = {}
    command_options["set variable"]["name"] = ["what", "names"]
    command_options["set variable"]["required"] = [True, True]
    command_options["set variable"]["type"] = [["variable", "v"], "dictlist"]
    command_options["set variable"]["default"] = [None, None]
    command_options["set variable"]["help1"] = "Help for command 'set'"
    command_options["set variable"]["help2"] = ["Bla1", "Bla2"]
    command_options["set variable"]["alternative"] = ["set", "s"]
    command_options["set variable"]["altoption"] = [["w"], ["n"]]

    command_options["connect sqlite3"] = {}
    command_options["connect sqlite3"]["name"] = ["what", "filename", "parse_formats"]
    command_options["connect sqlite3"]["required"] = [True, False, False]
    command_options["connect sqlite3"]["type"] = [["sqlite3", "sqlite", "sql3", "sql", "s"], "str", "bool"]
    command_options["connect sqlite3"]["default"] = [None, ":memory:", True]
    command_options["connect sqlite3"]["help1"] = "Help for command 'connect'"
    command_options["connect sqlite3"]["help2"] = ["Blabla1","Blabla2","Blabla3"]
    command_options["connect sqlite3"]["alternative"] = ["connect", "c"]
    command_options["connect sqlite3"]["altoption"] = [["w"], ["fn","f"], ["pf","p"]]

    command_options["connect sqlite3 easy"] = {}
    command_options["connect sqlite3 easy"]["name"] = ["filename", "parse_formats"]
    command_options["connect sqlite3 easy"]["required"] = [False, False]
    command_options["connect sqlite3 easy"]["type"] = ["str", "bool"]
    command_options["connect sqlite3 easy"]["default"] = [":memory:", True]
    command_options["connect sqlite3 easy"]["help1"] = "Help for command 'connect'"
    command_options["connect sqlite3 easy"]["help2"] = ["Blabla1","Blabla2"]
    command_options["connect sqlite3 easy"]["alternative"] = ["connect sqlite3", "connect sqlite", "connect sql3", "connect sql", "connect s", "c sqlite3", "c sqlite", "c sql3", "c sql", "c s",  "csqlite3", "csqlite", "csql3", "csql", "cs"]
    command_options["connect sqlite3 easy"]["altoption"] = [["fn","f"], ["pf","p"]]

    command_options["connect mysql"] = {}
    command_options["connect mysql"]["name"] = ["database", "user", "password", "host", "port"]
    command_options["connect mysql"]["required"] = [False, False, False, False, False]
    command_options["connect mysql"]["type"] = ["str", "str", "str", "str", "int"]
    command_options["connect mysql"]["default"] = ["", "root", "admin", "localhost", 3306]
    command_options["connect mysql"]["help1"] = "Help for command 'folder'"
    command_options["connect mysql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
    command_options["connect mysql"]["alternative"] = ["c mysql", "c my", "cmysql", "cmy"]
    command_options["connect mysql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

    command_options["connect postgre"] = {}
    command_options["connect postgre"]["name"] = ["database", "user", "password", "host", "port"]
    command_options["connect postgre"]["required"] = [False, False, False, False, False]
    command_options["connect postgre"]["type"] = ["str", "str", "str", "str", "int"]
    command_options["connect postgre"]["default"] = ["", "postgres", "postgres1", "localhost", 5432]
    command_options["connect postgre"]["help1"] = "Help for command 'folder'"
    command_options["connect postgre"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5"]
    command_options["connect postgre"]["alternative"] = ["c postgre", "c pg", "c p", "cpostgre", "cpg", "cp"]
    command_options["connect postgre"]["altoption"] = [["d"],["u"],["p"],["h"],["po"]]

    command_options["connect mssql"] = {}
    command_options["connect mssql"]["name"] = ["database", "user", "password", "host", "port", "driver", "option"]
    command_options["connect mssql"]["required"] = [False, False, False, False, False, False, False]
    command_options["connect mssql"]["type"] = ["str", "str", "str", "str", "int", "str", "str"]
    command_options["connect mssql"]["default"] = ["", None, None, f'''{variables["$mssql_host"]["options"]["value"]}\SQLEXPRESS''', None, "SQL Server", "Trusted_Connection=yes"]
    command_options["connect mssql"]["help1"] = "Help for command 'folder'"
    command_options["connect mssql"]["help2"] = ["Bla1", "Bla2", "Bla3", "Bla4", "Bla5", "Bla6", "Bla7"]
    command_options["connect mssql"]["alternative"] = ["c mssql", "c ms", "cmssql", "cms"]
    command_options["connect mssql"]["altoption"] = [["d"],["u"],["p"],["h"],["po"],["dr"],["o", "do"]]

    command_options["read"] = {}
    command_options["read"]["name"] = ["filename", "delimiter", "text_qualifier", "read_columns", "strip_columns", "lines"]
    command_options["read"]["required"] = [True, False, False, False, False, False]
    command_options["read"]["type"] = ["str", "str", "str", "bool", "bool", "int"]
    command_options["read"]["default"] = [None, "	", None, True, True, None]
    command_options["read"]["help1"] = "Help for command 'folder'"
    command_options["read"]["help2"] = ["Blabla1", "Blabla2", "Blabla3", "Blabla4", "Blabla5", "Blabla6"]
    command_options["read"]["alternative"] = ["read", "r"]
    command_options["read"]["altoption"] = [["f"],["d"],["t","tq"], ['r','rc'], ['s','sc'], ["l"]]

    command_options["export"] = {}
    command_options["export"]["name"] = ["filename", "delimiter", "none"]
    command_options["export"]["required"] = [True, False, False]
    command_options["export"]["type"] = ["str", "str", "str"]
    command_options["export"]["default"] = [None, "	", ""]
    command_options["export"]["help1"] = "Help for command 'folder'"
    command_options["export"]["help2"] = ["Blabla1", "Blabla2", "Blabla3"]
    command_options["export"]["alternative"] = ["e"]
    command_options["export"]["altoption"] = [["fn","f"],["d"],["null","n"]]

    command_options["load"] = {}
    command_options["load"]["name"] = ["filename"]
    command_options["load"]["required"] = [True]
    command_options["load"]["type"] = ["str"]
    command_options["load"]["default"] = [None]
    command_options["load"]["help1"] = "Help for command 'folder'"
    command_options["load"]["help2"] = ["Blabla1"]
    command_options["load"]["alternative"] = ["l"]
    command_options["load"]["altoption"] = [["fn","f"]]


    command_options["table"] = {}
    command_options["table"]["name"] = ["tablename", "drop_if_exists", "id"]
    command_options["table"]["required"] = [True, False, False]
    command_options["table"]["type"] = ["str", "bool", "str"]
    command_options["table"]["default"] = [None, False, None]
    command_options["table"]["help1"] = "Help for command 'folder'"
    command_options["table"]["help2"] = ["Blabla1", "Blabla2", "Blabla3"]
    command_options["table"]["alternative"] = ["table", "t"]
    command_options["table"]["altoption"] = [["tn","t"], ["die","de","dt","d"], ["i"]]


    command_options["insert"] = {}
    command_options["insert"]["name"] = ["tablename"]
    command_options["insert"]["required"] = [True]
    command_options["insert"]["type"] = ["str"]
    command_options["insert"]["default"] = [None]
    command_options["insert"]["help1"] = "Help for command 'folder'"
    command_options["insert"]["help2"] = ["Blabla1"]
    command_options["insert"]["alternative"] = ["insert", "i"]
    command_options["insert"]["altoption"] = [["tn","t"]]

    # print data via command print
    command_options["print"] = {}
    command_options["print"]["name"] = ["from", "to", "step", "random", "list", "columns"]
    command_options["print"]["required"] = [False, False, False, False, False, False]
    command_options["print"]["type"] = ["int", "int", "int", "int", "intlist", "strlist"]
    command_options["print"]["default"] = [0, 0, 1, 0, "[]", "[]"]
    command_options["print"]["help1"] = "Help for command 'folder'"
    command_options["print"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
    command_options["print"]["alternative"] = ["print", "p"]
    command_options["print"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"]]

    command_options["print data all"] = {}
    command_options["print data all"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
    command_options["print data all"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
    command_options["print data all"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int"]
    command_options["print data all"]["default"] = [0, "$all", 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
    command_options["print data all"]["help1"] = "Help for command 'folder'"
    command_options["print data all"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12"]
    command_options["print data all"]["alternative"] = ["print data all", "pda"]
    command_options["print data all"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["print data easy"] = {}
    command_options["print data easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
    command_options["print data easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
    command_options["print data easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int"]
    command_options["print data easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
    command_options["print data easy"]["help1"] = "Help for command 'folder'"
    command_options["print data easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12"]
    command_options["print data easy"]["alternative"] = ["print data", "pd"]
    command_options["print data easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["print data"] = {}
    command_options["print data"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
    command_options["print data"]["required"] = [False, False, False, False, False, False, False, False, False, False, False]
    command_options["print data"]["type"] = [["data","d"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
    command_options["print data"]["default"] = ["data", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
    command_options["print data"]["help1"] = "Help for command 'folder'"
    command_options["print data"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
    command_options["print data"]["alternative"] = ["print", "p"]
    command_options["print data"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["print columns"] = {}
    command_options["print columns"]["name"] = ["what"]
    command_options["print columns"]["required"] = [True]
    command_options["print columns"]["type"] = [["columns", "c"]]
    command_options["print columns"]["default"] = [None]
    command_options["print columns"]["help1"] = "Help for command 'folder'"
    command_options["print columns"]["help2"] = ["Bla1"]
    command_options["print columns"]["alternative"] = ["print", "p"]
    command_options["print columns"]["altoption"] = [["w"]]

    command_options["print history"] = {}
    command_options["print history"]["name"] = []
    command_options["print history"]["required"] = []
    command_options["print history"]["type"] = []
    command_options["print history"]["default"] = []
    command_options["print history"]["help1"] = "Help for command 'folder'"
    command_options["print history"]["help2"] = []
    command_options["print history"]["alternative"] = ["print h", "p h", "ph"]
    command_options["print history"]["altoption"] = []


    command_options["print variables"] = {}
    command_options["print variables"]["name"] = ["what"]
    command_options["print variables"]["required"] = [True]
    command_options["print variables"]["type"] = [["variables", "v"]]
    command_options["print variables"]["default"] = [None]
    command_options["print variables"]["help1"] = "Help for command 'folder'"
    command_options["print variables"]["help2"] = ["Bla1"]
    command_options["print variables"]["alternative"] = ["print", "p"]
    command_options["print variables"]["altoption"] = [["w"]]

    '''
    command_options["print"] = {}
    command_options["print"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
    command_options["print"]["required"] = [False, False, False, False, False, False, False, False, False, False, False]
    command_options["print"]["type"] = [["data","columns","history","d","c","h"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
    command_options["print"]["default"] = ["data", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
    command_options["print"]["help1"] = "Help for command 'folder'"
    command_options["print"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
    command_options["print"]["alternative"] = ["p"]
    command_options["print"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]
    '''

    command_options["break"] = {}
    command_options["break"]["name"] = ["what", "from", "to", "step", "list", "columns"]
    command_options["break"]["required"] = [False, False, False, False, False, False]
    command_options["break"]["type"] = [["data","columns"], "int", "int", "int", "intlist", "strlist"]
    command_options["break"]["default"] = ["data", 0, print_max_default, 1, None, None]
    command_options["break"]["help1"] = "Help for command 'folder'"
    command_options["break"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
    command_options["break"]["alternative"] = ["b"]
    command_options["break"]["altoption"] = [["w"],["f"], ["t"], ["s"], ["l"], ["c"]]

    command_options["data fill easy"] = {}
    command_options["data fill easy"]["name"] = ["formats", "nones", "title", "note", "title_color", "note_color"]
    command_options["data fill easy"]["required"] = [False, False, False, False, False, False]
    command_options["data fill easy"]["type"] = ["dictlist", "dictlist", "str", "str", "int", "int"]
    command_options["data fill easy"]["default"] = [None, None, None, None, None, None]
    command_options["data fill easy"]["help1"] = "Help for command 'data fill easy'"
    command_options["data fill easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6"]
    command_options["data fill easy"]["alternative"] = ["data fill", "data f", "d f ", "df"]
    command_options["data fill easy"]["altoption"] = [["fs", "f"], ["nulls", "ns", "n"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["data select easy"] = {}
    command_options["data select easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color"]
    command_options["data select easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False]
    command_options["data select easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"],"str", "str", "int", "int"]
    command_options["data select easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "any", None, None, None, None]
    command_options["data select easy"]["help1"] = "Help for command 'data select easy'"
    command_options["data select easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10", "Bla10", "Bla11"]
    command_options["data select easy"]["alternative"] = ["data select", "data s", "d s", "ds"]
    command_options["data select easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["data select"] = {}
    command_options["data select"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
    command_options["data select"]["required"] = [True, False, False, False, False, False, False, False, False, False, False]
    command_options["data select"]["type"] = [["select","se","s"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
    command_options["data select"]["default"] = ["select", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
    command_options["data select"]["help1"] = "Help for command 'folder'"
    command_options["data select"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
    command_options["data select"]["alternative"] = ["data", "d"]
    command_options["data select"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["data profile easy"] = {}
    command_options["data profile easy"]["name"] = ["from", "to", "step", "random", "list", "columns", "nones", "nones_option", "title", "note", "title_color", "note_color", "print_all", "purge"]
    command_options["data profile easy"]["required"] = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    command_options["data profile easy"]["type"] = ["int", "int", "int", "int", "intlist", "strlist", "strlist", ["any","all","none"], "str", "str", "int", "int", "bool", "bool"]
    command_options["data profile easy"]["default"] = [0, 0, 1, 0, "[]", "[]", "[]", "all", None, None, None, None, False, False]
    command_options["data profile easy"]["help1"] = "Help for command 'folder'"
    command_options["data profile easy"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11","Bla12","Bla13","Bla14"]
    command_options["data profile easy"]["alternative"] = ["data profile", "d profile", "d pr", "d p", "dpr", "dp"]
    command_options["data profile easy"]["altoption"] = [["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["nulls", "ns", "n"], ["no"], ["tt"], ["nt"], ["tc"], ["nc"], ["pa"], ["pu"]]

    command_options["data profile"] = {}
    command_options["data profile"]["name"] = ["what", "from", "to", "step", "random", "list", "columns", "title", "note", "title_color", "note_color"]
    command_options["data profile"]["required"] = [False, False, False, False, False, False, False, False, False, False, False]
    command_options["data profile"]["type"] = [["profile","pr","p"], "int", "int", "int", "int", "intlist", "strlist", "str", "str", "int", "int"]
    command_options["data profile"]["default"] = ["profile", 0, 0, 1, 0, "[]", "[]", None, None, None, None]
    command_options["data profile"]["help1"] = "Help for command 'folder'"
    command_options["data profile"]["help2"] = ["Bla1","Bla2","Bla3","Bla4","Bla5","Bla6","Bla7","Bla8","Bla9","Bla10","Bla11"]
    command_options["data profile"]["alternative"] = ["data", "d"]
    command_options["data profile"]["altoption"] = [["w"], ["f"], ["t"], ["s"], ["r"], ["l"], ["c"], ["tt"], ["nt"], ["tc"], ["nc"]]

    command_options["data reset"] = {}
    command_options["data reset"]["name"] = ["what"]
    command_options["data reset"]["required"] = [True]
    command_options["data reset"]["type"] = [["reset","rs","r"]]
    command_options["data reset"]["default"] = ["reset"]
    command_options["data reset"]["help1"] = "Help for command 'folder'"
    command_options["data reset"]["help2"] = ["Bla1"]
    command_options["data reset"]["alternative"] = ["data", "d"]
    command_options["data reset"]["altoption"] = [["w"]]

    command_options["graph boxplot"] = {}
    command_options["graph boxplot"]["name"] = ["what", "columns", "title", "show_fliers"]
    command_options["graph boxplot"]["required"] = [True, False, False, False]
    command_options["graph boxplot"]["type"] = [["boxplot","bo"], "strlist", "str", "bool"]
    command_options["graph boxplot"]["default"] = ["boxplot", None, None, True]
    command_options["graph boxplot"]["help1"] = "Help for command 'folder'"
    command_options["graph boxplot"]["help2"] = ["Bla1","Bla2","Bla3","Bla4"]
    command_options["graph boxplot"]["alternative"] = ["graph", "g"]
    command_options["graph boxplot"]["altoption"] = [["w"],["c"],["tt"],["sf"]]

    command_options["graph barchart"] = {}
    command_options["graph barchart"]["name"] = ["what", "columns", "title"]
    command_options["graph barchart"]["required"] = [True, False, False]
    command_options["graph barchart"]["type"] = [["barchart","ba"], "strlist", "str"]
    command_options["graph barchart"]["default"] = ["barchart", None, None]
    command_options["graph barchart"]["help1"] = "Help for command 'folder'"
    command_options["graph barchart"]["help2"] = ["Bla1","Bla2","Bla3"]
    command_options["graph barchart"]["alternative"] = ["graph", "g"]
    command_options["graph barchart"]["altoption"] = [["w"],["c"],["tt"]]

    command_options["graph linechart"] = {}
    command_options["graph linechart"]["name"] = ["what", "columns", "title"]
    command_options["graph linechart"]["required"] = [True, False, False]
    command_options["graph linechart"]["type"] = [["linechart","li"], "strlist", "str"]
    command_options["graph linechart"]["default"] = ["linechart", None, None]
    command_options["graph linechart"]["help1"] = "Help for command 'folder'"
    command_options["graph linechart"]["help2"] = ["Bla1","Bla2","Bla3"]
    command_options["graph linechart"]["alternative"] = ["graph", "g"]
    command_options["graph linechart"]["altoption"] = [["w"],["c"],["tt"]]

    command_options["graph histogram"] = {}
    command_options["graph histogram"]["name"] = ["what", "columns", "split", "title"]
    command_options["graph histogram"]["required"] = [True, False, False, False]
    command_options["graph histogram"]["type"] = [["histogram","hi"], "strlist", "strlist", "str"]
    command_options["graph histogram"]["default"] = ["histogram", None, None, None]
    command_options["graph histogram"]["help1"] = "Help for command 'folder'"
    command_options["graph histogram"]["help2"] = ["Bla1","Bla2","Bla3","Bla4"]
    command_options["graph histogram"]["alternative"] = ["graph", "g"]
    command_options["graph histogram"]["altoption"] = [["w"],["c"],["s"],["tt"]]

    command_options["data memory easy"] = {}
    command_options["data memory easy"]["name"] = ["name"]
    command_options["data memory easy"]["required"] = [False]
    command_options["data memory easy"]["type"] = ["str"]
    command_options["data memory easy"]["default"] = ["1"]
    command_options["data memory easy"]["help1"] = "Help for command 'folder'"
    command_options["data memory easy"]["help2"] = ["Bla1"]
    command_options["data memory easy"]["alternative"] = ["data memory", "data mem", "dm"]
    command_options["data memory easy"]["altoption"] = [["n"]]

    command_options["data memory"] = {}
    command_options["data memory"]["name"] = ["what", "name"]
    command_options["data memory"]["required"] = [True, False]
    command_options["data memory"]["type"] = [["memory","mem","m"],"str"]
    command_options["data memory"]["default"] = ["memory", "1"]
    command_options["data memory"]["help1"] = "Help for command 'folder'"
    command_options["data memory"]["help2"] = ["Bla1","Bla2"]
    command_options["data memory"]["alternative"] = ["data", "d"]
    command_options["data memory"]["altoption"] = [["w"],["n"]]

    command_options["data activate easy"] = {}
    command_options["data activate easy"]["name"] = ["name"]
    command_options["data activate easy"]["required"] = [False]
    command_options["data activate easy"]["type"] = ["str"]
    command_options["data activate easy"]["default"] = ["1"]
    command_options["data activate easy"]["help1"] = "Help for command 'folder'"
    command_options["data activate easy"]["help2"] = ["Bla1"]
    command_options["data activate easy"]["alternative"] = ["data activate", "data act", "da"]
    command_options["data activate easy"]["altoption"] = [["n"]]

    command_options["data activate"] = {}
    command_options["data activate"]["name"] = ["what", "name"]
    command_options["data activate"]["required"] = [True, False]
    command_options["data activate"]["type"] = [["activate","act","a"],"str"]
    command_options["data activate"]["default"] = ["memory", "1"]
    command_options["data activate"]["help1"] = "Help for command 'folder'"
    command_options["data activate"]["help2"] = ["Bla1","Bla2"]
    command_options["data activate"]["alternative"] = ["data", "d"]
    command_options["data activate"]["altoption"] = [["w"],["n"]]

    command_options["split"] = {}
    command_options["split"]["name"] = ["columns", "split"]
    command_options["split"]["required"] = [True, True]
    command_options["split"]["type"] = ["strlist", "strlist"]
    command_options["split"]["default"] = [None, None]
    command_options["split"]["help1"] = "Help for command 'folder'"
    command_options["split"]["help2"] = ["Bla1","Bla2"]
    command_options["split"]["alternative"] = ["split", "s"]
    command_options["split"]["altoption"] = [["c"],["s"]]

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

    variables["$do_mp"]["options"]["value"] = False
    if isinstance(vars(namespace)["do_mp"], bool):
        variables["$do_mp"]["options"]["value"] = vars(namespace)["do_mp"]

    if variables["$do_mp"]["options"]["value"]:
        print("Multiprocessing:", variables["$do_mp"]["options"]["value"], f"(using {mp.cpu_count()} processes)")
    else:
        print("Multiprocessing:", variables["$do_mp"]["options"]["value"])

    if len(vars(namespace)["sql_files"]) > 0:
        sqls = get_sql_queries_dict(vars(namespace)["sql_files"], variables["$folder_exists"]["options"]["value"], variables["$folder_name"]["options"]["value"])
        #print(sqls)
        for full_filename in sqls.keys():
            #OK_returned = 1
            for i, sql in enumerate(sqls[full_filename]):
                variables["$printCom"]["options"]["value"](f"\n\\\\ SQL file '{full_filename}' command no {str(i+1)} \\\\")
                #print(sql)
                #print()
                start = time.perf_counter()
                variables, data, columns = do_sql(sql, variables, command_options, data, columns)
                OK_returned = variables["$command_results"]["options"]["value"][-1]
                end = time.perf_counter()
                print()
                if OK_returned == 1:
                    print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                elif OK_returned > 1:
                    variables["$printRed"]["options"]["value"]("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                    time.sleep(2)
                else: break


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

        if variables["$folder_exists"]["options"]["value"]:
            print(f'''Using folder '{variables["$folder_name"]["options"]["value"]}'.''')
        else:
            variables["$folder_name"]["options"]["value"] = os.getcwd()
            print(f'''Folder is not specified. Using working directory '{variables["$folder_name"]["options"]["value"]}'.''')
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
                variables, data, columns = do_sql(sql, variables, command_options, data, columns)
                OK_returned = variables["$command_results"]["options"]["value"][-1]
                end = time.perf_counter()
                print()
                if OK_returned == 1:
                    print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
                elif OK_returned > 1:
                    variables["$printRed"]["options"]["value"]("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))
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
