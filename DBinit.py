# Host: sql12.freesqldatabase.com
# Database name: sql12714086
# Database user: sql12714086
# Database password: fAbSxAerrP
# Port number: 3306
import mysql.connector

username = 'sql12714086'
host="sql12.freesqldatabase.com"
password = "fAbSxAerrP"
database = "sql12714086"

def trial():
  mydb = mysql.connector.connect(
      username = username,
      host = host,
      password = password,
      database = database
    )
  cur = mydb.cursor()
  cur.execute("show databases;")
  print(cur.fetchall())



# cur.execute("""CREATE TABLE Purchases (
#     PurchaseID VARCHAR(10),
#     UserID VARCHAR(10),
#     RequesterName VARCHAR(50),
#     ItemID VARCHAR(10),
#     SupplierID VARCHAR(10),
#     PurchaseDate DATE,
#     DeliveryDate DATE,
#     Quantity INT,
#     UnitPrice DECIMAL(10,2),
#     TotalCost DECIMAL(10,2),
#     CostCenter VARCHAR(10),
#     GLAccount VARCHAR(10),
#     PONumber VARCHAR(10),
#     Currency VARCHAR(10),
#     UserName VARCHAR(50),
#     Department VARCHAR(50),
#     Role VARCHAR(50),
#     Budget DECIMAL(10,2),
#     SupplierName VARCHAR(50),
#     Country VARCHAR(50),
#     ContactNumber VARCHAR(20),
#     Email VARCHAR(50),
#     Rating DECIMAL(3,2),
#     AvgDeliveryTime INT,
#     LeadTime INT,
#     ReliabilityScore DECIMAL(3,2),
#     ItemName VARCHAR(100),
#     Description TEXT,
#     Specifications TEXT,
#     Category VARCHAR(50),
#     Subcategory VARCHAR(50),
#     NumberOfPurchases INT,
#     NumberOfReviews INT
# );""")
# cur.execute("""INSERT INTO purchase_orders VALUES
#     ('PO001', 'US071', 'Robin Lopez', 'I031', 'SUP004', '2024-01-29', '2024-02-21', 20, 28.55, 571.00, 'CC81', 'GL15600', 'PO001', 'USD', 'Robin Lopez', 'Production', 'Procurement Manager', 7367, 'West-Burns', 'France', '+33 8109725063', 'west-burns@gmail.com', 4.14, 10, 14, 2.49, 'Dropbox', 'Cloud storage service for personal and business use with secure file sharing and sync.', 'Offers mobile apps, version history, and collaboration tools. Supports large file uploads.', 'Cloud Services', 'Cloud Storage Service', 61, 51),
#     ('PO002', 'US018', 'Bobby Flores', 'I077', 'SUP014', '2024-02-19', '2024-03-10', 15, 136.67, 2050.05, 'CC89', 'GL16400', 'PO002', 'USD', 'Bobby Flores', 'Production', 'Employee', 4130, 'Hinton Group', 'Brazil', '+55 6228064161', 'hintongroup@gmail.com', 2.25, 6, 9, 3.34, 'Emerson Sensi Wi-Fi Smart Thermostat', 'Affordable smart thermostat with easy DIY installation and intuitive app for remote control.', 'Compatible with Alexa, Google Assistant, and Apple HomeKit.', 'Home Automation', 'Smart Thermostat', 24, 92),
#     ('PO003', 'US097', 'Vanessa Cooper', 'I005', 'SUP002', '2024-04-27', '2024-05-18', 11, 66.64, 733.04, 'CC35', 'GL10500', 'PO003', 'USD', 'Vanessa Cooper', 'Warehouse', 'Employee', 4498, 'Brown Inc', 'Japan', '+81 2101610896', 'browninc@gmail.com', 3.96, 8, 9, 4.49, 'Avast Premium Security', 'Full online protection for all of your devices.', 'Includes real-time threat detection, ransomware protection, and privacy firewall.', 'Security Software', 'Antivirus Software', 70, 14),
#     ('PO004', 'US038', 'Kenneth Kent', 'I070', 'SUP008', '2024-01-31', '2024-02-22', 4, 261.9, 1047.6, 'CC56', 'GL13100', 'PO004', 'USD', 'Kenneth Kent', 'Marketing', 'Department Head', 6855, 'Short Ltd', 'China', '+86 5851770892', 'shortltd@gmail.com', 2.34, 6, 7, 2.23, 'Ninja Specialty Coffee Maker', 'Multi-functional coffee maker with built-in frother for specialty drinks like lattes and cappuccinos.', 'Brews hot or iced coffee and includes fold-away frother for easy storage.', 'Kitchen Appliances', 'Coffee Maker', 30, 71);
# """)

# cur.execute("ALTER table Purchases rename purchase_orders ;")

query = "Create Table buyer_received_docs(PONumber VARCHAR(10), BOL BOOLEAN, PFI BOOLEAN, Drawings Boolean, MQIC BOOLEAN)"
query = "Create Table supplier_received_docs(PONumber VARCHAR(10), LOC BOOLEAN)"

query = "Create table requestor_supplier(PONumber Varchar(10), requestor VARCHAR(255), supplier VARCHAR(255))"


# cur.execute(query)


# cur.execute("Select * from purchase_orders;")
# cur.execute("show tables;")
# print(cur.fetchall())
