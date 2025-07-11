import tkinter as tk
from tkinter import scrolledtext

import lexer
import parser


def ejecutar_codigo():
    codigo = editor.get("1.0", tk.END)
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, "📤 Ejecutando análisis...\n\n")

    try:
        lexer_output = lexer.run_lexer_string(codigo)
        resultado.insert(tk.END, "🧠 Análisis Léxico:\n" + lexer_output + "\n")

        parser_output = parser.run_parser_string(codigo)
        resultado.insert(tk.END, parser_output)
    except Exception as e:
        resultado.insert(tk.END, f"❌ Error en el análisis: {str(e)}\n")


# def ejecutar_codigo():
#     codigo = editor.get("1.0", tk.END)
#     resultado.delete("1.0", tk.END)
#     resultado.insert(tk.END, "Ejecutando análisis...\n")
#     resultado.insert(tk.END, ">> Resultado simulado del análisis...\n")

def limpiar_consola():
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, bienvenida_texto)  # Vuelve a mostrar el mensaje de bienvenida

# Texto de bienvenida personalizado
bienvenida_texto = (
    "Bienvenido al analizador de Typescript\n"
    "Donde puedes aprender acerca de analizador lexico, sintactico y semántico !\n"
    "Solo clickea el Run button para porbar nuestro analizador.\n\n"
)

# Ventana principal
ventana = tk.Tk() 
ventana.title("Analizador TypeScript - GRUPO 3 ")
ventana.geometry("1100x600")
ventana.configure(bg="gray")

# Frame principal
frame = tk.Frame(ventana)
frame.pack(fill=tk.BOTH, expand=True)

# Editor de código
editor_frame = tk.Frame(frame)
editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

etiqueta_editor = tk.Label(editor_frame, text="Editor de Código", bg="black", fg="white", font=("Arial", 12, "bold"))
etiqueta_editor.pack(fill=tk.X)

editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, font=("Courier", 12), bg="#1e1e1e", fg="white", insertbackground='white')
editor.pack(fill=tk.BOTH, expand=True)

boton_ejecutar = tk.Button(editor_frame, text="▶ Ejecutar", font=("Arial", 14, "bold"), width=12, height=2, command=ejecutar_codigo)
boton_ejecutar.pack(pady=10)

# Consola de resultados
resultado_frame = tk.Frame(frame, bg="gray")
resultado_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

etiqueta_resultado = tk.Label(resultado_frame, text="Resultado", bg="gray", fg="white", font=("Arial", 16, "bold"))
etiqueta_resultado.pack(pady=5)

resultado = scrolledtext.ScrolledText(resultado_frame, wrap=tk.WORD, font=("Courier", 12), bg="black", fg="lime", height=25)
resultado.pack(fill=tk.BOTH, expand=True)
resultado.insert(tk.END, bienvenida_texto)  # Mostrar mensaje inicial

boton_limpiar = tk.Button(resultado_frame, text="Limpiar", font=("Arial", 12), width=12, height=2, command=limpiar_consola)
boton_limpiar.pack(pady=10)

ventana.mainloop()
