const buttons = document.querySelectorAll('.btn');
const senhaInput = document.getElementById('pass');
const delete_btn = document.querySelector('.delete');

let passwordChars = [];

// Atualizar o campo de senha com asteriscos sempre que o valor mudar
senhaInput.addEventListener('input', () => {
    senhaInput.setAttribute('value', senhaInput.value.replace(/./g, "*"));
});

buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Extrai apenas os números do texto do botão
        const numbers = btn.innerText.match(/\d+/g);

        // Se houver números, adiciona-os à lista de caracteres
        if (numbers) {
            passwordChars.push(numbers.join(''));  // Adiciona o número ao final da lista
            senhaInput.value = passwordChars.join('');  // Atualiza o campo de senha com os números
            senhaInput.dispatchEvent(new Event('input'));  // Dispara o evento de 'input' para atualizar os asteriscos
        }
    });
});

delete_btn.addEventListener('click', () => {
    if (passwordChars.length > 0) {
        // Remove o último número inserido
        passwordChars.pop();
        // Atualiza o campo de senha sem os números reais, substituindo por asteriscos
        senhaInput.value = passwordChars.join('');
        senhaInput.dispatchEvent(new Event('input'));
    }
});
