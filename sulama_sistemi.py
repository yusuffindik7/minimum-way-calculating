# Gerekli olan modülleri ekliyoruz
from collections import defaultdict
from os import remove
import re

# Maliyet tablosunu açıyoruz ve ilk satırdaki veriyi kaynak noktasi olarak tanımlıyoruz
tablo = open("Donem_Odevi/MaliyetTablosu.txt")

kaynak_noktasi = tablo.readline().replace('\n','')

# Satırları ve boşlukları silerek maliyet tablosundaki tüm verileri tek satıra indirgiyoruz
maliyet_tablosu = tablo.read().replace('\n', '')

# Tek satıra indirgediğimiz maliyet_tablosu'ndan sayısal değer içerene mesafe verilerini
# diğer ifadelerden ayırıyoruz ve istenmeyen işaretleri silip sadece noktaları belirliyoruz ve
# noktalar adında liste oluşturuyoruz 
mesafeler = re.sub('\D', '', maliyet_tablosu) 
noktalar = ''.join(i for i in maliyet_tablosu if not i.isdigit())
noktalar = re.split('[-:]', noktalar)
noktalar = [x for x in noktalar if len(x.strip()) > 0]

# Oluşturduğumuz tüm noktaları maliyet tablosunda verildiği gibi başlangıc ve hedef noktası
# şeklinde tanımlamak için noktalar dizisine baktığımızda mantıken indexi tek sayı olanları başlangıç, 
# çift sayı olanları ise hedef nokta olarak ayırıyoruz ve ayrı listeler oluşturuyoruz.
# Mesafeler için sayısal değerleri aldığımızda string olarak gözüktüğünden sayısal liste oluşturuyoruz
noktalar_baslangic = noktalar[::2]
noktalar_hedef = noktalar[1::2]
mesafeler = list(map(int, mesafeler))
    
# Algoritmada noktalar numerik gösterilmesi gerektiğinden stringleri key olarak alıp
# keylere karşılık sayısal değerler vermek için boş bir sözlük oluşturuyoruz
noktalar_numerik = {}

# Noktalar dizisindeki birbirinden farklı noktaları
# noktalar_numerik adında bir sözlüğe ekliyoruz ve
# her farklı noktayı anahtar olarak tanımlayıp anahtarları da 
# x = 0 dan başlayacak şekilde numaralandırıyoruz
x = 0
for i in noktalar:
    if i not in noktalar_numerik:
        noktalar_numerik[i] = x
        x += 1      

# Algoritma sayısal değerlerle çalıştığından çıktı alırken
# değerlere karşılık gelen keyleri göstermek için key ve value list oluşturduk
key_list = list(noktalar_numerik.keys())
value_list = list(noktalar_numerik.values())

# Minimum mesafe/maliyet için Kruskal Algoritması'nı kullanıyoruz
# Oluşturacağımız ağaç grafiği için graph adında bir sınıf var 
class Graph:
 
    def __init__(self, vertices):
        self.V = vertices  # Köşe noktaları/numaraları
        self.graph = []  # Boş grafik listesi
 
    # Grafiğe başlangıç, hedef ve mesafe noktaları ekleme
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
 
    # i eleman kümesini bulmaya yarayan fonksiyon
    # (yol sıkıştırma tekniği)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
 
    # x ve y kümesini birleştiren fonksiyon
    # (union fonksiyonu büyüklüğe göre sıralar)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
 
        # Ağaçtaki en yüksek köke en düşük kökü ekler?
        # (büyüklüğe göre birleştiriyor)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
 
        # Eğer büyüklükleri aynıysa bir kök daha oluşturup
        # büyüklüğünü bir arttırıyor
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
 
    # Minimum mesafe/maliyet işleme için Kruskal Algoritması'nın ana fonksiyonu
    def KruskalMST(self):
 
        result = []  # ortaya çıkan ağaç
         
        # sıralanmış kenarlar için dizin değişkeni
        i = 0
         
        # result[] için dizin değişkeni
        e = 0

        # İlk olarak tüm kenar noktalarını azalmama sırasına göre sıralıyor ve liste oluşturuyoruz
        self.graph = sorted(self.graph,
        # Hangi noktadan itibaren sıralanacağı konusunda takıldım,
        # item içerisinde kaynak noktasının numara karşılığını yazarak oradan başlatmak istedim fakat
        # galiba kaynak başlangıç, hedef ve mesafe olarak oluşturulan ağacın indexi belirleniyor
        # bu yüzden bu kısımda takıldım. 
                        key=lambda item: item[noktalar_numerik[kaynak_noktasi]])

        # Oluşan grafikte seçeceğimiz bir noktadan başlatmak için öncelikle aşağıdaki döngüyü kullanmaya çalıştım
        # baslangic, sıralanmış listenin içinde dolaşıp her index içerisinde belirlediğimiz noktanın en kısa mesafeye sahip
        # olanını bulup o indexten itibaren listenin yeniden sıralanmasını denemeye çalıştım maalesef olmadı.
         
        #for baslangic in self.graph:

        #    if noktalar_numerik[kaynak_noktasi] in self.graph[baslangic][0]:

        #        self.graph = sorted(self.graph,
        #                        key=lambda item: item[baslangic])

        parent = []
        rank = []
 
        # V adında alt küme oluşturuluyor
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
 
        # Alınan kenar noktası V-1 e eşittir
        while e < self.V - 1:
 
            # Son olarak en küçük noktayı seçip bir sonraki işlem için dizini bir arttırıyor

            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
 
            # Eğer bu nokta eklendiğinde döngüye dahil olmazsa
            # sonuca ekleyip bir sonraki nokta için sonuç dizinini arttırıyor

            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            # Aksi halde noktayı atıyor
 
# Oluşturulan MST haritasını gösteriyoruz, result içerisindeki u(baslangic noktasi), v(hedef noktasi)
# değerlerine karşılık keyleri ve mesafeyi yazdırıyoruz
        minimumCost = 0
        print("\nKaynak noktası {} için oluşturulan MST haritası:\n" .format(kaynak_noktasi)) 
       
        for u, v, weight in result:        
            minimumCost += weight 
            print("{} -- {} = %d" .format(key_list[value_list.index(u)], key_list[value_list.index(v)]) % weight)

        print("\nMinimum Maliyet:" , minimumCost)

# Grafikte kaç nokta olduğunu noktalar_numerik listesinden alıyoruz ve
# grafiğe büyüklüğünü tanımlıyoruz
g = Graph(len(noktalar_numerik))

# Eğer 50'den fazla nokta/tarla varsa print içerisindeki mesajı yazdırıyoruz
if len(noktalar_numerik) > 50:
    print('Maksimum 50 Adet Tarla Olabilir!')

# 50'den küçükse başlangıç noktalarına karşılık bir de hedef nokta ve mesafe olduğundan
# grafiğe eklemek için noktalar_baslangic içerisinde i döndürerek 
# string değerini teker teker bulup noktalar_numerik sözlüğündeki hangi sayıya denk geldiğini
# dizi 0 dan başlayacak şekilde(sayısal olması gerekiyor i yazamayız bu yüzden) buluyoruz ve
# mesafe ile birlikte ekliyoruz  
else:
    x=0
    for i in noktalar_baslangic:
        g.addEdge(noktalar_numerik[noktalar_baslangic[x]], noktalar_numerik[noktalar_hedef[x]], mesafeler[x])
        x += 1

# Fonksiyonu çağırıyoruz
g.KruskalMST()