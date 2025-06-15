
interface Producto { 
id: number; 
nombre: string; 
cantidad: number; 
precio: number; 
} 
function agregarProducto(inventario: Producto[], nuevo: Producto): 
Producto[] { 
inventario.push(nuevo); 
return inventario; 
} 
function valorTotalInventario(inventario: Producto[]): number { 
let total = 0; 
for (const item of inventario) { 
total += item.cantidad * item.precio; 
} 
return total; 
} 
let inventario: Producto[] = []; 
inventario = agregarProducto(inventario, { id: 1, nombre: "Manzanas", 
cantidad: 10, precio: 0.5 }); 
inventario = agregarProducto(inventario, { id: 2, nombre: "Naranjas", 
cantidad: 5, precio: 0.8 }); 
console.log("Valor total del inventario", valorTotalInventario(inventario));