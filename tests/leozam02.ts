//Pequeña prueba de TypeScript
 let edad: number = 25;
 let edades: number[] = [21, 30, 25];
 let b= true;
 let c= "Hola, TypeScript!";
 let d= 3;



//ALGORITMO PRINICIPAL
function promedioNotas(notas: number[]): number {
  let suma: number = 0;
  for (let a = 0; a < notas.length; a++) {
    suma += notas[a];
  }

  let promedio: number = suma / notas.length;
  return promedio;
}
 
let estudiante = prompt("Ingrese el nombre del estudiante:");
let notas: number[] = [8.5, 9.0, 7.5, 10]; 
let resultado = promedioNotas(notas);
console.log("Las notas del estudiante: ", estudiante);

if (resultado >= 9) {
  console.log("Tiene un promedio excelente");
} else if (resultado >= 7) {
  console.log(" Tiene un buen promedio");
} else {
  console.log(" Necesita mejorar. Promedio ");
}

//Prueba analizador semántico


let age: number = 25;
let nombre: string = "Ana";
let activo: boolean = true;

//Prueba de tipos incorrectos
let prueba1: number = "veinticinco";
let prueba2: string = 77;
let prueba3: boolean = "sí";

let sum: number = 5 + 7;
let saludo: string = "Hola " + "Mundo";
let concatenado: string = "Resultado: " + 10;

//Pruebas de errores de operaciones entre tipos
let suma: number = 5 + true;
let x1: boolean = true + "no";
let suma2: number = 5 + "10"; 

//Prueba variables no declaradas
let x2: number = y + 3;
let nombre2: string = persona;
