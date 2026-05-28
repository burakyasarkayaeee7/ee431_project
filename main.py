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

    ### 2. ŞİFRELEME (ENCODING)import numpy as np
from src.channel.bsc import bsc_channel
from src.hamming.encoder import hamming_encode  # Yazdığın Hamming şifreleyici
from src.hamming.decoder import hamming_decode  # Yazdığın Hamming çözücü
from src.convolutional.encoder import conv_encode  # Yeni formüllü Evrişimli şifreleyici
from src.convolutional.decoder import viterbi_decode  # Yeni formüllü Viterbi çözücü

def main():
    print("\n=== EE431 Projesi: Concatenated (Birleşik) Kodlama Sistemi Uçtan Uca Testi ===\n")

    # =========================================================================
    # 1. PARAMETRELER (Hamming Matrisleri)
    # =========================================================================
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
    test_ber = 0.10  # Kanal gürültü oranı (%10)
    test_seed = 42   # Gürültü maskesini sabitlemek için

    print("1. Orijinal Mesaj:                ", ornek_mesaj)

    # =========================================================================
    # 2. ŞİFRELEME (ENCODING STAGE) - İKİ KAT ZIRH
    # =========================================================================
    # Katman A: Hamming Encoding (İç Kodlama) -> 4 bitlik mesaj 7 bite çıkıyor
    hamming_sifreli = hamming_encode(ornek_mesaj, test_G)
    print("2. Katman A - Hamming Çıktısı (7 bit): ", hamming_sifreli)

    # Katman B: Convolutional Encoding (Dış Kodlama) -> 7 bitlik veri 14 bite çıkıyor
    tam_sifreli_mesaj = conv_encode(hamming_sifreli)
    print("3. Katman B - Evrişimli Çıktı (14 bit):", tam_sifreli_mesaj)

    # =========================================================================
    # 3. KANAL (BSC - GÜRÜLTÜ EKLENMESİ)
    # =========================================================================
    kanaldan_gelen_mesaj = bsc_channel(tam_sifreli_mesaj, test_ber, test_seed)
    print("4. Kanaldan Çıkan Bozuk Mesaj (Rx):    ", kanaldan_gelen_mesaj)

    # Kanalda oluşan toplam hata sayısını bulalım
    toplam_hata = np.sum(tam_sifreli_mesaj != kanaldan_gelen_mesaj)
    print(f"   --> Kanalda toplam {toplam_hata} bit gürültüden dolayı bozuldu!")

    print("\n-----------------------------------------------------------------")
    print("   DECODING (HATA DÜZELTME VE ÇÖZME STAGE) BAŞLADI...")
    print("-----------------------------------------------------------------\n")

    # =========================================================================
    # 4. ÇÖZME VE DÜZELTME (DECODING STAGE)
    # =========================================================================
    # Katman B'yi Çözme: Viterbi Decoder gürültüyü temizleyip 14 biti tekrar 7 bite düşürüyor
    viterbi_temiz = viterbi_decode(kanaldan_gelen_mesaj)
    print("5. Katman B - Viterbi Çıktısı (7 bit): ", viterbi_temiz)

    # Katman A'yı Çözme: Hamming Decoder kalan mikro hataları temizleyip orijinal 4 biti çıkarıyor
    nihai_mesaj = hamming_decode(viterbi_temiz, test_H)
    print("6. Katman A - Hamming Çıktısı (Nihai): ", nihai_mesaj)

    # =========================================================================
    # 5. SONUÇ KONTROLÜ
    # =========================================================================
    if np.array_equal(ornek_mesaj, nihai_mesaj):
        print("\nSONUÇ: MÜKEMMEL BAŞARI! İki katmanlı sistem birleşerek kanaldaki tüm gürültüyü yok etti.")
    else:
        print("\nSONUÇ: BAŞARISIZ! Çok yoğun gürültü oluştu, sistem limitlerini aştı.")

if __name__ == "__main__":
    main()
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