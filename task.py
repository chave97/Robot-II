from RPA.HTTP import HTTP
from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables
from RPA.Dialogs import Dialogs
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.FileSystem import FileSystem
import time

MODAL_CONTAINER="css:div[class='container']"
MODAL_HEADER="css:div[class='modal-header'"
MODAL_OK_BUTTON="xpath://*[@class='btn btn-dark'][text()='OK']"

ROBOT_HEAD_LOCATOR="xpath://*[@class='custom-select'][@name='head']"
ROBOT_LEG_LOCATOR="//*[@class='form-control'][@placeholder='Enter the part number for the legs']"
ROBOT_ADDRESS_LOCATOR="//*[@class='form-control'][@placeholder='Shipping address']"
ROBOT_PREVIEW_BUTTON="xpath://*[@id='preview'][@type='submit']"
ROBOT_ORDER_BUTTON="xpath://*[@id='order'][text()='Order']"
ROBOT_ORDER_ERROR="xpath://*[@class='alert alert-danger'][@role='alert']"
ROBOT_SCREENSHOOT_PATH="output/images/robot{}-screenshoot.png"
ROBOT_RECEIPT_PATH="./output/Order{}.pdf"

def wait():
    time.sleep(1)

def obtainUrl():
    dialog = Dialogs()
    dialog.add_text("Porfavor ingrese url de archivo .csv")
    dialog.add_text_input("url")
    result = dialog.run_dialog()
    return(result["url"])

def verifyModal():
    browser.wait_until_element_is_enabled(MODAL_CONTAINER)
    if browser.is_element_enabled(MODAL_HEADER):
        browser.click_button(MODAL_OK_BUTTON)

def downloadCSV():
    http = HTTP()
    url = obtainUrl()
    http.download(url,target_file="output/SalesOrder.csv")

def readCSV():
    tableLib = Tables()
    table = tableLib.read_table_from_csv("output/SalesOrder.csv")
    table.group_by_column("Order number") #Necesary?
    return(table)

def fillForm(order):
    if browser.is_element_enabled(ROBOT_HEAD_LOCATOR):
        browser.select_from_list_by_index(ROBOT_HEAD_LOCATOR,order["Head"])
        browser.select_radio_button("body",order["Body"])
        browser.input_text(ROBOT_LEG_LOCATOR,order["Legs"])
        browser.input_text(ROBOT_ADDRESS_LOCATOR,order["Address"])
        browser.click_button(ROBOT_PREVIEW_BUTTON)
        wait()
        #Save Robot Preview Screenshoot
        browser.screenshot("id:robot-preview-image",filename=ROBOT_SCREENSHOOT_PATH.format(order["Order number"]))
        browser.click_button(ROBOT_ORDER_BUTTON)
        wait()
        visible_error = browser.is_element_visible(ROBOT_ORDER_ERROR)
        while visible_error:
            browser.click_button(ROBOT_ORDER_BUTTON)
            wait()
            if browser.is_element_visible("id:order-completion"):
                break
        wait()

def saveReceipt(order):
    pdf = PDF()
    receipt_table = browser.get_element_attribute("id:order-completion","outerHTML")
    pdf.html_to_pdf(receipt_table,ROBOT_RECEIPT_PATH.format(order["Order number"]))
    wait()
    pdf.open_pdf(ROBOT_RECEIPT_PATH.format(order["Order number"]))
    pdf.add_watermark_image_to_pdf(image_path=ROBOT_SCREENSHOOT_PATH.format(order["Order number"]),output_path=ROBOT_RECEIPT_PATH.format(order["Order number"]))
    pdf.close_pdf(ROBOT_RECEIPT_PATH.format(order["Order number"]))

def cleanFiles():
    archive = Archive()
    archive.archive_folder_with_zip("output","./output/Orders.zip",include="*.pdf")
    fileSystem = FileSystem()
    pdfOrders = fileSystem.find_files("output/*.pdf")
    for pdf in pdfOrders:
        fileSystem.remove_file(pdf)
    pngRobots = fileSystem.find_files("output/images/*.png")
    for image in pngRobots:
        fileSystem.remove_file(image)

def orderRobots():
    orderTable = readCSV()
    browser.open_available_browser("https://robotsparebinindustries.com/#/robot-order",maximized=True)
    for order in orderTable:
        verifyModal()
        fillForm(order)
        saveReceipt(order)
        browser.click_button("id:order-another")
    browser.close_browser()
    cleanFiles()

    

            
if __name__ == "__main__":   
    browser = Selenium()
    downloadCSV()
    orderRobots()
    cleanFiles()