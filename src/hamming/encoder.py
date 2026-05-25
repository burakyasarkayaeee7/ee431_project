import numpy as np

def hamming_encode(message_block, G_matrix):
    ### 1. Mesaj bloğunu G matrisi ile çarpıyoruz.
    encoded_block = np.dot(message_block, G_matrix)
    
    ### 2. GF(2) (İkili sayı sistemi) üzerinde çalıştığımız için Modulo 2 alıyoruz.
    ### Numpy kütüphanebsinin normal matris çarpımından doğan çift sayıları (2,4,6,...)-> 0'a,
    ### tek sayıları (1,3,5,7,...) -> 1'e çevirerek toplama işlemini XOR mantığına oturtbmaya çalışırızz.
    encoded_block = encoded_block % 2
    
    return encoded_block

### --- TEST KISMI ---
if __name__ == "__main__":
    ###
    ### Test için rastgele bir G matrisi (*******Hoca parametreleri verince bu ksımı depiştir *******)
    ###

    test_G = np.array([
        [1, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1]
    ])
    
    ### 4 bitlik uydurma mesajımız
    ornek_mesaj = np.array([1, 0, 1, 1])
    
    ### Şifreleme fonksiyonumuzu çalıştırıyoruz
    sifrelenmis_mesaj = hamming_encode(ornek_mesaj, test_G)
    
    print("Orijinal Mesaj: ", ornek_mesaj)
    print("Hamming ile Şifrelenmiş Mesaj: ", sifrelenmis_mesaj)

    ### --- Output doğrulaması ve Nasıl elde ettik?
    ### Mesajımız [1, 0, 1, 1] olduğu için G matrisinin 1., 3. ve 4. satırları işleme sokarız.
    ### 2. satır 0 ile çarpıldığı için 2. satırı kullanmayız.
    ###
    ### 1. Satır: [1, 1, 0, 1, 0, 0, 0]
    ### 3. Satır: [1, 1, 1, 0, 0, 1, 0]
    ### 4. Satır: [1, 0, 1, 0, 0, 0, 1]
    ### Sütunbları kendi arasında toplayınca aşağıdaki gibi code bloğu elde ederiz
    ### Normal Toplam: [3, 2, 2, 1, 0, 1, 1]
    ### Modulo 2:      [1, 0, 0, 1, 0, 1, 1] (Çift sayılar 0, tek sayılar 1 yaptık).