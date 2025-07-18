# 🔍 Analizador Léxico TypeScript GRUPO 3

Este proyecto implementa un **analizador léxico** para el lenguaje **TypeScript**, utilizando **Python** y la librería **PLY (Python Lex-Yacc)**.

El sistema permite identificar tokens válidos (palabras clave, operadores, tipos, identificadores, literales, etc.) y reportar errores léxicos en el programa.


## 📁 Estructura del Proyecto
```text
├── lexer/                     <- Contiene el archivo principal del analizador léxico (lexer.py)
│   └── lexer.py               <- Define los tokens, reglas léxicas y la función run_lexer()
│   └── parser.py              <- Verificará que las expresiones y estructuras del código en TypeScript
│                                  sigan las reglas gramaticales del lenguaje. run_parser()
│
├── run_lexer.py              <- Script principal que ejecuta el analizador léxico desde consola.
│                                Recibe un archivo .ts y un nombre de usuario como argumento.
├── run_parser.py              <- Script principal que ejecuta el analizador sintactico desde consola.
│                                Recibe un archivo .ts y un nombre de usuario como argumento.
├── prog.py                   <- Archivo para cargar la interfaz gráfica para la prueba de los analizadores.
│                               El usuario escirbe en el editor del código y clickea el botón.
│
├── tests/                    <- Archivos de prueba escritos en TypeScript (.ts)
│   ├── leozam02.ts         <- Algoritmo de Leonardo Zambrano
│   ├── ajzambra.ts         <- Algoritmo de Andrés Zambrano
│   └── roberB1.ts         <- Algoritmo de Roberto Barrios
│
├── README.md                 <- Instrucciones generales del proyecto y cómo ejecutarlo.
```

## ▶️ ¿Cómo ejecutar el lexer?
Coloca tu archivo .ts de prueba en la carpeta tests/.

Ejecuta el siguiente comando desde la raíz del proyecto:

python run_lexer.py tests/archivo.ts usuarioGit

## ▶️ ¿Cómo ejecutar el parser?
Coloca tu archivo .ts de prueba en la carpeta tests/.

Ejecuta el siguiente comando desde la raíz del proyecto:

python run_parser.py tests/archivo.ts usuarioGit

📌 Cambia:
archivo.ts por el nombre del archivo que quieres analizar.
usuarioGit por tu nombre o nombre de usuario de GitHub.

## Librerías de Python necesarias

Para ejecutar este proyecto, asegúrate de tener instaladas las siguientes bibliotecas:

- [`ply`](https://pypi.org/project/ply/): para el análisis léxico y sintáctico.
- `tkinter`: incluida por defecto en la mayoría de instalaciones de Python.

## 👥 Integrantes


- **Leonardo Zambrano**: Se encargó de definir tokens para los tipos primitivos (`number`, `string`, `boolean`), operadores aritméticos (`+`, `-`, `*`, `/`, `%`, `**`), manejo de arreglos (`[]`), cadenas de texto (`"..."`, `'...'`) y números flotantes (`FLOAT`).

- **Andrés Zambrano**: Implementó los tokens para operadores de asignación y comparación (`=`, `+=`, `==`, `===`, `!=`, `!==`, `>=`, etc.), estructuras de control (`if`, `else`, `for`, `while`, `switch`, `return`), y definiciones de funciones (`function`, `const`, `class`).

- **Roberto Barrios**: Desarrolló el reconocimiento de operadores lógicos (`&&`, `||`, `!`), delimitadores y signos de puntuación (`{}`, `()`, `,`, `;`, `.`), funciones flecha (`=>`), y los tipos de comentario (`//`, `/* ... */`).


