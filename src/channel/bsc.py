import numpy as np

def bsc_channel(message_bits, ber, seed):

    ### 1. Rastgeleliği kontrol altıbna almak için seed'i kuruyoruz.
    np.random.seed(seed)  ### amacımız sistemi her çalıştırdığımızda aynı rastgelelikte yapmak istememiz.
    
    ### 2. Mesajın uzunluğu kadar, 0 ile 1 arasında rastgele sayılar atıyoruz.
    zarlar = np.random.rand(len(message_bits))
    
    ### 3. Hangi zarlar BER değerinden küçükse,o bitlerin bozulduğunu anlıyoruz.
    ### Örneğin BER = 0.10 ise:0.10'dan küçük gelen sayılar (true) hata var demek olacak.
    hata_maskesi = zarlar < ber
    
    ### 4. Hata olan yerleri ters çeviriyoruz (XOR işlemi)
    ### XOR mantığı:
    ### Eğer hata_maskesi 1 ise bit ters döner.
    ### Eğer hata_maskesi 0 ise bit aynı kalır.
    ### XOR Tablosu:
    ###
    ### Bit | Hata | Sonuç
    ### -------------------
    ###  0  |   0  |   0
    ###  1  |   0  |   1
    ###  0  |   1  |   1
    ###  1  |   1  |   0
    ###
    ### Özet:
    ### Hata = 0 --> bit değişmez.
    ### Hata = 1 --> bit flip olur (0->1, 1->0).

    received_bits = np.bitwise_xor(message_bits, hata_maskesi.astype(int)) ### .asttype true false'u 1 veya 0'a dönüştürür.
    
    return received_bits


### --- TEST KISMI ---
if __name__ == "__main__":

    ### Kişisel mesajımız: ECC2026-S09I 8*12= 96 bit
    mesaj = "ECC2026-S09I" 
    # Karakter | ASCII | 8-Bitlik Gösterim
    # ---------+-------+------------------
    #    E     |  69   | 01000101
    #    C     |  67   | 01000011
    #    C     |  67   | 01000011
    #    2     |  50   | 00110010
    #    0     |  48   | 00110000
    #    2     |  50   | 00110010
    #    6     |  54   | 00110110
    #    -     |  45   | 00101101
    #    S     |  83   | 01010011
    #    0     |  48   | 00110000
    #    9     |  57   | 00111001
    #    I     |  73   | 01001001
    ### burada her karakterin ASCII standartındaki 8 bitlik karşılıklarını yazdık.toplamda 96 bit

    bits = []
    for harf in mesaj:
        for bit in format(ord(harf), '08b'):  ### burada ord() ifadesi ASCII standartındaki onluk karşılık.
            bits.append(int(bit))             ####'08b' ise bu sayıyı başına eksik sıfırları ekleyerek net 8 bitlik binary (ikilik) metne dönüştürür.
    ornek_mesaj = np.array(bits)

    test_ber  = 0.10    ### Parametre sayfasındaki BER değerlerinden biri
    test_seed = 12013   ### Parametre sayfasındaki ilk seed

    bozulmus_mesaj = bsc_channel(ornek_mesaj, test_ber, test_seed)

    print("Orijinal Mesaj: ", ornek_mesaj)
    print("Bozulmuş Mesaj: ", bozulmus_mesaj)

    ### parametreleri hocanın verdiği parametrelerle değiştirdim.

    ### Bu kod sadece BSC kanalı testi
    ### Asıl 45 deney main.py'de yapılacak.
    ### main kodda 3 scheme Hamming, Conv, Concatenated x 5 BER x 3 seed = 45 denbey