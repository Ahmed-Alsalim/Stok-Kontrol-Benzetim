"""   Ahmed Tawfiq   """
"""   B181200553     """

import random
from math import inf
from beautifultable import BeautifulTable


######### Kullanılacak veriler #########
TalepMin = 80
TalepMax = 130
BasStok = 224
TedarikSure = [2, 3]
TedarikSureOlasilik = [0.75, 0.25]
SiparisMiktar = [224, 275, 325, 400]
MinStok = [200, 225, 250, 275, 300]
KayipMaliye = 100
StokMaliye = 0.2
SiparisMaliye = 50
DevreSayi = 5
BenzetimTablolarYazdir = True
TxtDosyasindaKaydet = True
########################################


# Kullanılacak listeler tanımlanır
BenZam = list(range(1, DevreSayi + 1))
NihaiMaliyeList = []
StokList = []
TalepList = []
EldeKalan = []
KayipList = []
StokPoz = []
SiparisList = []
TedarikSureList = []
StokMaliyeList = []
KayipMaliyeList = []
SiparisMaliyeList = []
ToplamMaliyeList = []


def main():
    for Q in SiparisMiktar:
        GeciciMaliyeList = []
        for R in MinStok:
            ClearData()
            StokList.append(BasStok)
            StokPoz.append(BasStok)
            SiparisList.append(0)
            for _ in BenZam:
                TalepList.append(TalepUret())
                EldeKalan.append(StokList[-1] - TalepList[-1])

                # Talep, stoktan fazla ise kayıp satış miktarı hesaplanır.
                # değil ise kayıp 0 olarak kaydedilir
                if EldeKalan[-1] < 0:
                    KayipList.append(-EldeKalan[-1])
                    EldeKalan[-1] = 0
                else:
                    KayipList.append(0)

                # Stok pozisyonu bulup, minimum stok seviyesinden az ise yeni sipariş açar
                Pozis = StokPoz[-1] - TalepList[-1] + KayipList[-1] + SiparisList[-1]
                StokPoz.append(Pozis)
                if StokPoz[-1] < R:
                    SiparisList.append(Q)
                    TedarikSure = TedarikSureUret()
                    TedarikSureList.append(TedarikSure)
                else:
                    SiparisList.append(0)
                    TedarikSureList.append(0)

                # Açılan siparişin teslim zamanı geldiğinde stoka ekler
                if len(TedarikSureList) >= 3 and TedarikSureList[-3] == 3:
                    if TedarikSureList[-2] == 2:
                        StokList.append(
                            EldeKalan[-1] + SiparisList[-2] + SiparisList[-3]
                        )
                    else:
                        StokList.append(EldeKalan[-1] + SiparisList[-3])
                elif len(TedarikSureList) >= 2 and TedarikSureList[-2] == 2:
                    StokList.append(EldeKalan[-1] + SiparisList[-2])
                else:
                    StokList.append(EldeKalan[-1])

                # Oluşan maliyetler hesaplar
                StokMaliyeList.append(EldeKalan[-1] * StokMaliye)
                KayipMaliyeList.append(KayipList[-1] * KayipMaliye)
                SiparisMaliyeList.append((SiparisList[-1] / Q) * SiparisMaliye)
                ToplamMaliyeList.append(
                    StokMaliyeList[-1] + KayipMaliyeList[-1] + SiparisMaliyeList[-1]
                )
            StokList.pop()
            StokPoz.pop(0)
            SiparisList.pop(0)

            # Tablonun toplam maliyeti hesaplayıp listeye ekler
            Toplam = round(sum(ToplamMaliyeList), 1)
            GeciciMaliyeList.append(Toplam)
            # Kullanıcı tablo yazdırmayı seçmiş ise yazdırılır
            if BenzetimTablolarYazdir:
                SaveTxt(f"\n\nQ={Q} ve R={R} için, Toplam maliyet: {Toplam}")
                BenzetimTablo()

        NihaiMaliyeList.append(GeciciMaliyeList)


# Benzetim tabloları hesaplamak için önceki verileri temizler
def ClearData():
    StokList.clear()
    TalepList.clear()
    EldeKalan.clear()
    KayipList.clear()
    StokPoz.clear()
    SiparisList.clear()
    TedarikSureList.clear()
    StokMaliyeList.clear()
    KayipMaliyeList.clear()
    SiparisMaliyeList.clear()
    ToplamMaliyeList.clear()


# Talep miktarı, verilen aralıkta rastgele değer döndürür
def TalepUret():
    return int(random.uniform(TalepMin, TalepMax))


# Tedarik süre, verilen kümeden ve dağılıma göre rastgele seçer
def TedarikSureUret():
    return int(random.choices(TedarikSure, weights=TedarikSureOlasilik)[0])


# Benzetim tabloları yazdırır
def BenzetimTablo():
    Table = BeautifulTable(maxwidth=150)
    Table.columns.append(BenZam, "Benzetim\nzamanı")
    Table.columns.append(StokList, "Başlangıç\nstok")
    Table.columns.append(TalepList, "Talep")
    Table.columns.append(EldeKalan, "Elde\nkalan")
    Table.columns.append(KayipList, "Kayıp\nsatış")
    Table.columns.append(StokPoz, "Stok\npozisyon")
    Table.columns.append(SiparisList, "Açılan\nsipariş")
    Table.columns.append(TedarikSureList, "Tedarik\nsüresi")
    Table.columns.append(StokMaliyeList, "Elde\nbulundurma\nmaliyeti")
    Table.columns.append(KayipMaliyeList, "Kayıp\nsatış\nmaliyeti")
    Table.columns.append(SiparisMaliyeList, "Sipariş\nmaliyeti")
    Table.columns.append(ToplamMaliyeList, "Toplam\nmaliye")
    Table.set_style(BeautifulTable.STYLE_SEPARATED)

    SaveTxt(Table)


# En düşük maliyetli seçenek işaretleyerek nihai karar tabloyu yazdırır
def KararTablo():
    minindex = []
    minvalue = inf
    for i in NihaiMaliyeList:
        if min(i) < minvalue:
            minvalue = min(i)
            minindex = [NihaiMaliyeList.index(i), i.index(min(i))]
    NihaiMaliyeList[minindex[0]][minindex[1]] = f"> {minvalue} <"

    Table = BeautifulTable()
    Table.set_style(BeautifulTable.STYLE_GRID)
    Table.columns.append(MinStok, "R \\ Q")
    for col in range(len(NihaiMaliyeList)):
        Table.columns.append(NihaiMaliyeList[col], str(SiparisMiktar[col]))

    SaveTxt("\n\nKARAR TABLOSU:")
    SaveTxt(Table)
    SaveTxt(
        f"En düşük maliyet ({minvalue}) için, Sipariş miktarı (Q) = {SiparisMiktar[minindex[0]]} ve Yeniden sipariş noktası (R) = {MinStok[minindex[1]]} "
    )
    SaveTxt("*" * 125 + "\n\n")


# Çıktı ekrana yazdırır ve kullanıcı isterse text dosyasına yazdırır
def SaveTxt(txt):
    print(txt)
    if TxtDosyasindaKaydet:
        with open("Benzetim Tablosu.txt", "a", encoding="UTF-8") as f:
            f.write((str(txt) + "\n"))


SaveTxt("*Tablo düzgün görünmüyorsa ekranı büyütünüz.\n")


# Kod çalıştırıldığında çalışacak fonksiyonlar
if __name__ == "__main__":
    main()
    KararTablo()
    if TxtDosyasindaKaydet:
        print("Benzetim Tablosu.txt dosyasında kaydedildi.")
