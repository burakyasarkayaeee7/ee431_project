import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__))) ### Çalışan dosyanın bulunduğu klasörü modül arama yollarına ekliyoruz.

from main import str_to_bits        ### mesajı bit dizisine çeviren fonksiyon
from main import run_hamming_only   ### sadece Hamming deneyi
from main import run_conv_only      ### sadece Convolutional deneyi
from main import run_concatenated   ### concatenated deney
from main import MESSAGE            ### "ECC2026-S09I"
from main import SEED_DEGERLERI     ### [12013, 17317, 24847]
from main import BERS_DEGERLERI     ### [0.001, 0.01, 0.05, 0.10, 0.15]

######################################################################################
### Post decoding BER 

### Hocanın grafiğinin Y ekseni "post-decoding BER" istiyor. Hata SAYISI yerine hata oranı istiyoruz.
###
### post-decoding BER = (decode sonrası kalan hata) / (toplam mesaj biti)
###

TOPLAM_BIT = len(str_to_bits(MESSAGE))


def post_decoding_ber(hata_sonra):
    """Kalan hata sayısını orana çevirir."""
    return hata_sonra / TOPLAM_BIT


### Post-decoding BER = 0 olduğunda log grafikte çizilemez
### log(0) tanımsız. Bu yüzden 0 olan noktaları çok küçük bir taban değerine sabitledik.
### 10^-4 seçtik çünkü 96 bitte düzeltilebilecek en küçük anlamlı oranın altında kalıyor ve grafik temiz duruyor.
TABAN_BER = 1e-4  ### bu 10 üzeri -4 demek


def grafik_icin_duzelt(ber_degeri):
    if ber_degeri <= 0:
        return TABAN_BER
    return ber_degeri


#####################
### Tüm deneyleri çalıştırıp sonuçları toplayacağız.

### Her yöntem için:
### Her BER de, her seedin post-decoding BER kaydediyoruz sonra seedlerin ortalamasını alıyoruz...


def deneyleri_calistir():
    message_bits = str_to_bits(MESSAGE)

    yontemler = {
        "Hamming Only":  run_hamming_only,
        "Conv Only":     run_conv_only,
        "Concatenated":  run_concatenated,
    }

    ### Yapıyı senin istediğin gibi daha toplu ve net şekilde tanımlıyoruz.
    sonuclar = {
        "Hamming Only": {
            "ortalama": [],
            "seedler": { 12013: [], 17317: [], 24847: [] } ### buralara her bir seed değeri için 5 farklı BER değeri gelicek
        },
        "Conv Only": {
            "ortalama": [],
            "seedler": { 12013: [], 17317: [], 24847: [] } ### buralara her bir seed değeri için 5 farklı BER değeri gelicek
        },
        "Concatenated": {
            "ortalama": [],
            "seedler": { 12013: [], 17317: [], 24847: [] } ### buralara her bir seed değeri için 5 farklı BER değeri gelicek
        }
    }



    ### 3 yöntem x 5 BER x 3 seed = 45 deney
    for yontem_adi, deney in yontemler.items():

        for ber in BERS_DEGERLERI:

            ### Bu BER değerinde 3 seed'i sırayla çalıştırıyoruz
            seed_berleri = []

            for seed in SEED_DEGERLERI:

                ### Deneyi çalıştır, sadece hata_sonra değerini alıyoruz
                ### hata_once ve hatasiz burada işimize yaramıyor, _ ile atlıyoruz
                _, hata_sonra, _ = deney(message_bits, ber, seed)

                ### Hata SAYISINI hata ORANINA çeviriyoruz
                ### Örnek: 14 hata / 96 bit = 0.1458 BER
                pd_ber = post_decoding_ber(hata_sonra)

                ### Hata 0 ise log grafikte çizilemez, tabana sabitliyoruz
                pd_ber_grafik = grafik_icin_duzelt(pd_ber)

                ### pd_ber → ortalama hesabı için ham değer listesine
                ### pd_ber_grafik → bu seed'in grafikte çizilecek izine
                seed_berleri.append(pd_ber)
                sonuclar[yontem_adi]["seedler"][seed].append(pd_ber_grafik)

            ### 3 seed'in ortalamasını alıp ortalama listesine ekliyoruz
            ### np.mean([a, b, c]) = (a+b+c)/3
            ortalama = np.mean(seed_berleri)
            sonuclar[yontem_adi]["ortalama"].append(grafik_icin_duzelt(ortalama))

    return sonuclar


#############################################################
### Grafik aşaması hocanın belirttiği şekilde 


### Produce a single plot of post-decoding BER versus channel BER for the three schemes, averaged over your three seeds, with all three individual seed traces shown.
###

### Yani TEK grafikte:


def grafik_ciz(sonuclar):   ### deneyleri calistir fonksiyonundan sonuçlar dict{} geldi


    renkler = {"Hamming Only":  "blue",     "Conv Only":    "red",     "Concatenated":  "green",}

    plt.figure(figsize=(15, 9))

    for yontem_adi, veri in sonuclar.items():  ### yöntemleri sırayla döngüye aliyoruz. veri o yöntemlerin seed vbe ortalma dizilerinni içeriyor.
        renk = renkler[yontem_adi]

        for seed in SEED_DEGERLERI:
            plt.plot(
                BERS_DEGERLERI, ### x ekseni 5 BER değeri
                veri["seedler"][seed], ### post decode sonrasi BER değerleri
                linestyle="--",     ### kesik çizgi
                color=renk,
                alpha=0.3,
                linewidth=1,
            )


        plt.plot(
            BERS_DEGERLERI,
            veri["ortalama"], ### 3 seed in ortalamasi
            linestyle="-",
            color=renk,
            marker="o",
            linewidth=2.5,
            markersize=7,
            label=yontem_adi,
        )

    ### Log ölçeğinde çizdik.BER değer aralıkları baya fazla çünkü
    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Kanal BER (Hocanın verdiği BER değerleri)")
    plt.ylabel("Post-Decoding BER (decode sonrası hata oranı)")
    plt.title("Post-Decoding BER vs Kanal BER")

    plt.grid(True, which="both", linestyle=":", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.show()


###############################################################################


if __name__ == "__main__":
    sonuclar = deneyleri_calistir()

    ### Sonuçları yazdırdık


    print("\nPost-Decoding BER ortalamalari:")
    print(f"{'Yontem':<16}", end="")
    for ber in BERS_DEGERLERI:
        print(f"{ber:>10}", end="")
    print()
    for yontem_adi, veri in sonuclar.items():
        print(f"{yontem_adi:<16}", end="")
        for deger in veri["ortalama"]:
            print(f"{deger:>10.5f}", end="")
        print()

    grafik_ciz(sonuclar)