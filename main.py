import flet as ft
import requests


def main(page: ft.Page):

    
    # FUENTE GLOBAL
    

    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
    }

    page.theme = ft.Theme(
        font_family="Poppins"
    )

    
    # CONFIGURACIÓN GENERAL
    

    page.title = "Métodos Numéricos"
    page.theme_mode = "light"
    page.padding = 0
    page.scroll = "auto"
    page.bgcolor = "#1E1B4B"

    
    # TABLAS
  

    tabla_newton = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("n")),
            ft.DataColumn(ft.Text("x")),
            ft.DataColumn(ft.Text("f(x)")),
            ft.DataColumn(ft.Text("f'(x)"))
        ],
        rows=[]
    )

    tabla_secante = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("n")),
            ft.DataColumn(ft.Text("Xi-1")),
            ft.DataColumn(ft.Text("Xi")),
            ft.DataColumn(ft.Text("Xi+1")),
            ft.DataColumn(ft.Text("Error"))
        ],
        rows=[]
    )


    # FUNCIÓN NEWTON
    

    def calcular_newton(e):

        try:

            tabla_newton.rows.clear()

            url = f"http://{ip_backend.value}/newton_tanque"

            data = {
                "h_inicial": float(h_inicial.value),
                "tolerancia": float(tolerancia.value),
                "max_iter": int(max_iter.value)
            }

            response = requests.post(url, json=data)

            res = response.json()

            iteraciones = res["iteraciones"]

            for item in iteraciones:

                tabla_newton.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(item["n"]))),
                            ft.DataCell(ft.Text(str(item["x"]))),
                            ft.DataCell(ft.Text(str(item["fx"]))),
                            ft.DataCell(ft.Text(str(item["dfx"])))
                        ]
                    )
                )

            ultima = iteraciones[-1]

            texto_resultado.value = f"Raíz Newton: {ultima['x']}"

            page.update()

        except Exception as error:

            texto_resultado.value = f"Error: {error}"

            page.update()

   
    # FUNCIÓN SECANTE
    

    def calcular_secante(e):

        try:

            tabla_secante.rows.clear()

            url = f"http://{ip_backend.value}/secante_poly"

            data = {
                "x0": float(x0.value),
                "x1": float(x1.value),
                "tolerancia": float(tolerancia.value),
                "max_iter": int(max_iter.value)
            }

            response = requests.post(url, json=data)

            res = response.json()

            iteraciones = res["iteraciones"]

            for item in iteraciones:

                tabla_secante.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(item["n"]))),
                            ft.DataCell(ft.Text(str(item["xi_1"]))),
                            ft.DataCell(ft.Text(str(item["xi"]))),
                            ft.DataCell(ft.Text(str(item["x_next"]))),
                            ft.DataCell(ft.Text(str(item["error_pct"])))
                        ]
                    )
                )

            ultima = iteraciones[-1]

            texto_resultado.value = f"Raíz Secante: {ultima['x_next']}"

            page.update()

        except Exception as error:

            texto_resultado.value = f"Error: {error}"

            page.update()

    # CAMPOS GENERALES
   

    ip_backend = ft.TextField(
        label="IP Backend",
        value="ip :8000",
        border_radius=15,
        filled=True,
        bgcolor="white"
    )

    tolerancia = ft.TextField(
        label="Tolerancia",
        border_radius=15,
        filled=True,
        bgcolor="white"
    )

    max_iter = ft.TextField(
        label="Máximo Iteraciones",
        border_radius=15,
        filled=True,
        bgcolor="white"
    )

   
    # CAMPOS NEWTON
   

    h_inicial = ft.TextField(
        label="Altura Inicial",
        border_radius=15,
        filled=True,
        bgcolor="white"
    )

   
    # CAMPOS SECANTE
    

    x0 = ft.TextField(
        label="x0",
        border_radius=15,
        filled=True,
        bgcolor="white"
    )

    x1 = ft.TextField(
        label="x1",
        border_radius=15,
        filled=True,
        bgcolor="white"
    )

   
    # BOTONES
    

    boton_newton = ft.ElevatedButton(
        "Calcular Newton",
        width=320,
        height=50,
        bgcolor="#C4B5FD",
        color="white",
        on_click=calcular_newton
    )

    boton_secante = ft.ElevatedButton(
        "Calcular Secante",
        width=320,
        height=50,
        bgcolor="#C4B5FD",
        color="white",
        on_click=calcular_secante
    )

    
    # RESULTADO
    

    texto_resultado = ft.Text(
        "",
        size=18,
        weight="bold",
        color="#111827",
        font_family="Poppins"
    )

    # HEADER
    

    header = ft.Container(

        width=float("inf"),

        content=ft.Column(
            [
                ft.Icon(
                    ft.Icons.CALCULATE,
                    size=50,
                    color="purple"
                ),

                ft.Text(
                    "Newton y Secante",
                    size=30,
                    weight="bold",
                    color="black",
                    font_family="Poppins"
                ),
            ],
            horizontal_alignment="center"
        ),

        gradient=ft.LinearGradient(
            colors=["#C4B5FD", "#F5D0FE"]
        ),

        padding=30
    )

    
    # CARD NEWTON
  

    card_newton = ft.Container(

        visible=True,

        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.FUNCTIONS,
                            color="#4f46e5"
                        ),

                        ft.Text(
                            "Método Newton-Raphson",
                            size=22,
                            weight="bold",
                            font_family="Poppins"
                        )
                    ]
                ),

                h_inicial,
                tolerancia,
                max_iter,
                boton_newton
            ],
            spacing=15
        ),

        bgcolor="#E6E6FA",
        padding=20,
        border_radius=20,
        margin=15,

        shadow=ft.BoxShadow(
            blur_radius=15,
            color="#d1d5db",
            offset=ft.Offset(0, 4)
        )
    )

    # CARD SECANTE
   

    card_secante = ft.Container(

        visible=False,

        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.SHOW_CHART,
                            color="#059669"
                        ),

                        ft.Text(
                            "Método Secante",
                            size=22,
                            weight="bold",
                            font_family="Poppins"
                        )
                    ]
                ),

                x0,
                x1,
                tolerancia,
                max_iter,
                boton_secante
            ],
            spacing=15
        ),

        bgcolor="#E6E6FA",
        padding=20,
        border_radius=20,
        margin=15,

        shadow=ft.BoxShadow(
            blur_radius=8,
            color="#d1d5db",
            offset=ft.Offset(0, 4)
        )
    )

    
    # CARD RESULTADO
    

    card_resultado = ft.Container(

        content=ft.Column(
            [
                ft.Row(
                    [
                      
                        ft.Text(
                            "Resultado",
                            size=22,
                            weight="bold",
                            font_family="Poppins"
                        )
                    ]
                ),

                texto_resultado
            ]
        ),

        bgcolor="#E6E6FA",
        padding=20,
        border_radius=20,
        margin=15,

        shadow=ft.BoxShadow(
            blur_radius=8,
            color="#d1d5db",
            offset=ft.Offset(0, 4)
        )
    )

    
    # CARD TABLA NEWTON
    card_tabla_newton = ft.Container(
        visible=True,
        content=ft.Column(
            [
                ft.Text(
                    "Tabla Newton",
                    size=22,
                    weight="bold",
                    font_family="Poppins"
                ),

                ft.Container(
                    content=ft.Column(
                        [
                            # AQUÍ AGREGAMOS EL ROW PARA EL SCROLL HORIZONTAL
                            ft.Row(
                                [tabla_newton], 
                                scroll="auto"
                            )
                        ],
                        scroll="auto" # Mantiene el scroll vertical
                    ),

                    height=300,
                    padding=10,
                    border_radius=10,
                    bgcolor="#E6E6FA"
                )
            ]
        ),

        bgcolor="light blue",
        padding=20,
        border_radius=20,
        margin=15,

        shadow=ft.BoxShadow(
            blur_radius=15,
            color="#d1d5db",
            offset=ft.Offset(0, 4)
        )
    )

    # CARD TABLA SECANTE
  
    card_tabla_secante = ft.Container(
        visible=False,
        content=ft.Column(
            [
                ft.Text(
                    "Tabla Secante",
                    size=22,
                    weight="bold",
                    font_family="Poppins"
                ),

                ft.Container(
                    content=ft.Column(
                        [
                            # AQUÍ AGREGAMOS EL ROW PARA EL SCROLL HORIZONTAL
                            ft.Row(
                                [tabla_secante], 
                                scroll="auto"
                            )
                        ],
                        scroll="auto" # Mantiene el scroll vertical
                    ),

                    height=300,
                    padding=10,
                    border_radius=10,
                    bgcolor="#E6E6FA"
                )
            ]
        ),

        bgcolor="light blue",
        padding=20,
        border_radius=20,
        margin=15,

        shadow=ft.BoxShadow(
            blur_radius=15,
            color="#d1d5db",
            offset=ft.Offset(0, 4)
        )
    )
    

    
    # MOSTRAR NEWTON
    

    def mostrar_newton(e):

        card_newton.visible = True
        card_tabla_newton.visible = True

        card_secante.visible = False
        card_tabla_secante.visible = False

        page.update()

    
    # MOSTRAR SECANTE
    

    def mostrar_secante(e):

        card_newton.visible = False
        card_tabla_newton.visible = False

        card_secante.visible = True
        card_tabla_secante.visible = True

        page.update()

    
    # APPBAR
    

    page.appbar = ft.AppBar(

        title=ft.Text(
            "Métodos Numéricos",
            weight="bold",
            font_family="Poppins",
            color="black"
        ),

        center_title=True,

        bgcolor="#C4B5FD",

        actions=[

            ft.PopupMenuButton(

                icon=ft.Icons.MENU,

                items=[

                    ft.PopupMenuItem(
                        content=ft.Text("Newton"),
                        on_click=mostrar_newton
                    ),

                    ft.PopupMenuItem(
                        content=ft.Text("Secante"),
                        on_click=mostrar_secante
                    )
                ]
            )
        ]
    )

    
    # AGREGAR TODO
   

    page.add(

        header,

        ip_backend,

        card_newton,

        card_secante,

        card_resultado,

        card_tabla_newton,

        card_tabla_secante
    )


ft.app(target=main)