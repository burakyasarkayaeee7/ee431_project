import numpy as np

def bsc_channel(message_bits, ber, seed):
    # 1. Rastgeleliği kontrol altına almak için seed'i kuruyoruz
    np.random.seed(seed)
    
    # 2. Mesajın uzunluğu kadar, 0 ile 1 arasında rastgele sayılar (zarlar) atıyoruz
    zarlar = np.random.rand(len(message_bits))
    
    # 3. Hangi zarlar BER değerinden küçükse, o bitlerin bozulduğunu anlıyoruz
    # Örneğin BER 0.10 ise, 0.10'dan küçük gelen zarlar True (hata var) olacak
    hata_maskesi = zarlar < ber
    
    # 4. Hata olan yerleri ters çeviriyoruz (XOR işlemi)
    # XOR (^) mantığı: Gelen bit 1 ve hata_maskesi 1 ise sonuç 0 olur (bozuldu)
    received_bits = np.bitwise_xor(message_bits, hata_maskesi.astype(int))
    
    return received_bits

# --- TEST KISMI ---
if __name__ == "__main__":
    ornek_mesaj = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1])
    test_ber = 0.20 # %20 hata ihtimali
    test_seed = 42  # Sabit çekirdek
    
    bozulmus_mesaj = bsc_channel(ornek_mesaj, test_ber, test_seed)
    
    print("Orijinal Mesaj: ", ornek_mesaj)
    print("Bozulmuş Mesaj: ", bozulmus_mesaj)