"""   Ahmed Tawfiq   """
"""   B181200553     """
"""     Ödev 2       """

import random
from beautifultable import BeautifulTable
import beautifultable

# TalepMin, TalepMax = input("Talep dağılımın aralığı (arada boşluk bırakarak 'Min Max' şeklinde yazınız): ").split()
# # Olasılık dağılımı ile yapılabilir sonra
# TedarikSure = input("Tedarik süresi: ")
# Stok = input("Başlangıç stok: ")
# Siparis = input("Sipariş miktarı (Q): ")
# MinStok = input("Yeniden sipariş noktası (R): ")
# KayipMaliye = input("Kayıp satış maliyeti / Adet: ")
# StokMaliye = input("Elde bulundurma maliyeti / Adet: ")
# SiparisMaliye = input("Sipariş maliyeti: ")

# Demo data
TalepMin = 80
TalepMax = 130
# Olasılık dağılımı ile yapılabilir sonra
TedarikSure = 2
BasStok = 224
Siparis = 224
MinStok = 200
KayipMaliye = 100
StokMaliye = 0.2
SiparisMaliye = 50

BenZam = list(range(1, 6))
StokList = [BasStok]
TalepList = []
EldeKalan = []
KayipList = []
StokPoz = [BasStok]
SiparisList = [0]
TedarikSureList = []
StokMaliyeList = []
KayipMaliyeList = []
SiparisMaliyeList = []
ToplamMaliyeList = []
def main():
    for i in BenZam:
        TalepList.append(TalepUret())
        EldeKalan.append(StokList[-1]-TalepList[-1])

        if EldeKalan[-1] < 0:
            KayipList.append(-EldeKalan[-1])
            EldeKalan[-1] = 0
        else:
            KayipList.append(0)

        Pozis = StokPoz[-1] - TalepList[-1] + KayipList[-1] + SiparisList[-1]
        StokPoz.append(Pozis)

        if StokPoz[-1] < MinStok:
            SiparisList.append(Siparis)
            TedarikSureList.append(TedarikSure)
            SiparisGelis=TedarikSure
        else:
            SiparisList.append(0)
            TedarikSureList.append(0)
            SiparisGelis-=1

        if SiparisGelis == 0:
            StokList.append(EldeKalan[-1] + SiparisList[-3])
        else:
            StokList.append(EldeKalan[-1])
        
        StokMaliyeList.append(EldeKalan[-1]*StokMaliye)
        KayipMaliyeList.append(KayipList[-1]*KayipMaliye)
        SiparisMaliyeList.append((SiparisList[-1]/Siparis)*SiparisMaliye)
        ToplamMaliyeList.append(StokMaliyeList[-1] + KayipMaliyeList[-1] + SiparisMaliyeList[-1])

    StokList.pop()
    StokPoz.pop(0)
    SiparisList.pop(0)

    


def TalepUret():
    return int(random.uniform(TalepMin, TalepMax))

def CreateTable():
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
    toplam = 0
    for i in ToplamMaliyeList:
        toplam += i
    print("Q={} ve R={} için, Toplam maliyet: {}".format(Siparis, MinStok, toplam))

if __name__ == '__main__':
    main()
    CreateTable()