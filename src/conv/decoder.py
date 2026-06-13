import numpy as np

### TRELLIS(OLASILIK GEÇİŞ TABLOSU) 
def get_trellis():
    """
    =============================================================================================================
    | m0 | m1 | m2 | m  | c1 | c2 | Current State (m0,m1,m2) | Next State (m1,m2,m) |
    -------------------------------------------------------------------------------------------------------------
    | 0  | 0  | 0  | 0  | 0  | 0  |          000              |         000          |
    | 0  | 0  | 0  | 1  | 1  | 1  |          000              |         001          |
    -------------------------------------------------------------------------------------------------------------
    | 0  | 0  | 1  | 0  | 0  | 1  |          001              |         010          |
    | 0  | 0  | 1  | 1  | 1  | 0  |          001              |         011          |
    -------------------------------------------------------------------------------------------------------------
    | 0  | 1  | 0  | 0  | 1  | 1  |          010              |         100          |
    | 0  | 1  | 0  | 1  | 0  | 0  |          010              |         101          |
    -------------------------------------------------------------------------------------------------------------
    | 0  | 1  | 1  | 0  | 1  | 0  |          011              |         110          |
    | 0  | 1  | 1  | 1  | 0  | 1  |          011              |         111          |
    -------------------------------------------------------------------------------------------------------------
    | 1  | 0  | 0  | 0  | 1  | 1  |          100              |         000          |
    | 1  | 0  | 0  | 1  | 0  | 0  |          100              |         001          |
    -------------------------------------------------------------------------------------------------------------
    | 1  | 0  | 1  | 0  | 1  | 0  |          101              |         010          |
    | 1  | 0  | 1  | 1  | 0  | 1  |          101              |         011          |
    -------------------------------------------------------------------------------------------------------------
    | 1  | 1  | 0  | 0  | 0  | 0  |          110              |         100          | 
    | 1  | 1  | 0  | 1  | 1  | 1  |          110              |         101          |
    -------------------------------------------------------------------------------------------------------------
    | 1  | 1  | 1  | 0  | 0  | 1  |          111              |         110          |
    | 1  | 1  | 1  | 1  | 1  | 0  |          111              |         111          |
    =============================================================================================================

    1. AŞAMA: Olasılık Haritasını (Trellis) Çıkarma
    - Current State = (m0, m1, m2)
    - Input = m
    - Next State = (m1, m2, m)
    - c1 = m ^ m1 ^ m0       (g1 = 1101)
    - c2 = m ^ m2 ^ m1 ^ m0  (g2 = 1111)
    """

    # Trellis bilgilerini tutacak sözlük 
    trellis = {}  ### dict{}

    ### K=4 olduğu için toplam 2^(K-1) = 8 adet state vardır:
    ### 000, 001, 010, 011, 100, 101, 110, 111
    for state in range(8):

        ### Her state için ayrı bir area açıyoruz
        trellis[state] = {}

        m0 = (state >> 2) & 1   ### en eski bit
        m1 = (state >> 1) & 1
        m2 = state & 1           ### en yeni bit
        ### >> demek sağa kaydırma işlemi, & ise en sondaki biti al demek.

        # Sisteme gelebilecek yeni input biti:
        # m = 0 veya 1 olabilir
        for m in [0, 1]:

            # c1 = m XOR m2 XOR m0  (g1 = 1101)
            c1 = m ^ m1 ^ m0

            # c2 = m XOR m2 XOR m1 XOR m0  (g2 = 1111)
            c2 = m ^ m2 ^ m1 ^ m0

            # NEXT STATE hesaplama, encoder'daki shift ile aynı: m0=m1, m1=m2, m2=m
            next_state = (m1 << 2) | (m2 << 1) | m

            ### TRELLIS Tablosuna kaydetme işlemi
            trellis[state][m] = {

                # Geçilecek yeni state
                'next_state': next_state,

                # Üretilen çıktı bitleri
                'output': (c1, c2)
            }

    # Oluşturulan trellis yapısını geri döndür
    return trellis


#####################################
# VITERBI DECODER
#####################################
def viterbi_decode(received_bits):

    """
    2. ve 3. AŞAMA

    2. AŞAMA:
    - Branch Metric hesaplama
    - Path Metric hesaplama
    - ACS (Add Compare Select)

    3. AŞAMA:
    - Traceback (Geriye iz sürme)
    """

    # Toplam state sayısı: K=4 için 2^(K-1) = 8
    num_states = 8

    # Trellis yapısını oluştur
    trellis = get_trellis()


    ### PATH METRIC BAŞLANGICI
    ### Viterbi'ye başlamadan önce hazırlık yapıyoruz.
    ### path_metrics her state'in hata sayısını tutar, başta hepsi sonsuz sadece 000 state'i 0
    # Her state için başlangıç maliyeti sonsuz aslında sonsuz demek bu state'e henuz hiç yol yok demek
    
    path_metrics = np.full(num_states, np.inf)

    # Sistem her zaman 000 state'inden başlar
    path_metrics[0] = 0   

    # Traceback için hafıza listesi
    memory = []

    #####################################
    # GELEN VERİYİ 2'ŞER BİT İŞLE
    #####################################

    # Rate 1/2 olduğu için veri 2 bitlik gruplar halinde okunur
    for i in range(0, len(received_bits), 2): ### listeyi ikişer ikişer admlıyoruz

        # Kanaldan gelen iki bit
        r1 = received_bits[i]
        r2 = received_bits[i + 1] ### bu her adımda iki bit okuduğumuz anlamına gelir

        ### Her adımda yeni boş bir tablo açıyoruz.
        ### Çünkü hesaplarken bir önceki adımın değerleri bozmak istemiyoruz
        new_path_metrics = np.full(num_states, np.inf) 

        # O anki adımın hafızası.her adım için ayrı ayrı hafıza tutuyoruz
        step_memory = {}


        ######################################
        # TÜM STATE'LERİ DOLAŞ
        #####################################

        for state in range(num_states):

            # Eğer bu state'e hiç ulaşılmadıysa geç
            if path_metrics[state] == np.inf:
                continue

            # her stateten iki input çıkabilir 0veya 1
            for m in [0, 1]:

                # Trellis geçiş bilgileri
                transition = trellis[state][m] ### trellis fonksiyonu içindeki next state ve output değerlerini aliyoruz

                ### Sonraki state
                next_state = transition['next_state']

                ### Beklenen encoder çıktısı
                ### Encoder bu geçişte ne üretmeliydi, kanaldan gelenle karşılaştıracağız
                expected_out = transition['output']


                #####################################
                ### BRANCH METRIC (HAMMING DISTANCE)

                ### Gelen bit ile beklenen bit farklıysa 1 hata say
                hata_sayisi = (r1 != expected_out[0]) + (r2 != expected_out[1])

                #####################################
                ### PATH METRIC

                # Toplam hata puanı
                new_metric = path_metrics[state] + hata_sayisi


                #####################################
                ### ACS (ADD-COMPARE-SELECT)

                # Eğer yeni yol daha iyiyse:
                if new_metric < new_path_metrics[next_state]:

                    # En düşük maliyetli yolu seçiyoruz.ve kaydediyoruz
                    new_path_metrics[next_state] = new_metric

                    ### Traceback için hangi state'ten geldiğimizi ve hangi input bitiyle geldiğimizi tutuyoruz
                    step_memory[next_state] = (state, m)

        ### tabloyu yeniden yaptık.ve burdan devam edicez
        path_metrics = new_path_metrics

        # Hafızaya ekle
        memory.append(step_memory)


    #####################################
    ### 3. AŞAMA: TRACEBACK
    #####################################

    # Kurtarılan mesaj listesi
    decoded_message = []

    # En düşük maliyetli final state'i seç
    current_state = np.argmin(path_metrics)  ### argmin en küçük değerin indexini döndürür

    # Hafızayı sondan başa doğru oku
    for step in reversed(memory):

        # Önceki state ve input biti
        prev_state, m = step[current_state]

        # Input bitini kaydet
        decoded_message.append(m)

        # Geri git
        current_state = prev_state

    # Liste tersten oluştuğu için düzelt
    decoded_message.reverse()

    # NumPy array olarak döndür
    return np.array(decoded_message)


#####################################
# ANA PROGRAM
#####################################
if __name__ == "__main__":

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.conv.encoder import conv_encode    

    # Örnek mesaj
    mesaj = np.array([1, 0, 1, 1])

    # Encode et
    sifreli = conv_encode(mesaj)

    # Temiz kanalda decode et
    kurtarilan = viterbi_decode(sifreli)

    print("Şifreli Veri:      ", sifreli)
    print("Kurtarılan Mesaj:  ", kurtarilan[:len(mesaj)])
    print("Doğru mu:          ", np.array_equal(mesaj, kurtarilan[:len(mesaj)]))

    ### parametreleri hocanın verdiği parametrelerle değiştirdim.