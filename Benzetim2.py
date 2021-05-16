"""   Ahmed Tawfiq   """
"""   B181200553     """
"""     Ödev 2       """

import random
from beautifultable import BeautifulTable

############
Demo = True
############


if not Demo:
    TalepMin, TalepMax = input(
        "Talep dağılımın aralığı (arada boşluk bırakarak 'Min Max' şeklinde yazınız): "
    ).split()
    # Olasılık dağılımı ile yapılabilir sonra
    # TedarikSure = input("Tedarik süresi: ")
    Stok = input("Başlangıç stok: ")
    # Siparis = input("Sipariş miktarı (Q): ")
    # MinStok = input("Yeniden sipariş noktası (R): ")
    KayipMaliye = input("Kayıp satış maliyeti / Adet: ")
    StokMaliye = input("Elde bulundurma maliyeti / Adet: ")
    SiparisMaliye = input("Sipariş maliyeti: ")
    DevreSayi = input("Çalıştırılacak devre sayısı: ")

else:
    # Demo data
    TalepMin = 80
    TalepMax = 130
    BasStok = 224
    Siparis = [224, 275, 325, 400]
    MinStok = [200, 225, 250, 275, 300]
    KayipMaliye = 100
    StokMaliye = 0.2
    SiparisMaliye = 50
    DevreSayi = 5

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
    for Q in Siparis:
        GeciciMaliyeList = []
        for R in MinStok:
            ClearData()
            StokList.append(BasStok)
            StokPoz.append(BasStok)
            SiparisList.append(0)
            for B in BenZam:
                TalepList.append(TalepUret())
                EldeKalan.append(StokList[-1] - TalepList[-1])

                if EldeKalan[-1] < 0:
                    KayipList.append(-EldeKalan[-1])
                    EldeKalan[-1] = 0
                else:
                    KayipList.append(0)

                Pozis = StokPoz[-1] - TalepList[-1] + KayipList[-1] + SiparisList[-1]
                StokPoz.append(Pozis)

                if StokPoz[-1] < R:
                    SiparisList.append(Q)
                    TedarikSure = TedarikSureUret()
                    TedarikSureList.append(TedarikSure)
                    SiparisGelis = TedarikSure
                else:
                    SiparisList.append(0)
                    TedarikSureList.append(0)
                    SiparisGelis -= 1

                if SiparisGelis == 0:
                    StokList.append(EldeKalan[-1] + SiparisList[-3])
                else:
                    StokList.append(EldeKalan[-1])

                StokMaliyeList.append(EldeKalan[-1] * StokMaliye)
                KayipMaliyeList.append(KayipList[-1] * KayipMaliye)
                SiparisMaliyeList.append((SiparisList[-1] / Q) * SiparisMaliye)
                ToplamMaliyeList.append(
                    StokMaliyeList[-1] + KayipMaliyeList[-1] + SiparisMaliyeList[-1]
                )
            StokList.pop()
            StokPoz.pop(0)
            SiparisList.pop(0)

            Toplam = round(sum(ToplamMaliyeList), 1)
            GeciciMaliyeList.append(Toplam)
            BenzetimTablo()
            print("Q={} ve R={} için, Toplam maliyet: {} \n\n".format(Q, R, Toplam))

        NihaiMaliyeList.append(GeciciMaliyeList)


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


def TalepUret():
    return int(random.uniform(TalepMin, TalepMax))


def TedarikSureUret():
    return int(random.choices([2, 3], weights=[0.75, 0.25])[0])


def BenzetimTablo():
    Table = BeautifulTable()
    Table.columns.append(BenZam, "Benzetim\nzamanı")
    Table.columns.append(StokList, "Başlangıç\nstok")
    Table.columns.append(TalepList, "Talep")
    Table.columns.append(EldeKalan, "Elde\nkalan")
    Table.columns.append(KayipList, "Kayıp")
    Table.columns.append(StokPoz, "Stok\npozisyon")
    Table.columns.append(SiparisList, "Açılan\nsipariş")
    Table.columns.append(TedarikSureList, "Tedarik\nsüresi")
    Table.columns.append(StokMaliyeList, "Elde\nbulundurma\nmaliyeti")
    Table.columns.append(KayipMaliyeList, "Kayıp\nsatış\nmaliyeti")
    Table.columns.append(SiparisMaliyeList, "Sipariş\nmaliyeti")
    Table.columns.append(ToplamMaliyeList, "Toplam\nmaliye")
    Table.set_style(BeautifulTable.STYLE_SEPARATED)
    Table.columns.width = 11

    print(Table)


def KararTablo():
    Table = BeautifulTable()
    Table.columns.append(MinStok, "R \\ Q")
    for col in range(len(NihaiMaliyeList)):
        Table.columns.append(NihaiMaliyeList[col], str(Siparis[col]))

    print(Table)


if __name__ == "__main__":
    main()
    KararTablo()
