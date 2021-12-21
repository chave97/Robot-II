#RPA.Tables para leer csv
#RPA.HTTP para descargar archivos
'''
Parte 1: Descargar el archivo orders.csv --> LISTO

Parte 2: Ingresar a la web de Robocorp --> LISTO

Parte 3: Verificar ventana "pop up" y aceptar terminos --> LISTO

Parte 4: Llenar campos de orden con datos de .csv

Parte 5: Generar pedido.

Parte 6: Descargar orden de pedido en PDF

Parte 7: Sacar captura al dibujo del robot

Parte 8: Poner dentro del PDF descargado la imagen del robot.

Parte 9: Una vez completados todos los pedidos, agrupar los archivos y comprimirlos en un .zip

Parte 10: Ver como meter el "Asistant"

'''

from RPA.HTTP import HTTP
from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables
from RPA.Dialogs import Dialogs

def obtengo_url():
    dialog = Dialogs()
    dialog.add_text("Porfavor ingrese url de archivo .csv")
    dialog.add_text_input("url")
    resultado = dialog.run_dialog()
    return(resultado["url"])

def verifico_modal():
    browser.open_available_browser("https://robotsparebinindustries.com/#/robot-order",maximized=True)
    browser.wait_until_element_is_enabled("css:div[class='container']")
    if browser.is_element_enabled("css:div[class='modal-header'"):
        browser.click_button("xpath://*[@class='btn btn-dark'][text()='OK']")

def obtengo_datos_csv():
    print("arranco leyendo el csv")

def genero_robots():
    print("me desplazo por la página")

   
browser = Selenium()
http = HTTP()

#url = obtengo_url()
#http.download(url,overwrite=True)
verifico_modal()

