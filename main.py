import numpy as np
from src.hamming.encoder import hamming_encode
from src.hamming.decoder import hamming_decode
from src.channel.bsc import bsc_channel

def main():
    print("\n=== EE431 Projesi: Hamming Hata Düzeltme Sistemi Uçtan Uca Testi ===\n")

    ### 1. PARAMETRELER (Hoca verene kadar uydurma değerler)
    test_G = np.array([
        [1, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1]
    ])

    test_H = np.array([
        [1, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ])

    ornek_mesaj = np.array([1, 0, 1, 1])
    test_ber = 0.15 # Hata çıkma ihtimali
    test_seed = 42  # Gürültüyü sabitlemek için (42 seed'i 1 bitlik hata üretir)

    print("1. Orijinal Mesaj:           ", ornek_mesaj)

    ### 2. ŞİFRELEME (ENCODING)
    sifreli_mesaj = hamming_encode(ornek_mesaj, test_G)
    print("2. Şifrelenmiş Mesaj (Tx):   ", sifreli_mesaj)

    ### 3. KANAL (BSC - GÜRÜLTÜ EKLENMESİ)
    kanaldan_gelen_mesaj = bsc_channel(sifreli_mesaj, test_ber, test_seed)
    print("3. Kanaldan Çıkan Mesaj (Rx):", kanaldan_gelen_mesaj)

    # Kanaldaki hatayı görselleştirelim (XOR ile farkı buluyoruz)
    hatalar = sifreli_mesaj ^ kanaldan_gelen_mesaj
    if np.any(hatalar):
        print("   --> KANALDA HATA OLUŞTU! Bozulan bitler: ", hatalar)
    else:
        print("   --> KANALDA HATA OLUŞMADI.")

    ### 4. ÇÖZME VE DÜZELTME (DECODING)
    duzeltilmis_mesaj = hamming_decode(kanaldan_gelen_mesaj, test_H)
    print("4. Dekoder Çıktısı (Düzeltildi):", duzeltilmis_mesaj)

    ### 5. SONUÇ KONTROLÜ
    if np.array_equal(sifreli_mesaj, duzeltilmis_mesaj):
        print("\nSONUÇ: BAŞARILI! Sistem kanaldaki hatayı yakaladı ve başarıyla düzeltti.")
    else:
        print("\nSONUÇ: BAŞARISIZ! (Hamming sadece 1 bitlik hataları düzeltebilir, çoklu hata oluşmuş olabilir).")

if __name__ == "__main__":
    main()