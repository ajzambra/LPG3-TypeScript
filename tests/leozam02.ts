//Pequeña prueba de TypeScript
 let edad: number = 25;
 let edades: number[] = [21, 30, 25];

let suma: number = 0;


//ALGORITMO PRINICIPAL
function promedioNotas(notas: number[]): number {
  // for (let a = 0; a < notas.length; a++) {
	//    suma += notas[a];
  //  }
 
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
