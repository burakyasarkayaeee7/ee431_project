import numpy as np


### hocanın verdiği paramerteleri test etmek amacıyla yaptım

# Parametre sayfasından aldığım H matrisi (4 x 15)
H = np.array([
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1]
])
# H matrisinin içinden P^T kısmını alma işlemi.Bu kod şöyle oluyor.15 sütubnumuz var ilk 11 sütubnu aldı.
P_T = H[:, :11]

# P matrisinin transpobnunu oluşturuyoruz
P = P_T.T

# G = [I_11 | P] oluşturuluyor
I_11 = np.eye(11, dtype=int) ### np.eye birim matris fonksiyonu yaptık.ve (int) tam sayı yaptık.
G = np.hstack((I_11, P))     ### matrisleri yatay olarak birleştirir.

print("G matrisi:")
print(G)

# TEST 1: Boyut kontrolü
print("H boyutu:", H.shape, "-> beklenen (4, 15)")
print("G boyutu:", G.shape, "-> beklenen (11, 15)")
print() ### 1 satır boşluk bırakır

# TEST 2: Sistematik form kontrolü
print("H'nin son 4 sğtunu birim matris olmalı:")
print(H[:, 11:]) ### burada 12 13 14 15. sütüunlardaki değerleri alarak.birim matris olup olmadığını kontrol ettik.
print()

# TEST 3: Ana doğrulama G * H^T = 0 (mod 2)

### XOR mantığı:
### Eğer hata_maskesi 1 ise bit ters döner.
### Eğer hata_maskesi 0 ise bit aynı kalır.
### XOR Tablosu:
###
### Bit | Hata | Sonuç
### ------------------
###  0  |  0   |   0
###  1  |  0   |   1
###  0  |  1   |   1
###  1  |  1   |   0
###
### Özet:
### Hata = 0 --> bit değişmez.
### Hata = 1 --> bit flip olur (0->1, 1->0).
verification = np.dot(G, H.T) % 2
print("G * H^T sonucu 0 olmalı:")
print(verification)
print()

if not np.any(verification):
    print("SONUÇ BAŞARILI: G * H^T (mod 2) işlemi sıfır matrisini verdi.")
else:
    print("HATA: Matrisler uyuşmuyor!")

# TEST 4: Örnek bir mesajı encode edip sendromunu kontrol edelim
test_mesaj = np.array([1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0])
codeword = np.dot(test_mesaj, G) % 2
sendrom = np.dot(codeword, H.T) % 2

print("Test mesajı:", test_mesaj)
print("Codeword   :", codeword)
print("Sendrom    :", sendrom, "-> sıfır olmalı")

if not np.any(sendrom):
    print("SONUÇ BAŞARILI: Codeword geçerli, sendrom sıfır.")
else:
    print("HATA: Codeword geçersiz!")