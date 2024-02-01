const cookieBox =  
    document.getElementById("cookieBox"); 

const acceptCookie =  
    document.querySelector(".acceptCookie"); 

const rejectCookie =  
    document.querySelector(".rejectCookie");



//подтврерждение удаления записи о тренировке
function confirmDelete(){
    alert("Подтвредите удаление");
};


//куки хранятся 30 дней, если их принять
acceptCookie.onclick = () => { 
    document.cookie = "CookieBy=MyCookie; max-age="
        + 60 * 60 * 24 * 30; 
    if (document.cookie) { 
        cookieBox.classList.add("hide"); 
    }
}; 

//непринятие куки
rejectCookie.onclick = () => { 
    alert("Вы не принли куки, поэтому ваши данные не будут сохранены"); 
    cookieBox.classList.add("hide"); 
}; 

//проверка сохраненных куки для сайта
let checkCookie = document.cookie.indexOf("CookieBy=MyCookie");

//если есть уже куки, то не показываем уведомление, если нет - то снова показываем
checkCookie !== -1 ? cookieBox.classList.add("hide") : cookieBox.classList.remove("hide");

//проверка чекбокса
function checkIt() {
    document.getElementById("check").required = true;
}

