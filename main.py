import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.hamming.encoder import hamming_encode, G_ASSIGNED
from src.hamming.decoder import hamming_decode, H_ASSIGNED  ### H_ASSIGNED de import ettik
from src.convolutional.encoder import conv_encode
from src.convolutional.decoder import viterbi_decode
from src.channel.bsc import bsc_channel

####################################
### EE431 Project Burak Yaşar Kaya 21050211007
### Hamming (15,11) + Convolutional K=4 (g1=octal15, g2=octal17)

### Kişisel 96-bit mesaj: ECC2026-S09I (12 karakter, 8-bit ASCII)
### # Karakter | ASCII | 8-Bitlik Gösterim
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

MESSAGE= "ECC2026-S09I"   ### hocanın verdiği mesaj
SEED_DEGERLERI   = [12013, 17317, 24847] ### hocanın verdiği seed değerleri 
BERS_DEGERLERI   = [0.001, 0.01, 0.05, 0.10, 0.15]  ### hocanın verdiği ber değerleri

def str_to_bits(s):
    bits = []
    for harf in s:  ### mesajdaki karakterleri sırasıyla aldık
        for bit in format(ord(harf), '08b'):  ### ord() karakteri ASCII sayısına çeviriyor.
            bits.append(int(bit))             ### format() 8 bitlik binary string yapıyor.baştaki sıfır eksik bitlere 0 koyar. for döngüsü ise her karakteri tek tek alır.
    return np.array(bits, dtype=int)          ### append() ile stringten sayıya çeviriyoruz.ve listeye ekliyoruz.en sonda diziyi numpy dizisi yapıyoruz.



######################################
### Padding fonksiyonu

def pad_to_multiple(bits, block_size):
    
    ### 96 biti 11e bölünce 8 bit arttı. 96-88=8
    ### o yüzden 3 sıfır ekleyip 99 bite tamamlıyoruz.çünkü messaj bit sayimiz 11
    rem = len(bits) % block_size

    ### zaten tam bölünüyorsa dokunma
    if rem == 0:
        return bits, 0

    ### kaç sıfır ekleyeceğimizi hesaplıyoruz
    pad_len = block_size - rem

    ### np.zeros(pad_len) ile 3 tane sıfırdan oluşan dizi oluşturuyoruz
    ### np.concatenate ile 96 bitlik mesaj dizisinin sonuna bu sıfırları ekliyoruz
    return np.concatenate([bits, np.zeros(pad_len, dtype=int)]), pad_len 


######################################
### 1. Sadece Hamming

def run_hamming_only(message_bits, ber, seed):

    ### 96 biti 11 bitlik bloklara bölüyoruz, 9 blok elde ediyoruz
    padded, pad_len = pad_to_multiple(message_bits, 11)
    n_blocks = len(padded) // 11

    errors_before = 0  ### kanaldan geçmeden önce kaç bit bozuldu sayacağız
    decoded_bits = []  ### decode ettiğimiz bitleri bu diziye atıcaz

    for i in range(n_blocks):

        block = padded[11*i : 11*(i+1)] ### 11 bitlik bloğu alıyoruz

        codeword = hamming_encode(block, G_ASSIGNED)  ### Hamming encode işlemi 11 bitten 15e çıkardık.

        ### BSC kanalından geçiriyoruz
        noisy = bsc_channel(codeword, ber, seed + i)  ### seed değerini değiştiriyoruz.her blok farklı hata patterni alsın diye
        errors_before += int(np.sum(noisy != codeword))  ### farklı olan bitleri aldık.kaç bit bozuldu sayıyoruz

        decoded = hamming_decode(noisy, H_ASSIGNED)  ### H_ASSIGNED ile decode ediyoruz, 15 bit → 11 bit
        decoded_bits.extend(decoded)     ### extend() tek düz liste için

    decoded_bits = np.array(decoded_bits, dtype=int)

    if pad_len > 0:
        decoded_bits = decoded_bits[:-pad_len]  ### padding eklediğimiz 3 sıfırı çıkarıyoruz

    errors_after = int(np.sum(decoded_bits != message_bits))  ### decoded_bits != message_bits farklı olan bitleri buluyor True/False dizisi döndürüyor
    perfect = np.array_equal(decoded_bits, message_bits)
    return errors_before, errors_after, perfect



######################################
### 2. Sadece convolutional

def run_conv_only(message_bits, ber, seed):

    encoded = conv_encode(message_bits) ### 96 biti encode ediyoruz
                                        ### conv_encode içinde 3 terminasyon biti ekledik.99 bit
                                        ### bit rate 1/2 olduğu için output 99*2 = 198 bit

    ### BSC kanalından geçiriyoruz
    noisy = bsc_channel(encoded, ber, seed)
    errors_before = int(np.sum(noisy != encoded)) ### noisy != encoded farklı olan bitleri buluyor, np.sum sayıyor

    ### Viterbi decode: 198 bit → 99 bit çıkıyor (96 mesaj + 3 terminasyon)
    decoded = viterbi_decode(noisy)

    ### son 3 terminasyon bitini atıyoruz, sadece 96 mesaj bitini alıyoruz
    decoded = decoded[:len(message_bits)]

    ### decoded_bits != message_bits farklı olan bitleri buluyor True/False dizisi döndürüyor
    ### np.sum True'ları 1 False'ları 0 sayıyor, böylece hata sayısını buluyoruz
    errors_after = int(np.sum(decoded != message_bits))
    perfect = np.array_equal(decoded, message_bits)
    return errors_before, errors_after, perfect


######################################
### 3. Concatenation hamming+conv
### önce Hamming encode, sonra Convolutional encode
### decode ederken önce Viterbi sonra Hamming

def run_concatenated(message_bits, ber, seed):

    ### Hamming encode
    ### 96 biti 9 tane 11 bitlik bloğa bölüyoruz
    padded, pad_len = pad_to_multiple(message_bits, 11)
    n_blocks = len(padded) // 11

    hamming_codewords = []
    for i in range(n_blocks):
        blok = padded[11*i : 11*(i+1)]          ### 11 bitlik bloğu aldık
        hamming_codewords.extend(hamming_encode(blok, G_ASSIGNED))  ### 11 bit → 15 bit
    hamming_codewords = np.array(hamming_codewords, dtype=int)
    ### 9 blok x 15 bit = 135 bit oldu

    ### Conv encode
    ### 135 bit + 3 terminasyon = 138 bit → rate 1/2 → 276 bit
    conv_encoded = conv_encode(hamming_codewords)

    ### BSC kanalo
    noisy = bsc_channel(conv_encoded, ber, seed)
    errors_before = int(np.sum(noisy != conv_encoded))

    ### Viterbi decode: 276 bit → 138 bit çıkıyor (135 hamming + 3 terminasyon)
    hamming_received = viterbi_decode(noisy)

    ### son 3 terminasyon bitini atıyoruz, sadece 135 hamming bitini alıyoruz
    hamming_received = hamming_received[:len(hamming_codewords)]

    ### Hamming decode
    ### 135 biti 9 tane 15 bitlik bloğa bölüyoruz → her blok 11 bite döner
    decoded_bits = []
    for i in range(n_blocks):
        blok = hamming_received[15*i : 15*(i+1)]
        decoded_bits.extend(hamming_decode(blok, H_ASSIGNED))  ### H_ASSIGNED ile decode ediyoruz, 15 bit → 11 bit
    decoded_bits = np.array(decoded_bits, dtype=int)

    ### başta eklediğimiz 3 sıfırı çıkarıyoruz, tekrar 96 bite dönüyoruz
    if pad_len > 0:
        decoded_bits = decoded_bits[:-pad_len]

    errors_after = int(np.sum(decoded_bits != message_bits))
    perfect = np.array_equal(decoded_bits, message_bits)
    return errors_before, errors_after, perfect

######################################
### ANA PROGRAM

if __name__ == "__main__":

    ### mesajı bit dizisine çeviriyoruz
    message_bits = str_to_bits(MESSAGE)

    ### 3 yontem, 5 BER, 3 seed = 45 deney
    yontemler = [
        ("Hamming Only",  run_hamming_only),
        ("Conv Only",     run_conv_only),
        ("Concatenated",  run_concatenated),
    ]

    ### sonuçları yazdırıyoruz
    print(f"{'Yontem':<18} {'BER':>6} {'Seed':>7} {'Hata_Once':>10} {'Hata_Sonra':>11} {'Perfect':>8}")
    print("-" * 65)

    for yontem_adi, fonksiyon in yontemler:
        for ber in BERS_DEGERLERI:
            for seed in SEED_DEGERLERI:

                ### her kombinasyon için deneyi çalıştırıyoruz
                hata_once, hata_sonra, perfect = fonksiyon(message_bits, ber, seed)

                print(f"{yontem_adi:<18} {ber:>6.3f} {seed:>7d} {hata_once:>10d} {hata_sonra:>11d} {str(perfect):>8}")

        print()  ### yontemler arası boşluk