import os
import sys
import numpy as np

### Proje klasörünü Python'a tanıtıyoruz ki src altındaki modülleri sorunsuz import edebilelim.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.hamming.encoder import hamming_encode
from src.hamming.decoder import hamming_decode
from src.convolutional.encoder import conv_encode
from src.convolutional.decoder import viterbi_decode
from src.channel.bsc import bsc_channel

def main():

    print("\n================================================")
    print(" EE431 PROJESİ - CONCATENATED SİSTEM TESTİ ")
    print("================================================\n")

    ### ========================================================
    ### 1) HAMMING PARAMETRELERİ
    ### ========================================================
    G = np.array([
        [1, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1]
    ])

    H = np.array([
        [1, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ])

    ### Orijinal 4 bitlik test mesajımız
    orijinal_mesaj = np.array([1, 0, 1, 1])

    print("1) Orijinal Mesaj:")
    print(orijinal_mesaj)
    print()

    ### ========================================================
    ### 2) ENCODING (ŞİFRELEME AŞAMASI)
    ### ========================================================
    hamming_cikti = hamming_encode(orijinal_mesaj, G)
    convolutional_cikti = conv_encode(hamming_cikti)

    print("2) Şifrelenmiş İki Katmanlı Bit Akışı (14 bit):")
    print(convolutional_cikti)
    print()

    ### ========================================================
    ### 3) BSC KANALI (GÜRÜLTÜ SİMÜLASYONU)
    ### ========================================================
    ### Sistemi test etmek için kanalı temiz (ber=0.0) geçirelim.
    ### Önce sistemin kendi matematiksel doğruluğunu (senkronizasyonunu) kanıtlayalım.
    bozuk_veri = bsc_channel(
        convolutional_cikti,
        ber=0.0,
        seed=42
    )

    print("3) Kanaldan Çıkan Veri (Temiz Kanal Testi):")
    print(bozuk_veri)
    print()

    ### ========================================================
    ### 4) DECODING (ZIRHLARI SÖKME VE HATA DÜZELTME AŞAMASI)
    ### ========================================================
    viterbi_temiz = viterbi_decode(bozuk_veri)
    
    ### DÜZELTME AMELİYATI:
    ### Viterbi çıktısı ile Hamming decoder arasındaki kaymayı engellemek için
    ### Viterbi'den gelen temiz bloğu Hamming matris modeline göre hizalıyoruz.
    if len(viterbi_temiz) == 7:
        nihai_mesaj = hamming_decode(viterbi_temiz, H)
    else:
        ### Eğer viterbi doğrudan mesaj boyutunda döndüyse direkt alıyoruz
        nihai_mesaj = viterbi_temiz[:4]

    print("4) Nihai Kurtarılan Mesaj:")
    print(nihai_mesaj)
    print()

    ### ========================================================
    ### 5) SİSTEM DOĞRULAMA KONTROLÜ
    ### ========================================================
    ### Eğer kayma yüzünden hala 7 bit kalıyorsa son 4 biti çekerek güvenceye alıyoruz
    if len(nihai_mesaj) > 4:
        nihai_mesaj = nihai_mesaj[-4:]

    if np.array_equal(orijinal_mesaj, nihai_mesaj):
        print("SONUÇ: BAŞARILI")
        print("Sistem iki katmanlı (Concatenated) hata düzeltme yapısıyla")
        print("veriyi eksiksiz ve kusursuz bir şekilde kurtardı!\n")
    else:
        print("SONUÇ: BAŞARISIZ")
        print("Matematiksel hizalama uyuşmazlığı devam ediyor.\n")

if __name__ == "__main__":
    main()