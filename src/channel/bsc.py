import numpy as np

def bsc_channel(message_bits, ber, seed):

    ### 1. Rastgeleliği kontrol altına almak için seed'i kuruyoruz.
    np.random.seed(seed)
    
    ### 2. Mesajın uzunluğu kadar, 0 ile 1 arasında rastgele sayılar atıyoruz.
    zarlar = np.random.rand(len(message_bits))
    
    ### 3. Hangi zarlar BER değerinden küçükse,o bitlerin bozulduğunu anlıyoruz.
    ### Örneğin BER = 0.10 ise:0.10'dan küçük gelen sayılar True (hata var) olacak.
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

    received_bits = np.bitwise_xor(message_bits, hata_maskesi.astype(int))
    
    return received_bits


### --- TEST KISMI ---
if __name__ == "__main__":

    ornek_mesaj = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1])

    test_ber = 0.10   ### %10 hata ihtimali
    test_seed = 97    ### Sabit çekirdek
    
    bozulmus_mesaj = bsc_channel(ornek_mesaj, test_ber, test_seed)
    
    print("Orijinal Mesaj: ", ornek_mesaj)
    print("Bozulmuş Mesaj: ", bozulmus_mesaj)