import numpy as np



### G_ASSIGNED matrisini buraya ekledik çünkü main kodu yazarken diğer modüllerinde bbu fonksiyona ihtiyaç duyduğunu fark ettim.Ve global değişken olarak tanımladım.


### Hocanın verdiği H matrisinden türetilen G matrisi (11 x 15)
### verify_matrices.py'de GH^T = 0 ile doğrulandı
G_ASSIGNED = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,  1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,  1, 1, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,  1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,  1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,  0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,  0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,  0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,  0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  1, 0, 0, 1],
])

def hamming_encode(message_block, G_matrix):
    ### 1. Mesaj bloğunu G matrisi ile çarpıyoruz.
    encoded_block = np.dot(message_block, G_matrix)
    
    ### 2. GF(2) (İkili sayı sistemi) üzerinde çalıştığımız için Modulo 2 alıyoruz.
    ### Numpy kütüphanesinin normal matris çarpımından doğan çift sayıları (2,4,6,...)-> 0'a,
    ### tek sayıları (1,3,5,7,...) -> 1'e çevirerek toplama işlemini XOR mantığına oturtuyoruz.
    encoded_block = encoded_block % 2
    
    return encoded_block

### --- TEST KISMI ---
if __name__ == "__main__":

    ### verify_matrices.py'de türettiğimiz G matrisi (11 x 15)
    test_G = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,  1, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,  1, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,  1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,  1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,  0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,  0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,  0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,  0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  1, 0, 0, 1],
    ])

    ### 11 bitlik örnek mesajımız
    ornek_mesaj = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0])

    ### Şifreleme fonksiyonumuzu çalıştırıyoruz
    sifrelenmis_mesaj = hamming_encode(ornek_mesaj, test_G)

    print("Orijinal Mesaj: ", ornek_mesaj)
    print("Hamming ile Şifrelenmiş Mesaj: ", sifrelenmis_mesaj)

    ### --- Output doğrulaması:
    ### Mesajımız [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0] olduğu için G matrisinin
    ### 1., 3., 4., 7., 9., 10. satırları (1 olan konumlar) işleme girer.
    ### Sütunlar kendi arasında mod 2 toplanır -> 15 bitlik codeword elde edilir.
    ### Sistematik formda ilk 11 bit orijinal mesajın kendisidir.

    ### parametreleri hocanın verdiği parametrelerle değiştirdim.