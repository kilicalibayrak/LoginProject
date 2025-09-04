document.addEventListener('DOMContentLoaded' , function() {
    const girisButonu = document.getElementById('loginBtn');
    girisButonu.addEventListener('click', async function() {
        // 🔹 Önce buton animasyonu çalışsın
        girisButonu.classList.add("shrink");
        // 2 saniye sonra eski haline dönsün
        setTimeout(() => {
            girisButonu.classList.remove("shrink");
        }, 700);

        //username ve passwordu alma fonksiyonu:
        const {username,password} = getInputValues();

        //username ve passwordu kontrol etme fonksiyonu:
        if(!validateInputs(username, password)) {
            showError({error:'Kullanıcı Adı veya Şifre Giriniz.'});
            return;
        }
        
        try {
            //response ve datayı alma
            const {response, data} = await sendLoginRequest(username, password);
            
            const responseAgent=await fetch('http://127.0.0.1:8000/api/agent/');
            const dataAgent = await responseAgent.json();
            if(dataAgent && dataAgent.agent_id) {
                localStorage.setItem("agent_id", dataAgent.agent_id);
            }
            if(dataAgent && dataAgent.name) {
                localStorage.setItem("name" , dataAgent.name);
            }

            //response ve data alınırsa datayı işleme:
            processLoginResult(response, data);
        }
        catch (error){
            //backende bağlanılamıyor.
            showError({error:'API Hatası...'});
        }
    });
});

//username ve password inputlarını al
function getInputValues() {
    return {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };
}

//username ve password boş mu?
function validateInputs(username, password) {
    return username.trim() && password.trim();
}

//response ve datayı alma
//not: turkcelle yollayacağımız body formatını kontrol et.
async function sendLoginRequest(username,password) {

    const url = 'http://127.0.0.1:8000/api/login/';
    const headers={'Content-Type':'application/json'};
    const body = JSON.stringify( {username: username, password: password});
    const payload= {
        method:'POST',
        headers: headers,
        body: body
    };
    const response= await fetch(url,payload);
    const data = await response.json(); 

    return {response,data};
}

//response ve datayı kontrol edip işleme:
function processLoginResult(response, data) {
    if(response.ok) {
        showMessage(data);
        storeTokens(data);
        redirectToChat();

    }
    else {
        showError(data);
    }
}

//tokenları kaydetme:
function storeTokens(data) {
    console.log(data.agent_id)
    if(data.data && data.data.access_token) {
        localStorage.setItem('access_token', data.data.access_token);
    }
    if(data.data && data.data.refresh_token) {
        localStorage.setItem('refresh_token', data.data.refresh_token);
    }
}

//chat.html sayfasına yönlendirme
function redirectToChat() {
    window.location.href= '/frontend/chat/chat.html';
}

//backendten gelen bütün hata mesajları
//kullanıcı adı ve şifre hata mesajı
//backende bağlanılmazsa hata mesajı
function showError(data) {
    const errorMessage = document.getElementById('errorMessage');
    if(errorMessage) {
        errorMessage.textContent = data.error || 'Bilinmeyen bir hata oluştu.';  
        errorMessage.style.display= 'block';
        setTimeout(() => {
            errorMessage.textContent = "";
            errorMessage.style.display = "none";
        }, 2200);
    }
}
//backendten gelen başarılı giriş mesajı
function showMessage(data) {
    const trueMessage = document.getElementById('trueMessage');
    if(trueMessage) {
        trueMessage.textContent= data.message || 'Giriş Başarılı';
        trueMessage.style.display= 'block';
        setTimeout(() => {
            trueMessage.textContent = "";
            trueMessage.style.display = "none";
        }, 2200);
    }
}
