const buttons = document.querySelectorAll('.btn');
const senhaInput = document.getElementById('pass');
const delete_btn = document.querySelector('.delete');

let passwordChars = [];


senhaInput.addEventListener('input', () => {
    senhaInput.setAttribute('value', senhaInput.value.replace(/./g, "*"));
});

buttons.forEach(btn => {
    btn.addEventListener('click', () => {

        const numbers = btn.innerText.match(/\d+/g);

  
        if (numbers) {
            passwordChars.push(numbers.join(''));  
            senhaInput.value = passwordChars.join('');  
            senhaInput.dispatchEvent(new Event('input')); 
        }
    });
});

delete_btn.addEventListener('click', () => {
    if (passwordChars.length > 0) {
      
        passwordChars.pop();
   
        senhaInput.value = passwordChars.join('');
        senhaInput.dispatchEvent(new Event('input'));
    }
});
