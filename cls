[33mcommit a22b64a170fdeb975e9fecdef2cc94b3f4828e76[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmaster[m[33m)[m
Author: burakykkk <burakyasarkaya.eee@gmail.com>
Date:   Mon May 25 22:52:10 2026 +0300

    Commit 6: Test sonrası klasör gereksiz pycache dosyalarıyla doldu. Reponun çöplüğe dönmemesi ve sadece kendi yazdığım kodların kalması için .gitignore oluşturup arka plan dosyalarını temizledim.

[33mcommit 01c1cf95d42194832651f32edcb039705ce5672d[m
Author: burakykkk <burakyasarkaya.eee@gmail.com>
Date:   Mon May 25 22:41:05 2026 +0300

    Commit 5: Projenin ana modülleri (Encoder, BSC, Decoder) main.py dosyasında birleştirildi. Orijinal mesaj şifrelenip kanala sokuldu ve decoder'ın oluşan gürültüyü başarıyla düzelttiği uçtan uca test edildi.

[33mcommit 379e90fb0f9ea09892f2b90bc66a6f1d0359a528[m
Author: burakykkk <burakyasarkaya.eee@gmail.com>
Date:   Mon May 25 22:32:19 2026 +0300

    Commit 4: Sistemibbn alıcı kısmı için decoder.py eklendi. Gelen bozuk mesajın sendromunbu H matrisiyle bulup düzeltebn algoritmayı kurdumm..

[33mcommit 8cc9e78670c6bc3a9814c70ab97115f3c965cc45[m
Author: burakykkk <burakyasarkaya.eee@gmail.com>
Date:   Mon May 25 19:42:32 2026 +0300

    Commit 3: src/hamming altında encoder.py dosyası oluşturuldu. Test bloğuna çıktının nasıl hesaplandığını unutmamak için adım adım matris çarpımı el çözümü eklendi.

[33mcommit ee77e3e64dc956009adb23ff3fb8dedc57f10a52[m
Author: burakykkk <burakyasarkaya.eee@gmail.com>
Date:   Mon May 25 19:07:45 2026 +0300

    Commit 2: Projedeki gürültülü kanal adımı için BSC simülatörü oluşturuldu. Kodun her çalışmasında aynı hatalı bitleri verip test aşamasını kolaylaştırması için seed ayarlandı ve BER tabanlı XOR hata maskelemesi koda döküldü.

[33mcommit f1ca8420c136599a12ba0624e4853426ec502726[m
Author: burakykkk <burakyasarkaya.eee@gmail.com>
Date:   Mon May 25 18:35:01 2026 +0300

    Commit 1: Proje mimarisi oluşturuldu. İleride yazılacak kanal simülatörü ve Hamming kodlarının düzenli durması için ana klasör yapısı ayarlandı ve README eklendi.
