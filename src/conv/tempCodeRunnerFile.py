import numpy as np

def conv_encode(giris_mesaji):
    """
    Rate 1/2 Convolutional Encoder
    
    Sistem modeli:
        Current State = (m0, m1)
        Input Bit     = m2
        Next State    = (m1, m2)

    Çıkış formülleri:
        x1 = m0 ^ m1 ^ m2
        x2 = m0 ^ m2
    """

    
    # Encoderibn başlangıç durumu
    # Shift register ilk başta 00 (a) durumunda başlar.
    
    m0 = 0
    m1 = 0

    # Şifrelenmiş bitleri burada tutacağız
    encoded_bits = []


    # Mesaj bitlerini sırayla sisteme gönderiyoruzz
    # Her gelen bit burada m2 değeri yerine kullanılır.
    for m2 in giris_mesaji:

        ### XOR yaptık.
        x1 = m0 ^ m1 ^ m2
        x2 = m0 ^ m2

        # append kullanırsak bitler kutu içinde hapis kalır ve kod hata verir.
        # extend ile kutuyu açıp bitleri serbest bırakıyoruz, böylece hepsi düz bir sıra oluyor.
        encoded_bits.extend([x1, x2])


        ### Shift Register 
        ### Bir sonraki adım için m1 artık m0 yerine geçer, sisteme yeni giren m2 ise m1 olur.
        m0 = m1
        m1 = m2

    ### Listeyi NumPy array olarak geri döndürüyoruz
    return np.array(encoded_bits)

### Şimdi test edicez
if __name__ == "__main__":

    print("\n--- Convolutional Encoder Testi ---")

    # Sisteme gönderilecek örnek mesaj
    mesaj = np.array([1, 0, 1, 1])

    # Encoding işlemi yaparak şifreli çıktıyı buluyoruz.
    sifreli_cikti = conv_encode(mesaj)


    print("Giriş Mesajı        :", mesaj)
    print("Şifreli Çıkış       :", sifreli_cikti)