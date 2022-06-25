const grams = document.querySelector('#grams')
const ounces = document.querySelector('#ounces')


grams.addEventListener('input',()=>{
    
    let val = grams.value / 28.34
    ounces.value = val.toFixed(2)

})
ounces.addEventListener('input',()=>{
    
    let val = ounces.value * 28.34
    grams.value = val.toFixed(2)

})




