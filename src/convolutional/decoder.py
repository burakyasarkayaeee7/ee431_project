import numpy as np
# =============================================================================
# TRELLIS(OLASILIK GEÇİŞ TABLOSU 
# ==========================================================================
def get_trellis():
    """
    ========================================================================================================
    | m0 | m1 | m2 | x1 | x2 | Current State (m0,m1) | Next State (m1,m2) |
    --------------------------------------------------------------------------------------------------------
    | 0  | 0  | 0  | 0  | 0  |         00 (a)        |        00 (a)      |
    | 0  | 0  | 1  | 1  | 1  |         00 (a)        |        01 (b)      |
    --------------------------------------------------------------------------------------------------------
    | 0  | 1  | 0  | 1  | 0  |         01 (b)        |        10 (c)      |
    | 0  | 1  | 1  | 0  | 1  |         01 (b)        |        11 (d)      |
    --------------------------------------------------------------------------------------------------------
    | 1  | 0  | 0  | 1  | 1  |         10 (c)        |        00 (a)      |
    | 1  | 0  | 1  | 0  | 0  |         10 (c)        |        01 (b)      |
    --------------------------------------------------------------------------------------------------------
    | 1  | 1  | 0  | 0  | 1  |         11 (d)        |        10 (c)      |
    | 1  | 1  | 1  | 1  | 0  |         11 (d)        |        11 (d)      |
    ========================================================================================================

    1. AŞAMA: Olasılık Haritasını (Trellis) Çıkarma
    - Current State = (m0, m1)
    - Input = m2
    - Next State = (m1, m2)
    - x1 = m0 ^ m1 ^ m2
    - x2 = m0 ^ m2
    """

    # Trellis bilgilerini tutacak sözlük
    trellis = {}

    ### K=Constraint Length ###
    ### K=3 olduğu için toplam 2^(K-1)=4 adet state vardır:
    ### 00, 01, 10, 11
    for state in range(4):

        ### Her state için ayrı bir alan açıyoruz
        trellis[state] = {}

      # State değerini iki bite ayırıyoruz. 
        # Örnek: state = 2 -> binary 10
        # m0 = 1, m1 = 0
        m0 = (state >> 1) & 1  # state'i 1 bit sağa kaydırarak (maskeleyerek) m0 bitini elde ediyoruz.
        m1 = state & 1         # state'in son bitini alarak m1 bitini elde ediyoruz.

        # Sisteme gelebilecek yeni input biti:
        # m2 = 0 veya 1 olabilir
        for m2 in [0, 1]:

            # x1 = m0 XOR m1 XOR m2
            x1 = m0 ^ m1 ^ m2

            # x2 = m0 XOR m2
            x2 = m0 ^ m2

            # NEXT STATE Hesaplamasi

            # Yeni state = (m1,m2)
            # m1 sola kaydırılır, m2 en sağa eklenir
            next_state = (m1 << 1) | m2

            ### TRELLIS Tablosunba kaydetme işlemi

            trellis[state][m2] = {

                # Geçilecek yeni state
                'next_state': next_state,

                # Üretilen çıktı bitleri
                'output': (x1, x2)
            }

    # Oluşturulan trellis yapısını geri döndür
    return trellis


# =============================================================================
# VITERBI DECODER
# =============================================================================
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

    # Toplam state sayısı
    num_states = 4

    # Trellis yapısını oluştur
    trellis = get_trellis()

    # =========================================================
    # PATH METRIC BAŞLANGICI
    # =========================================================

    # Her state için başlangıç maliyeti sonsuz
    path_metrics = np.full(num_states, np.inf)

    # Sistem her zaman 00 state'inden başlar
    path_metrics[0] = 0

    # Traceback için hafıza listesi
    memory = []

    # =========================================================
    # GELEN VERİYİ 2'ŞER BİT İŞLE
    # =========================================================

    # Rate 1/2 olduğu için veri 2 bitlik gruplar halinde okunur
    for i in range(0, len(received_bits), 2):

        # Kanaldan gelen iki bit
        r1 = received_bits[i]
        r2 = received_bits[i + 1]

        # Yeni metric değerleri
        new_path_metrics = np.full(num_states, np.inf)

        # O anki adımın hafızası
        step_memory = {}

        # =========================================================
        # TÜM STATE'LERİ DOLAŞ
        # =========================================================

        for state in range(num_states):

            # Eğer bu state'e hiç ulaşılmadıysa geç
            if path_metrics[state] == np.inf:
                continue

            # O state'ten çıkabilecek input bitleri
            for m2 in [0, 1]:

                # Trellis geçiş bilgileri
                transition = trellis[state][m2]

                # Sonraki state
                next_state = transition['next_state']

                # Beklenen encoder çıktısı
                expected_out = transition['output']

                # =====================================================
                # BRANCH METRIC (HAMMING DISTANCE)
                # =====================================================

                # Gelen bit ile beklenen bit farklıysa 1 hata say
                bm = (r1 != expected_out[0]) + \
                     (r2 != expected_out[1])

                # =====================================================
                # PATH METRIC
                # =====================================================

                # Toplam hata puanı
                new_metric = path_metrics[state] + bm

                # =====================================================
                # ACS (ADD-COMPARE-SELECT)
                # =====================================================

                # Eğer yeni yol daha iyiyse:
                if new_metric < new_path_metrics[next_state]:

                    # En düşük maliyeti kaydet
                    new_path_metrics[next_state] = new_metric

                    # Traceback için:
                    # hangi state'ten geldiğimizi
                    # ve hangi input bitiyle geldiğimizi sakla
                    step_memory[next_state] = (state, m2)

        # Metricleri güncelle
        path_metrics = new_path_metrics

        # Hafızaya ekle
        memory.append(step_memory)

    # =============================================================================
    # 3. AŞAMA: TRACEBACK
    # =============================================================================

    # Kurtarılan mesaj listesi
    decoded_message = []

    # En düşük maliyetli final state'i seç
    current_state = np.argmin(path_metrics)

    # Hafızayı sondan başa doğru oku
    for step in reversed(memory):

        # Önceki state ve input biti
        prev_state, m2 = step[current_state]

        # Input bitini kaydet
        decoded_message.append(m2)

        # Geri git
        current_state = prev_state

    # Liste tersten oluştuğu için düzelt
    decoded_message.reverse()

    # NumPy array olarak döndür
    return np.array(decoded_message)


# =============================================================================
# ANA PROGRAM
# =============================================================================
if __name__ == "__main__":

    # =========================================================
    # ORİJİNAL ŞİFRELİ VERİ
    # =========================================================

    # [1,0,1,1] mesajının encoder çıktısı
    sifreli = np.array([1, 1, 1, 0, 0, 0, 0, 1])

    # =========================================================
    # KANALDA BOZULMUŞ VERİ
    # =========================================================

    # Gürültü nedeniyle bazı bitler değişmiş
    bozuk = np.array([1, 1, 0, 0, 0, 0, 1, 1])

    # =========================================================
    # VITERBI DECODING
    # =========================================================

    # Mesajı kurtar
    kurtarilan = viterbi_decode(bozuk)

    # =========================================================
    # SONUÇLARI YAZDIR
    # =========================================================

    print("Şifreli Veri:      ", sifreli)
    print("Bozuk Kanal Çıkışı:", bozuk)
    print("Kurtarılan Mesaj:  ", kurtarilan)