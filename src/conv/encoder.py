import numpy as np

def conv_encode(giris_mesaji):
    """
    Rate 1/2 Convolutional Encoder
    
    Sistem modeli:
        K = 4, (k-1)memory = 3, 8 durum
        g1 = D^3 + D^2 + 1       (octal 15, binary 1101)
        g2 = D^3 + D^2 + D + 1   (octal 17, binary 1111)

    Shift Register: [m0, m1, m2] (en eski solda)
    Input Bit: m3

    Çıkış formülleri:
        x1 = m3 ^ m2 ^ m0        (g1: 1101)
        x2 = m3 ^ m2 ^ m1 ^ m0  (g2: 1111)

    Next State: m0=m1, m1=m2, m2=m3
    """

 ### Shift register başlangıç durumu
    ### K=4 olduğu için 3 register var, hepsi 0
    m0 = 0
    m1 = 0
    m2 = 0

    ### Şifrelenmiş bitleri tutmak için bir dizi oluşturduk
    encoded_bits = []

    ### K-1 = 3 adet sıfır bit ekliyoruz terminasyon işlemi yani mesajımız [1, 0, 1, 1, 0, 0, 0] bu oluyor ###
    ### çıkış bit sayısı da (mesaj biti(4)+terminasyondaki (3)bit)*2



    ### "feed K-1 trailing zero bits so encoder returns to zero state" bubnu hocanın verdiği parametre dosyasında diyor
    giris_mesaji = list(giris_mesaji) + [0, 0, 0]

    ### mesaj bitlerini sırayla sisteme gönderdik
    ### her gelen bit burada m3 değeri yerine kullanılır
    for m3 in giris_mesaji:

        ### g1 ve g2 polinomlarına göre XOR yaptık.
        x1 = m3 ^ m2 ^ m0          ### g1 = 1101: D^3, D^2, D^0 konumları
        x2 = m3 ^ m2 ^ m1 ^ m0    ### g2 = 1111: D^3, D^2, D^1, D^0 konumları

        ### append kullanırsak bitler kutu içinde hapis kalır ve kod hata verir.
        ### extend ile kutuyu açıp bitleri serbest bırakıyoruz, böylece hepsi düz bir sıra oluyor.
        encoded_bits.extend([x1, x2])

        ### Shift Register güncelleme
        ### Bir sonraki adım için registerlar sola kayar, yeni bit en sağa girer.
        m0 = m1
        m1 = m2
        m2 = m3

    ### Listeyi NumPy array olarak geri döndürüyoruz
    return np.array(encoded_bits)


### Şimdi test edicez
if __name__ == "__main__":

    print("\n--- Convolutional Encoder Testi ---")

    ### Sisteme gönderilecek örnek mesaj
    mesaj = np.array([1, 0, 1, 1])

    ### Encoding işlemi yaparak şifreli çıktıyı buluyoruz.
    sifreli_cikti = conv_encode(mesaj)

    print("Giriş Mesajı:", mesaj)
    print("Şifreli Çıkış:", sifreli_cikti)
    print("Output bit sayısı:", len(sifreli_cikti))




    ### parametreleri hocanın verdiği parametrelerle değiştirdim.