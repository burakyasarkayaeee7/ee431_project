import numpy as np

def hamming_decode(received_block, H_matrix):
    ### 1. Parity-Check (H) matrisinin transpozunu alıyoruz.
    ### Proje yönergesinde "Standard libraries for arrays" kullanımı serbest olduğu için,
    ### transpoz işlemini iç içe döngülerle sıfırdan yazmak yerine NumPy kütüphanbenin .T özelliğini kullanıyoruz.
    H_T = H_matrix.T
    
    ### 2. Sendrom Hesaplama: Gelen mesajı H'nin transpozu ile çarpıp Modulo 2 alıyoruz.
    ### Formül: S = r * H^T
    syndrome = np.dot(received_block, H_T) % 2
    
    ### 3. Sendrom kontrolü: Eğer sendrom [0, 0, 0] ise kanalda hata olmamıştır.
    if not np.any(syndrome):
        return received_block
        
    ### 4. Hata Teşhisi: Sendrom, H matrisinin hangi sütununa eşit?
    ### Eşit olduğu sütunun indeksi, bize hangi bitin bozulduğunu söyler.
    error_index = -1
    for i in range(H_matrix.shape[1]):
        if np.array_equal(syndrome, H_matrix[:, i]):
            error_index = i
            break
            
    ### 5. Hata Düzeltme (Tedavi): Bozuk olduğu tespit edilen biti XOR mantığıyla tersine çeviriyoruz.
    corrected_block = received_block.copy()
    if error_index != -1:
        corrected_block[error_index] = (corrected_block[error_index] + 1) % 2
        
    return corrected_block

### --- TEST KISMI ---
if __name__ == "__main__":
    ### Test için uydurma bir H (Parity-Check) matrisi
    test_H = np.array([
        [1, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ])
    
    ### Encoder testinde orijinal mesaj [1 0 1 1] iken, şifrelenmiş hali [1 0 0 1 0 1 1] çıkmıştı.
    ### Diyelim ki kanaldan geçerken 2. bit (indeks 1) gürültüden etkilendi ve 0 yerine 1 oldu:
    bozuk_mesaj = np.array([1, 1, 0, 1, 0, 1, 1])
    
    ### Dekoderi çalıştırıp tedaviyi uyguluyoruz
    duzeltilmis_mesaj = hamming_decode(bozuk_mesaj, test_H)
    
    print("Kanaldan Gelen Bozuk Mesaj: ", bozuk_mesaj)
    print("Dekoderin Düzelttiği Mesaj: ", duzeltilmis_mesaj)
    
    ### --- MATEMATİKSEL SAĞLAMASI ---
    ### Bozuk Mesaj: [1, 1, 0, 1, 0, 1, 1]
    ### H Transpoz ile çarpıldığında Sendrom = [1, 1, 1] çıkar.
    ### H matrisine bakarsak, [1, 1, 1] sütunu 2. sütundur (indeks 1).
    ### Demek ki 2. bit hatalı! Dekoder bu biti bulur ve 1'i tekrar 0 yapar.