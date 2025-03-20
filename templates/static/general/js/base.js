let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();
});

searchBtn.addEventListener("click", ()=>{ 
    sidebar.classList.toggle("open");
    menuBtnChange();
});

function menuBtnChange() {
if(sidebar.classList.contains("open")){
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
}else {
    closeBtn.classList.replace("bx-menu-alt-right","bx-menu");
}
}

// Função para confirmar o logout
function confirmarLogout(event) {
    const confirmation = confirm("Tem certeza de que deseja sair?");
    
    if (!confirmation) {
        event.preventDefault();  // Se o usuário cancelar, previne o redirecionamento
    }
}

// Adicionar o evento ao link de logout
document.addEventListener("DOMContentLoaded", function() {
    const logoutLink = document.getElementById("logout-link");  // ID do link de logout
    if (logoutLink) {
        logoutLink.addEventListener("click", confirmarLogout);  // Adicionar o evento de clique
    }
});
