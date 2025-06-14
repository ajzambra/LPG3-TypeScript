function promedioNotas(notas: number[]): number {
  let suma: number = 0;
  for (let i = 0; i < notas.length; i++) {
	suma += notas[i];
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
