from flask import Flask, jsonify, render_template, request
import time
import math
import re
import nltk
import pandas as pd
import numpy as np
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()    
from timeit import default_timer as timer
import tkinter as tk
from tkinter import filedialog
app = Flask(__name__)
@app.route("/")
def main():
    # Carga template main.html
    return render_template('index.html')

@app.route("/", methods=["POST","GET"])
def proce():
    start = timer()
    nltk.download('stopwords')
    porter = PorterStemmer()
    start = timer()
    url = "https://github.com/JBorja96/Diccionario-Kichwa/raw/main/dataset.csv"

    df = pd.read_csv(url, encoding="utf8")
    kichwa = pd.unique(df['Kichwa'])
    sp = pd.unique(df['Spanish'])
    ki = np.array(df['Kichwa'])
    et = np.array(df['Etiqueta'])
    ki2 = ki.tolist()
    et2 = et.tolist()
    e = request.form['todo']
    d = []
    d.append(e)
    #d=['HATUN MAMITA PACHA RIKURICHIKWAN RIMAY Shuk karu ayllu llaktapimi hatun mamita kawsashka payka tukuy punllakunami ukka hatarishpa wiwikata michinaman kawsakkashka nin Skuk punllami paypak uchilla churika shuk sumak pacharikurita kunpitashka paypak watakuna paktakpi chay hatun mamitaka ashkata kushikushpami hapishka payka pirka patapimi warkuska puñuna kawitu manyapi chay pacharichika sumaktami sapan tutamantakunatami tic tac nishpa rikchachikkashka nin Tayka semana washaka shuk tutamantaka chay pacharikurika mana uyarishkachu hatun mamitaka mana ukka hatarishkachu paypak tutamanta mikunata ruranaman wiwikatapash mana michinaman rishkachu kawitupi puñukushkallami chaymantami chay hatun mamitaka yuyarishka kayaka pitak rikchachinka pacharikuripak mana ushanchu nishpaka puñurishkallami tukuy pachakunata ninkunami']

    d1 = ['HATUN MAMITA PACHA RIKURICHIKWAN RIMAY']
    fin = []
    def NLP(Lista):
        i = 0
        total2 = []
        total = []
        e = 0
        s = 0
        r = []
        for frase in Lista:
            i = 0
            D2 = frase.lower()
            D3 = re.sub('[()""!@#$%^&*¿?«{},0123456789./:;’^]', ' ', D2)
            D4 = D3.split()
            while (i < len(D4)):
                r.append(D4[i])
                i = i+1
                if(i < len(D4)):
                    r.append(D4[i])
                    h = " ".join(r)
                    i = i+1
                    if(h in kichwa):
                        if(i <= len(D4)):
                            r.append(D4[i])
                            i = i+1
                            h2 = " ".join(r)
                            if(h2 in kichwa):
                                fin.append(h2)
                                h2 = ""
                                h = ""
                                r = []
                            else:
                                fin.append(h)
                                h = ""
                                r = []
                                i = i-1
                        else:
                            fin.append(h)
                            h = ""
                            r = []
                            i = i-1
                    else:
                        fin.append(D4[i-2])
                        h = ""
                        r = []
                        i = i-1
                else:
                    fin.append(D4[i-1])
                    h = ""
                    r = []
        return fin

    def transformacion(k2):
        y = 0
        y2 = []
        while (y < len(ki2)):
            if(et2[y] == k2):
                y2.append(ki2[y])
                y = y+1
            else:
                y = y+1
        return y2

    cuento = NLP(d)

    positivo = transformacion('positivo')

    negativo = transformacion('negativo')

    neutro = transformacion('neutro')

    f2 = []

    f2.append(cuento)
    f2.append(positivo)
    f2.append(negativo)
    f2.append(neutro)

    def jaccard(Lista):
        mat_jaccard = []
        for i in Lista:
            temp = []
            for j in Lista:
                a = set(i)
                b = set(j)
                res = len(a & b)
                num_elemnt = len(a)+len(b)
                temp.append(res/(num_elemnt-res))
            mat_jaccard.append(temp)
        return np.array(mat_jaccard)

    jac = jaccard(f2)

    def diccionario(Lista):
        dic = []
        for frase in Lista:
            for palabra in frase:
                if palabra in dic:
                    False
                else:
                    dic.append(palabra)
        return dic

    diccionario_abstract = diccionario(f2)

    def TF_DF_IDF(diccionario):
        tf = []
        df = []
        idf = []
        for i in diccionario:
            fd = 0
            frec = 0
            temp = []
            for j in f2:
                frec = j.count(i)
                if frec > 0:
                    frec = 1+(math.log10(frec))
                    fd = fd+1
                temp.append(frec)
            idf.append(math.log10(len(f2)/fd))
            df.append(fd)
            tf.append(temp)
        return tf, df, idf

    def TFxIDF(diccionario_abstract):
        TF, DF, IDF = TF_DF_IDF(diccionario_abstract)
        tfxidf = []
        for i in range(len(IDF)):
            temp = []
            for j in range(len(TF[0])):
                temp.append(IDF[i]*TF[i][j])
            tfxidf.append((temp))
        tfxidf = [list(f) for f in (zip(*tfxidf))]
        return tfxidf

    tf_idf = TFxIDF(diccionario_abstract)

    def Long_normalizacion(tf_idf):
        long_norm = []
        for j in tf_idf:
            acum = 0
            for i in j:
                acum = acum+pow(i, 2)
            modulo = math.sqrt(acum)
            temp1 = []
            for i in j:
                temp1.append(i/modulo)
            long_norm.append(temp1)
        return long_norm

    long_norm = Long_normalizacion(tf_idf)

    def Coseno(long_norm):
        punt_cos = []
        for i in long_norm:
            lista = []
            for j in long_norm:
                lista.append(round(np.dot(j, i), 3))
            punt_cos.append(lista)
        return np.array(punt_cos)

    Puntuacioncoseno = Coseno(long_norm)
    print("************SEGUN JACARD**************")
    print(jac)
    print("su porcentaje de positividad es ", jac[0][1]*100)
    print("su porcentaje de negatividad es ", jac[0][2]*100)
    print("su porcentaje de neutralidad es ", jac[0][3]*100)

    rja = []
    rja.append(jac[0][1])
    rja.append(jac[0][2])
    rja.append(jac[0][3])
    rj1 = max(rja)
    rj2 = rja.index(rj1)

    if(rj2 == 0):
        c = 'positivo'
    elif(rj2 == 1):
        c = 'negativo'
    else:
        c = 'neutro'

    print("El texto es calificado como ", c)
    print("************SEGUN COSENO VECTORIAL**************")
    print(Puntuacioncoseno)
    print("su porcentaje de positividad es ", Puntuacioncoseno[0][1]*100)
    print("su porcentaje de negatividad es ", Puntuacioncoseno[0][2]*100)
    print("su porcentaje de neutralidad es ", Puntuacioncoseno[0][3]*100)

    rca=[]
    rca.append(Puntuacioncoseno[0][1])
    rca.append(Puntuacioncoseno[0][2])
    rca.append(Puntuacioncoseno[0][3])
    rc1=max(rca)
    rc2=rca.index(rc1)

    if(rc2 == 0):
        c1 = 'positivo'
    elif(rc2 == 1):
        c1 = 'negativo'
    else:
        c1 = 'neutro'

    print("El texto es calificado como ", c1)
    rjaf=[jac[0][1]*100,jac[0][2]*100,jac[0][3]*100]
    rcaf=[Puntuacioncoseno[0][1]*100,Puntuacioncoseno[0][2]*100,Puntuacioncoseno[0][3]*100]

    etiqu=['positivo','negativo','neutro']
    sp2=np.array(df['Spanish'])
    sp22=sp2.tolist()
    r2=len(cuento)
    print("palabra","\t","traduccion")
    po=0
    asd=[]
    asd1=[]
    tee=""
    while po<r2:
        if(cuento[po]in kichwa):
            mn=ki2.index(cuento[po])
            print(cuento[po],"\t",sp22[mn])
            asd.append(cuento[po])
            asd1.append(sp22[mn])
        po=po+1
    return render_template("index.html",jac=jac,
        a=jac[0][1]*100,
        b=jac[0][2]*100,
        c=jac[0][3]*100,
        d=c,
        Puntuacioncoseno=Puntuacioncoseno,
        e=Puntuacioncoseno[0][1]*100,
        f=Puntuacioncoseno[0][2]*100,
        g=Puntuacioncoseno[0][3]*100,
        h=c1,
        asd=asd,
        asd1=asd1,
        tee=tee)

# @app.route("/pro")
# def mainn():
#     # Carga template main.html
#     return render_template('pro.html')




if __name__ == '__main__':
    app.run(debug=True)
