from RPA.HTTP import HTTP
from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables
from RPA.Dialogs import Dialogs
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.FileSystem import FileSystem
import time


def obtain_url():
    dialog = Dialogs()
    dialog.add_text("Porfavor ingrese url de archivo .csv")
    dialog.add_text_input("url")
    result = dialog.run_dialog()
    return(result["url"])

def verify_modal():
    browser.wait_until_element_is_enabled("css:div[class='container']")
    if browser.is_element_enabled("css:div[class='modal-header'"):
        browser.click_button("xpath://*[@class='btn btn-dark'][text()='OK']")

def download_csv():
    url = obtain_url()
    http.download(url,target_file="output/SalesOrder.csv")

def read_csv():
    lcsv = Tables()
    table = lcsv.read_table_from_csv("output/SalesOrder.csv")
    table.group_by_column("Order number") #Necesary?
    return(table)

def genero_robots():
    table = read_csv()
    browser.open_available_browser("https://robotsparebinindustries.com/#/robot-order",maximized=True)
    for order in table:
        verify_modal()
        if browser.is_element_enabled("xpath://*[@class='custom-select'][@name='head']"):
            browser.select_from_list_by_index("xpath://*[@class='custom-select'][@name='head']",order["Head"])
            browser.select_radio_button("body",order["Body"])
            browser.input_text("//*[@class='form-control'][@placeholder='Enter the part number for the legs']",order["Legs"])
            browser.input_text("//*[@class='form-control'][@placeholder='Shipping address']",order["Address"])
            browser.click_button("xpath://*[@id='preview'][@type='submit']")
            time.sleep(1)
            robotScreenshot = browser.screenshot("id:robot-preview-image",filename="output/images/robot{}-screenshoot.png".format(order["Order number"]))
            browser.click_button("xpath://*[@id='order'][text()='Order']")
            time.sleep(1)
            visible_error = browser.is_element_visible("xpath://*[@class='alert alert-danger'][@role='alert']")
            while visible_error:
                browser.click_button("xpath://*[@id='order'][text()='Order']")
                time.sleep(1)
                if browser.is_element_visible("id:order-completion"):
                    break
            time.sleep(1)
            receipt_table = browser.get_element_attribute("id:order-completion","outerHTML")
            listOfFiles = []
            listOfFiles.append("output/images/robot{}-screenshoot.png".format(order["Order number"]))
            pdf.html_to_pdf(receipt_table,"./output/Order{}.pdf".format(order["Order number"]))
            print(listOfFiles)
            time.sleep(1)
            pdf.open_pdf("./output/Order{}.pdf".format(order["Order number"]))
            pdf.add_watermark_image_to_pdf(image_path="output/images/robot{}-screenshoot.png".format(order["Order number"]),output_path="./output/Order{}.pdf".format(order["Order number"]))
            pdf.close_pdf("./output/Order{}.pdf".format(order["Order number"]))
            time.sleep(1)
            browser.click_button("id:order-another")
            time.sleep(1)
    browser.close_browser()
    deleteFiles()
    

def deleteFiles():
    archivo = Archive()
    archivo.archive_folder_with_zip("output","./output/Orders.zip",include="*.pdf")
    fileSystem = FileSystem()
    pdfOrders = fileSystem.find_files("output/*.pdf")
    for pdf in pdfOrders:
        fileSystem.remove_file(pdf)
    pngRobots = fileSystem.find_files("output/images/*.png")
    for image in pngRobots:
        fileSystem.remove_file(image)
            
if __name__ == "__main__":   
    browser = Selenium()
    http = HTTP()
    pdf = PDF()
    #url = obtengo_url()
    #http.download(url,overwrite=True)
    genero_robots()
    #descargo_csv()
    #leo_csv()