# Resmi Gazete Kullanarak RAG Geliştirme Projesi

## **a- Projenin Amacı Nedir?**
Projenin amacı, Resmi Gazete’de yayınlanan yasal düzenlemeler, kararlar ve diğer resmi duyurulara hızlı ve doğru erişim sağlamaktır. 
- Resmi Gazete içerikleri genellikle karmaşık bir yapıya sahiptir ve arama yapmak zaman alabilir. Bu nedenle, kullanıcıların sordukları sorulara anlamlı ve alakalı yanıtlar alabilecekleri bir sistem geliştirmek hedeflenmektedir.
- Örnek kullanım: "İstanbul Teknik Üniversitesi için yeni açılan kontenjanlar nelerdir?" gibi sorulara spesifik yanıtlar sunulması.


## **b- Veriyi Nasıl İşleyeceksiniz?**

### 1. **Veri Toplama**
- Resmi Gazete'nin web sitesinden web scraping yöntemleriyle günlük olarak veri çekilecek.
- PDF formatında yayınlanan belgeler metin formatına dönüştürülecek.

### 2. **Metin İşleme**
- Belgeler OCR teknolojisi ile okunabilir metne dönüştürülecek.
- NLP araçları kullanılarak içerik segmentlere ayrılacak (başlık, madde).
- Tarih, karar numarası, konu başlığı gibi anahtar bilgiler etiketlenecek.

### 3. **Dizinleme**
- Veriler, vektör tabanlı bir veritabanına (örneğin Pinecone) indekslenecek.
- İçeriğin semantik anlamını yakalamak için bir embedding modeli kullanılacak.


## **c- LLM ve Retrieval Bileşenleri Nasıl Entegre Olacak?**

### 1. **Retrieval**
- Kullanıcıdan gelen sorgu embedding modeli ile vektör formatına dönüştürülecek.
- Vektör tabanlı veritabanından en alakalı içerik parçaları getirilerek yanıt oluşturma sürecine aktarılacak.

### 2. **LLM**
- Getirilen içerikler, LLM tarafından özetlenerek ve işlenerek yanıt oluşturulacak.
- Sorguya özel bağlamlı yanıtlar sağlanacak.

#### **Süreç Akışı**
1. Sorgu
2. Vektör Arama (Retriever) 
3. İlgili İçeriklerin Çıkarılması
4. LLM ile Yanıt Oluşturma.


## **d- Bu Proje Hangi Sorunu Çözmeyi Hedefliyor?**

### 1. **Zaman Kaybını Azaltma**
- Resmi Gazete’de belirli bir bilgiye ulaşmak isteyen kullanıcılar, sayfalarca belgeyi manuel olarak incelemek zorunda kalıyor. Bu sistem ile gerçekleştirilecek işlem birkaç saniyeye düşecek.

### 2. **Anlamayı Kolaylaştırma**
- Resmi Gazete dili genellikle karmaşık ve teknik bir yapıya sahip. Bu sistem, bu dili daha anlaşılır bir şekilde özetleyecek.

### 3. **Kapsamlı Arama**
- Kullanıcılar yalnızca belirli anahtar kelimelere değil, içerik anlamına dayalı olarak arama yapabilecek.

### 4. **Güncel**
- Resmi Gazete her gün güncellendiği için sistem de dinamik bir şekilde yeni içeriklerle güncellenecek.