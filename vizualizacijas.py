import pandas as pd # datu apstrāde
from termcolor import colored as cl # teksta izvade
import matplotlib.pyplot as plt # vizualizācija
import seaborn as sb # vizualizācija

# vizualizaciju pamata konfigurācija
sb.set_style('whitegrid') # plot style
plt.rcParams['figure.figsize'] = (15, 10) # plot size


# Karstuma karte (korelācija)
def karstuma_karte(datne, saglabat=False):
    df = pd.read_csv(datne)
    sb.heatmap(df.corr(method = 'spearman'), annot = True, cmap = 'coolwarm')
    if saglabat:
        # izveidojam datnes nosaukumu bez mapes un faila tipe
        datnes_vards = datne[datne.find("/"):datne.find(".")]
        plt.savefig('atteli/{}-heatmap.png'.format(datnes_vards))
    plt.show()


# Lieluma sastopamības biežums
def sadalijuma_grafiks(datne, kolonna, saglabat=False):
    df = pd.read_csv(datne)
    sb.distplot(df[kolonna], color = 'r')
    plt.title(kolonna.capitalize() + ' biežums', fontsize = 16)
    plt.xlabel(kolonna.capitalize(), fontsize = 14)
    plt.ylabel('Biežums', fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    if saglabat:
        plt.savefig('atteli/{}.png'.format(kolonna))
    plt.show()


# Izkliedes grafiks (scatter plot)
def izkliedes_grafiks(datne, x, y, saglabat=False):
    df = pd.read_csv(datne)
    i = df.columns
    
    plot1 = sb.scatterplot(x, y, data = df, color = 'orange', edgecolor = 'b', s = 15)
    plt.title('{} / {}'.format(x, y), fontsize = 16)
    plt.xlabel('{}'.format(x), fontsize = 14)
    plt.ylabel('{}'.format(y), fontsize = 14)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    if saglabat:
        plt.savefig('atteli/{}-{}.png'.format(x, y))
    plt.show()


datne1 = 'dati/ss_lv_auto.csv'
datne2 = 'dati/ss_auto_old.csv'

# karstuma_karte(datne1, True)
# sadalijuma_grafiks(datne1, "nobraukums")
# sadalijuma_grafiks(datne1, "cena")
# sadalijuma_grafiks(datne1, "cena")
# izkliedes_grafiks(datne1, 'gads', 'cena')
# izkliedes_grafiks(datne2, 'gads', 'nobraukums')
# izkliedes_grafiks(datne2, 'gads', 'cena')
# izkliedes_grafiks(datne1, 'cena', 'nobraukums')
# izkliedes_grafiks(datne2, 'cena', 'nobraukums')