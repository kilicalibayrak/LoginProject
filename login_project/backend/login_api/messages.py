#Status Hataları:
HTTP_STATUS_MESSAGES = {
    200: "Giriş Başarılı",

    400: "Hatalı İstek - JSON formatı veya eksik alan",
    401: "Yetkisiz Erişim - Yanlış kullanıcı adı/şifre",
    403: "Erişim Engellendi - Yetkiniz yok",
    404: "API Endpoint Bulunamadı",
    405: "Sadece POST İsteği Kabul Edilir",
    408: "İstek Zaman Aşımı - API yanıt vermedi",
    413: "İstek Çok Büyük",
    415: "JSON Formatı Gerekli",
    419: "Oturum Süresi Doldu",
    422: "İşlenemeyen İstek - Doğrulama hatası",
    429: "Çok Fazla İstek - Rate limit aşıldı",
    
    500: "Yetkisiz Erişim - Yanlış kullanıcı adı/şifre",
    502: "Kötü Ağ Geçidi - API ulaşılamaz",
    503: "Servis Kullanılamıyor - API bakımda",
    504: "Ağ Geçidi Zaman Aşımı - API yanıt vermedi",
}
