import requests
from bs4 import BeautifulSoup
from pony import orm

# Create database object
db = orm.Database()


# Create entity Product
class Product(db.Entity):
    id = orm.PrimaryKey(str)
    description = orm.Required(str)
    normal_price = orm.Required(int)
    credit_price = orm.Required(int)
    url_product = orm.Required(str)


# MariaDb connect
db.bind(provider='mysql', host='localhost', user='d3h', passwd='', db='webscraping')
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
    # Print info
    print('ID: ' + id)
    print('Description: ' + description)
    print('Normal price: ' + str(normal_price))
    print('Credit price: ' + str(credit_price))
    print('URL product: ' + hostname + product_description.a.get('href'))
    print('\n')
