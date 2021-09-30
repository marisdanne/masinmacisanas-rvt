import pandas as pd # datu apstrāde
import numpy as np  # darbs ar masīviem
from termcolor import colored as cl # teksta izvade
import matplotlib.pyplot as plt # vizualizācija
import seaborn as sb # vizualizācija
import pickle

from sklearn.model_selection import train_test_split # data split

from sklearn.linear_model import LinearRegression # OLS algorithm
from sklearn.linear_model import Ridge # Ridge algorithm
from sklearn.linear_model import Lasso # Lasso algorithm
from sklearn.linear_model import BayesianRidge # Bayesian algorithm
from sklearn.linear_model import ElasticNet # ElasticNet algorithm
from sklearn import ensemble # Labāki algoritmi
from sklearn.metrics import explained_variance_score as evs # evaluation metric
from sklearn.metrics import r2_score as r2 # evaluation metric


def sagatavot_datus(datne, kolonnas_x, kolonnas_y):

    df = pd.read_csv(datne)
    # df = df.loc[df['modelis'] == 'XC 90']
    print(df.describe())
    # reizēm nepieciešams izmest datus, kur ir tukšas vērtības
    # df.dropna(inplace = True)
    # vai arī aizpildīt tukšos datus ar 0
    # df = df.fillna(0)

    # # reizem nepieciešams pārvērst datu tipus
    # df = parverst_kolonnu(df, kolonna)

    # neatkarīgās (ieejas/avota) vērtības, sauc par X_var
    X_var = df[kolonnas_x].values 
    # atkarīgās (izejas) vērtības, sauc par y_var
    y_var = df[kolonnas_y].values

    # sadalām datus trenēšanā izmantojamos un pārbaudei atstātos
    X_train, X_test, y_train, y_test = train_test_split(X_var, y_var, test_size = 0.2, random_state = 0)

    return(X_train, X_test, y_train, y_test)


def parverst_kolonnu(df, kolonna):
    # pārvēršam visu par Integer, jo tā vajag LinearRegression
    df[kolonna] = pd.to_numeric(df[kolonna], errors = 'coerce')
    df[kolonna] = df[kolonna].astype('int64')
    return df


def modela_kvalitate(y_test, resultats):
    # Kvalitate virs 0.6 ir OK
    print(cl('Explained Variance Score (dispersija): {}'.format(evs(y_test, resultats)), attrs = ['bold']))
    print(cl('R-Squared (kvadratiska novirze): {}'.format(r2(y_test, resultats)), attrs = ['bold']))


def saglabat_modeli(datne, modelis):
    with open(datne, 'wb') as f:
        s = pickle.dumps(modelis)
        f.write(s)


def ieladet_modeli(datne):
    with open(datne, 'rb') as f:
        s = f.read()
        modelis = pickle.loads(s)
    return modelis


def trenet_modeli(modelis, X_train, y_train, X_test, saglabat=None):
    modelis.fit(X_train, y_train)
    if saglabat:
        saglabat_modeli(saglabat, modelis)
    resultats = modelis.predict(X_test)
    return modelis, resultats


def prognozejam_rezultatu(modelis, dati):
    rezultats = modelis.predict(dati)
    return rezultats


def main():
    datne1 = 'dati/ss_lv_auto.csv'
    kol_x1 = ['gads','nobraukums']
    kol_y1 = 'cena'

    datne2 = 'dati/ss_auto_old.csv'
    # kol_x2 = ['wheel-base','length','engine-size','city-mpg']
    kol_x2 = ['gads','nobraukums']
    kol_y2 = 'cena'

    datne3 = 'dati/ss_auto.csv'
    kol_x3 = ['gads','tilpums','nobraukums']
    kol_y3 = 'cena'    

    # Sagatavojam datus no datnes1
    X_train, X_test, y_train, y_test = sagatavot_datus(datne1, kol_x1, kol_y1)

    # # Sagatavojam datus no datnes2
    # X_train, X_test, y_train, y_test = sagatavot_datus(datne2, kol_x2, kol_y2)


    # vienkārša lineārā regresija
    # modelis = LinearRegression()
    # Citi algoritmi ko var lietot:
    # # 2. Ridge
    # modelis = Ridge(alpha = 0.5)
    # # 3. Lasso
    # modelis = Lasso(alpha = 0.01)
    # # 4. Bayesian
    # modelis = BayesianRidge()
    # # 5. ElasticNet
    # modelis = ElasticNet(alpha = 0.01)
    # Labāks algoritms
    modelis = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2, learning_rate = 0.1, loss = 'ls')

    #modelis, rezultats = trenet_modeli(modelis, X_train, y_train, X_test)
    # # Ja gribam saglabāt modeli datnē
    modelis, rezultats = trenet_modeli(modelis, X_train, y_train, X_test, "ss-modelis.pickle")
    modela_kvalitate(y_test, rezultats)

    # Lietojam modeli, lai prognozetu rezultātu
    # dati1 = [[2021,50]]
    # dati1_rez = 1

    # Prognozejot varam dot 2dimensiju masivu
    # dati2 = [[2337,102,109,30]]
    # dati2_rez = 13950
    # Volkswagen,T-Roc,Volkswagen T-Roc,2019,Dīzelis,2.0,30,24900,Pārdodu VW T-Roc 2.0Tdi Dsg 150zs.   Rūpnīcas garantija līdz 2024. gada ,https://i.ss.lv/gallery/4/777/194031/38806185.th2.jpg,/msg/lv/transport/cars/volkswagen/t-roc/bpembf.html
    # Volkswagen,Passat (B8),Volkswagen Passat (B8),2015,Dīzelis,2.0,176,12200
    # dati3 = [[2015, 2.0, 176]]
    # dati3_rez = 12200

    # prognoze = prognozejam_rezultatu(modelis, dati1)
    # print(prognoze, dati1_rez)

    # print("Ielādējam modeli no datnes")
    # modelis2 = ieladet_modeli("modelis.pickle")
    # rezultats2 = modelis2.predict(X_test)
    # modela_kvalitate(y_test, rezultats2)
    # prognoze = prognozejam_rezultatu(modelis2, [dati1])
    # print(prognoze, dati1_rez)


if __name__ == "__main__":
    main()