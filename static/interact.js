let q = document.getElementById("text-box");

// q.addEventListener('submit', (e)=>{
//     // e.preventDefault();
//     let h = document.createElement("div");
//     h.id = "msg";
//     let text = document.getElementById("text").value;
//     console.log(text);
//     h.textContent = text;
//     document.getElementById("message").appendChild(h);
//     document.getElementById("text").value = "";
//     e.preventDefault();
//     // e.stopPropagation;
//     return false;

// });

document.getElementById("btn").addEventListener('submit', (e)=>{
    // let q = document.getElementById("checked")
    let Account = document.getElementById("account")
    let Password = document.getElementById("password")
    let Name = document.getElementById("name")

    // alert(w.value);

    if(Account.value=="" || Password.value==""||Name.value==""){
        alert("帳號、密碼及名字不能空白");
        e.preventDefault();
    }else{
        //pass
    }
}
)

document.getElementById("btn2").addEventListener('submit', (e)=>{
    let Account2 = document.getElementById("account2")
    let Password2 = document.getElementById("password2")

    if(Account2.value=="" || Password2.value==""){
        alert("帳號或密碼不能空白");
        e.preventDefault();
    }else{
        //pass
    }

}
)

// document.getElementById("forms").addEventListener("submit", function(event) {
//     event.preventDefault(); 
//     let number = document.getElementById("count").value;
//     number = Number(number);
//     if(Number.isInteger(number) == false || number<0){
//         alert("請輸入正整數");
//     }else{
//         let square_url = '/square/'+ number;
//         window.location.href = square_url;
//     }
// });


