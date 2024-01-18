import flet as ft
import aiohttp
import asyncio



numero_pokemon = 0

#le decimos que es asincrona para que no se congele mientras hace peticiones a internet
#Asincrono = si hacemos A y B, no necesariamente debe ocurrir A y luego B, pueden ocurrir A y B en diferentes tiempos o al mismo tiempo sin afectar al otro
async def main(page: ft.Page): #le decimos que page es de flet, para poder acceder a las funciones de page
    #ahora podemos configurar la pagina
    
    #aca le decimos que espere a que pase la funcion 'await'
    # await page.add(ft.Text(value= "Hola mundo"))
    # pass

    #------------DIMENSIONES
    page.window_width = 720
    page.window_height= 1280
    page.window_resizable = False
    page.padding = 0
    page.fonts={
            "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
    }
    page.theme = ft.Theme(font_family="zpix")

    #defino los eventos de los clicks


    async def peticiones(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()


    async def evento_click(e: ft.ContainerTapEvent):
        global numero_pokemon
        if e.control == flecha_arriba: #si flecha arriba es true, aumenta 1, si no resta 1
            numero_pokemon +=1
        else:
            numero_pokemon -=1

        numero_actual = (numero_pokemon%151) +1 #modulo nos devuelve de 0 a 150, y le agregamos 1 para que empiece en 1 y termine en 151

        resultado = await peticiones(f"https://pokeapi.co/api/v2/pokemon/{numero_actual}") #pasamos el n° de pokemon como una variable
        print(resultado['name'])
        pokemon_peticion = f"Name: {resultado['name']}\n\nAbilities:"
        for elemeto in resultado['abilities']:
            habilidad = elemeto['ability']['name']
            pokemon_peticion += f"\n{habilidad}"
        pokemon_peticion += f"\n\nHeight: {resultado['height']}"
        texto_datos.value=pokemon_peticion

        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero_actual}.png"
        imagen.src = sprite_url

        await page.update_async()

    #evento vacio para cambiar despues
    # async def evento_vacio(e: ft.ContainerTapEvent):
    #     print("Evento!", e)


    #elemento tipo stack nos permite poner una cosa sobre la otra
        
    async def parpadeo ():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()
        
    luz_azul = ft.Container(width=70,
        height=70,
        left= 5,
        top =5,
        bgcolor=ft.colors.BLUE,
        border= ft.border.all(),
        border_radius = 50)
        
    boton_azul = ft.Stack([
        ft.Container(width=80,
        height=80,
        bgcolor=ft.colors.WHITE,
        border= ft.border.all(),
        border_radius = 50),
        
        luz_azul

        ]
    )

    item_superior = [      
        ft.Container(
            boton_azul,
            width=80,
            height=80
    ),
       ft.Container(
            width=40,
            height=40,
            border =ft.border.all(),
            border_radius= 50,
            bgcolor = ft.colors.RED_200
    ),
       ft.Container(
            width=40,
            height=40,
            border =ft.border.all(),
            border_radius= 50,
            bgcolor = ft.colors.YELLOW
    ),
       ft.Container(
            width=40,   
            height=40,
            border =ft.border.all(),
            border_radius= 50,
            bgcolor = ft.colors.GREEN
    )
    ]

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    imagen= ft.Image(src=sprite_url,
                 scale = 7,
                 width= 50,
                 height = 50,
                 top = 350/2,
                 left = 550/2)

    item_centro = ft.Stack([
        ft.Container(width=600,
                     height=400,
                     bgcolor=ft.colors.WHITE,
                     border_radius=10),

        ft.Container(width=550,
                     height=350,
                     left=25,
                     top = 25,
                     bgcolor=ft.colors.BLACK87),

        imagen    ])
    

    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(40,0),
            ft.canvas.Path.LineTo(0,50),
            ft.canvas.Path.LineTo(80,50),
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL,
        ),)
    ],
    width=80,
    height=50,)

    flecha_arriba = ft.Container(triangulo, #ponemos flecha arriba afuera para detectar si se toca este o no, asi nos devuleve true
                        width=80,
                         height=50,
                         on_click=evento_click
                         )

    flechas = ft.Column(
        [

            flecha_arriba,
            #rotate funciona con radianes, asique hay que pasar el angulo de grados a radianes
            ft.Container(triangulo,
                        rotate=ft.Rotate(angle=3.14159),
                        width=80,
                         height=50,
                         on_click=evento_click
                         ),
        ]
    )

    texto_datos = ft.Text(value="...",
                          color = ft.colors.BLACK,
                          size=22)


    item_inferior = [
        ft.Container(width=50,
                     ), #margen izquierdo

        ft.Container(texto_datos,
                     padding=10,
                     width=400,
                     height=300,
                     bgcolor = ft.colors.GREEN,
                     border_radius=20,
                     border=ft.border.all()
                     ),
        ft.Container(width=50,
                     ), #margen derecho
 
        ft.Container(flechas,
                     width=80,
                     height= 120,  
                     )

    ]

    #3)Creamos la fila
    
    superior = ft.Container(content=ft.Row(item_superior),
        width=600,
        height=80,
        margin=ft.margin.only(top=40)
    )


    centro = ft.Container(content=item_centro,
        width=600,
        height=400,
        margin=ft.margin.only(top=40),
        alignment=ft.alignment.center
    )
    
    inferior = ft.Container(
        content=ft.Row(item_inferior),
        width=600,
        height=400,
        margin=ft.margin.only(top=40)
    )

    #2) CREAMOS UNA UNICA COLUMNA que va a contener 3 filas

    col = ft.Column(
        spacing= 0,
        #Esta columna va a tener 3 filas
        controls=[
            superior,
            centro,
            inferior,
        ]
    )

    #1) ESTE CONTENEDOR ES LA PAGINA PRINCIPAL, EL fondo
    contenedor = ft.Container (col,
        width=720,
        height=1280,
        bgcolor=ft.colors.RED,
        alignment=ft.alignment.top_center
    )
    await page.add_async(contenedor)
    await parpadeo()

ft.app(target=main)