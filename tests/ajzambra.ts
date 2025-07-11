//lexico algoritmo

let contador: number = 10;
contador += 2;
contador -= 1;
contador *= 3;
contador /= 2;
contador %= 4;

let resultado1 = contador == 10;
let resultado2 = contador !== 5;
let resultado3 = contador < 20;
let resultado4 = contador >= 1;

function comparar(a: number, b: number): boolean {
  if (a === b) {
    return true;
  } else {
    return false;
  }
}


//Semantico y Sintantico algoritmo

var edad = 25;                             // varAssignment
var activo: boolean = true;               // varAssignment con tipo

while (true) {             // controlEstructure (WHILE)
    console.log("Mayor de edad");         // Instrucción dentro del bucle
}

const sumar = (a: number, b: number) => {  // arrow_function con tipos y bloque
    return a + b;
};

interface Persona {                       // interface + propiedades
    nombre: string;
}                  
