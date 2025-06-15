function calcularAreaYPerimetro(dim: [number, number]): void {
    let largo: number = dim[0];
    let ancho: number = dim[1];
    if (largo <= 0 || ancho <= 0) {
      console.log("Dimensiones inválidas");
      return;
    }
    let area: number = largo * ancho;
    let perimetro: number = 2 * (largo + ancho);
    console.log("Área del rectángulo:", area);
    console.log("Perímetro del rectángulo:", perimetro);
  }
  let dimensiones: [number, number] = [10, 5];
  calcularAreaYPerimetro(dimensiones);
  for (let i = 0; i < 3; i++) {
    console.log("Iteración:", i);
  }
  