import requests
from bs4 import BeautifulSoup
from pony import orm
from pony.orm import db_session

# Create database object
db = orm.Database()


# Create entity Product
class Product(db.Entity):
    id = orm.PrimaryKey(str, auto=False)
    description = orm.Required(str)
    normal_price = orm.Required(float)
    credit_price = orm.Required(float)
    url_product = orm.Required(str)


@db_session
def pushProduct(i, description, normal_price, credit_price, url):
    Product(id=i, description=description, normal_price=normal_price, credit_price=credit_price, url_product=url)


# MariaDb connect
db.bind(provider='mysql', host='localhost', user='robot_wscraping_insert', passwd='', db='DBWebScraping')
# Mapping
db.generate_mapping(create_tables=True)

# Get the page
page = requests.get('http://intelaf.com/Precios_stock_resultado.aspx?area=COMPU-PROC')
hostname = 'http://intelaf.com/'

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
# Selector to products
selector = '.contenedor_producto .descripcion '
# Select products container html (div a)
products_description = soup.select(selector)
products_normal_price = soup.select(selector + 'b i a')
products_credit_price = soup.select(selector + 'a strong')

# Create product dictionary
for credit_price, normal_price, product_description in \
        zip(products_credit_price, products_normal_price, products_description):
    # Get id: get href, clear link
    id = normal_price.get('href').replace('precios_stock_detallado.aspx?codigo=', '')
    # Get description, 'product_description.a' get de first 'a'.
    description = product_description.a.contents[0]
    # Get value,only number, set decimal point
    normal_price = int(''.join(filter(str.isdigit, normal_price.contents[0]))) / 100
    credit_price = int(''.join(filter(str.isdigit, credit_price.contents[0]))) / 100
    url = hostname + product_description.a.get('href')
    # Print info
    print('ID: ' + id)
    print('Description: ' + description)
    print('Normal price: ' + str(normal_price))
    print('Credit price: ' + str(credit_price))
    print('URL product: ' + url)
    print('\n')
    pushProduct(id, description, normal_price, credit_price, url)
