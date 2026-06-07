### Analizler BER Grafiği
### Bu analizi phase 3 işlemi için yaptık.
### main koddaki 45 deneyi aldık.her bir yöntem için BER grafiği çizdik.hoca hepsini tek grafikte istediği için tek grafik oldu

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import str_to_bits, run_hamming_only, run_conv_only, run_concatenated


MESSAGE        = "ECC2026-S09I"
SEED_DEGERLERI = [12013, 17317, 24847]
BERS_DEGERLERI = [0.001, 0.01, 0.05, 0.10, 0.15]

message_bits = str_to_bits(MESSAGE)


yontemler = [("Hamming Only",  run_hamming_only),("Conv Only",     run_conv_only),("Concatenated",  run_concatenated),]   ### Her yöntem için sonuçları topluyoruz                       


### Her yöntem için 15 sonuç
sonuclar = {} ### sonucları tutan dict{}

### sıfır BER değerlerini log skalada göstermek için küçük bir değerle değiştiriyoruz
MIN_BER = 1e-4

for yontem_adi, fonksiyon in yontemler:
    seed_bazli = []   ### her BER için 3 seed sonucu
    ortalama   = []   ### her BER için ortalama

    for ber in BERS_DEGERLERI:
        seed_berleri = []
        for seed in SEED_DEGERLERI:
            _, errors_after, _ = fonksiyon(message_bits, ber, seed)
            post_ber = errors_after / len(message_bits)
            post_ber = max(post_ber, MIN_BER)  ### sıfır yerine MIN_BER koy
            seed_berleri.append(post_ber)
        seed_bazli.append(seed_berleri)
        ortalama.append(np.mean(seed_berleri))

    sonuclar[yontem_adi] = {
        'seed_bazli': seed_bazli,
        'ortalama':   ortalama
    }



### Grafik çizim kısmı matplotlib

renkler  = {'Hamming Only': 'blue', 'Conv Only': 'red', 'Concatenated': 'green'}
markers  = {'Hamming Only': 'o',    'Conv Only': 's',   'Concatenated': '^'}

plt.figure(figsize=(15, 9))

for yontem_adi in sonuclar:
    seed_bazli = sonuclar[yontem_adi]['seed_bazli']
    ortalama   = sonuclar[yontem_adi]['ortalama']

    ### Her seed için ince çizgi çiz
    for j in range(len(SEED_DEGERLERI)):
        seed_sonuclari = [seed_bazli[i][j] for i in range(len(BERS_DEGERLERI))]
        plt.plot(BERS_DEGERLERI, seed_sonuclari,
                 color=renkler[yontem_adi], alpha=0.3, linewidth=1, linestyle='--')

    ### Ortalama çizgisi
    plt.plot(BERS_DEGERLERI, ortalama,
             color=renkler[yontem_adi], linewidth=2,
             marker=markers[yontem_adi], label=yontem_adi)


plt.xscale('log')  ### mühendislikte BER grafikleri log grafiği şeklinde çizilir.aralığımız çok büyük olduğu için kullandık.
plt.yscale('log')
plt.xlabel('Hocanın verdiği BER değerleri')
plt.ylabel('Decoding işleminden sonraki BER değerleri')
plt.title('BER Karşılaştırma Grafiği')
plt.legend()

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('ber_grafik.png', dpi=150)
plt.show()



