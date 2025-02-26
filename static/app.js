const buttons = document.querySelectorAll('.btn');
// const textarea = document.querySelector('textarea')
const senhaInput = document.getElementById('pass');
const btnLogin = document.getElementById('btn_login');
const delete_btn = document.querySelector('.delete');


let passwordChars = [];

senhaInput.addEventListener('input', () => {
    // Atualiza o valor do atributo value com asteriscos
    senhaInput.setAttribute('value', senhaInput.value.replace(/./g, "*"));
});


buttons.forEach(btn =>{
    // btn.addEventListener('click', ()=>{
    //     passwordChars.push(btn.innerText);
    //     senhaInput.value = passwordChars.join('');
    //     senhaInput.dispatchEvent(new Event('input'));
    //     console.log(passwordChars)
    //     console.log(senhaInput.value)
    // });
    btn.addEventListener('click', () => {
        // Extrai apenas os números do texto do botão
        const numbers = btn.innerText.match(/\d+/g);
        // Converte a lista de números em string separada por vírgula
        const numberString = numbers.join(',');
        // Adiciona a string de números à lista de caracteres da senha
        passwordChars.push(numberString);
        // Atualiza o valor do campo de senha
        senhaInput.value = passwordChars.join(',');
        // Dispara o evento 'input' para atualizar a validação do campo
        senhaInput.dispatchEvent(new Event('input'));
        console.log(numberString)
        console.log(passwordChars);
        console.log(senhaInput.value);
      });
});


delete_btn.addEventListener('click', () =>{
    if (passwordChars.length > 0){
        passwordChars.pop()
        senhaInput.value = passwordChars.join('');
    }
    
});
