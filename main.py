# Melakukan import terhadap modul yang dibutuhkan
import mysql.connector 
from mysql.connector import Error
import pandas as pd
import datetime

# Membuat fungsi koneksi python dengan RDBS di SQL
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db)
        print("MySQL database connection successfull")
    except Error as err:
        print(f"Error: {err}")
    return connection

# Definisi parameter
nama_host = "localhost"
user = "root"
password = "Datascience2022"
db = "db_lib"

# Koneksi ke database 'db_lib'
connection = create_db_connection(nama_host, user, password, db)

# Membuat fungsi untuk menambahkan user perpustakaan
def add_new_user():
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #User Input pada opsi
    nama_user = input("Masukkan Nama User: ")
    tgl_user = input("Masukkan Tanggal Lahir(YYYY-MM-DD): ")
    pek_user = input("Masukkan Pekerjaan: ")
    alamat_user = input("Masukkan Alamat: ")
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    sql = f"INSERT INTO user(nama_user, tanggal_lahir, pekerjaan, alamat) VALUES ('{nama_user}', '{tgl_user}', '{pek_user}', '{alamat_user}')"         
    mycursor.execute(sql)
    mydb.commit()
    
    #Print querry berhasil dieksekusi
    print("Query berhasil dieksekusi")
    print("-------------------------")
    print("Data berhasil ditambahkan")
    
# Membuat fungsi untuk menambahkan buku perpustakaan    
def add_new_book():
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #User Input pada opsi
    id_buku = input("Masukkan Kode Buku: ")
    nama_buku = input("Masukkan Nama Buku: ")
    category_buku = input("Masukkan Kategori Buku: ")
    stock_buku = input("Masukkan Stock Buku: ")
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    sql = f"INSERT INTO buku VALUES ({id_buku}, '{nama_buku}', '{category_buku}', {stock_buku})"         
    mycursor.execute(sql)
    mydb.commit()
    
    #Print querry berhasil dieksekusi
    print("Query berhasil dieksekusi")
    print("-------------------------")
    print("Data berhasil ditambahkan")

# Membuat fungsi untuk menambahkan transaksi pinjam buku perpustakaan
def add_new_trans():
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #User Input pada opsi
    id_user_pinjam = input("Masukkan ID Peminjaman: ")
    id_buku_pinjam = input("Masukkan ID Buku: ")
    nama_user_pinjam = input("Masukkan Nama Peminjam: ")
    nama_buku_pinjam = input("Masukkan Nama Buku: ")
    tanggal_pinjam = datetime.datetime.today() # Peminjaman dilakukan pada hari ini
    tanggal_kembali = tanggal_pinjam + datetime.timedelta(days=3) # Pengembalian dilakukan 3 hari setelah pinjam
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    sql = f"INSERT INTO peminjaman VALUES ('{id_user_pinjam}', '{id_buku_pinjam}', '{nama_user_pinjam}', '{nama_buku_pinjam}','{tanggal_pinjam.strftime('%Y-%m-%d')}', '{tanggal_kembali.strftime('%Y-%m-%d')}')"
    sql_update = f"UPDATE buku SET stock = stock - 1 WHERE id_buku = {id_buku_pinjam}" # Mengurangi stock buku yang dipinjam
    mycursor.execute(sql)
    mycursor.execute(sql_update)
    mydb.commit()
    
    #Print querry berhasil dieksekusi
    print("Query berhasil dieksekusi")
    print("-------------------------")
    print(f"Buku telah dipinjamkan ke: {nama_user_pinjam}")

# Membuat fungsi untuk menampilkan seluruh buku perpustakaan
def show_buku():
    #Counter terhadap iterasi
    no = 0
    
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    mycursor.execute('SELECT * FROM buku;')
    cursor = mycursor.fetchall()
    
    #Print header dari kolom
    print(mycursor.column_names)
    
    #Itersi terhadap setiap baris
    for data in cursor:
        no += 1
        print(data)
    
# Membuat fungsi untuk menampilkan seluruh user perpustakaan
def show_user():
    #Counter terhadap iterasi
    no = 0
    
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    mycursor.execute('SELECT * FROM user;')
    cursor = mycursor.fetchall()
    
    #Print header dari kolom
    print(mycursor.column_names)
    
    #Itersi terhadap setiap baris
    for data in cursor:
        no += 1
        print(data)    

# Membuat fungsi untuk menampilkan seluruh transaksi peminjaman perpustakaan
def show_trans():
    #Counter terhadap iterasi
    no = 0
    
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    mycursor.execute('SELECT * FROM peminjaman;')
    result = mycursor.fetchall()
    
    #Print header dari kolom
    print(mycursor.column_names)
    
    
    if mycursor.rowcount == 0: #Defensive apabila tidak terdapat transaksi peminjaman
        print("Belum terdapat peminjaman")
    else:
        for data in result: #Itersi terhadap setiap baris
            no += 1
            print(data)  

# Membuat fungsi untuk melakukan pencarian terhadap buku dengan keyword yang diinginkan
def cari_buku(): 
    #User Input buku yang ingin dicari
    seach_book = input("Masukkan Nama Buku: ")
    
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #Syntax SQL yang dimasukkan ke mysqlconnector
    mycursor.execute(f"SELECT * FROM buku WHERE nama_buku LIKE '%{seach_book}%';")
    cursor = mycursor.fetchall()
    
    
    if mycursor.rowcount == 0: #Defensive apabila tidak terdapat transaksi peminjaman
        print("Buku tidak tersedia")
    else:
        columns = mycursor.description
        result = []
        for value in cursor: #Itersi terhadap setiap baris dan memunculkan header kolom
            tmp = {}
            for (index,column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
        print(pd.DataFrame(result))    

# Membuat fungsi untuk melakukan pengembalian buku yang dipinjamkan
def kembalikan_buku():
    #Koneksikan dengan SQL
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    
    #User Input buku yang ingin dikembalikan
    id_user_pinjam = input("Masukkan ID Peminjaman: ")
    id_buku_pinjam = input("Masukkan ID Buku: ")
    
    # Menghapus dari daftar pinjaman untuk buku yang akan dikembalikan
    sql = f"DELETE FROM peminjaman WHERE id_user = {id_user_pinjam} AND id_buku = {id_buku_pinjam}"
    
    # Mengembalikan stock buku ke semula
    sql_update = f"UPDATE buku SET stock = stock + 1 WHERE id_buku = {id_buku_pinjam}"
    
    #Eksekusi Syntax SQL ke mysqlconnector
    mycursor.execute(sql)
    mycursor.execute(sql_update)
    mydb.commit()
    
    #Print querry berhasil dieksekusi
    print("Query berhasil dieksekusi")
    print("-------------------------")
    if mycursor.rowcount == 0:
        print("Tidak ada peminjaman buku tersebut") #Defensive apabila input user salah
    else:
        print(f"Buku telah dikembalikan") #Buku berhasil dikembalikan

# Fungsi agar program looping 
finished = False
while not finished:
    
    #Interface Program
    interface = """
    ....................LIBRARY MANAGEMENT.................... 
          1. Pendaftaran User Baru
          2. Pendaftaran Buku Baru
          3. Peminjaman Buku
          4. Tampilkan Daftar Buku
          5. Tampilkan Daftar User
          6. Tampilkan Daftar Peminjaman
          7. Cari Buku
          8. Pengembalian
          9. Exit
    """
    print(interface)
    
    #Opsi User Interface untuk masing-masing pilihan
    choice = int(input('Masukkan nomor tugas:'))
    
    if choice == 1: # Pendaftaran User Baru
        #Tampilkan data
        print("-------------------------------------")
        add_new_user()
            
    elif choice == 2: # Pendaftaran Buku Baru
        #Tampilkan data
        print("-------------------------------------")
        add_new_book()
        
    elif choice == 3: # Peminjaman
        #Tampilkan data
        print("-------------------------------------")
        add_new_trans()       
        
    elif choice == 4: # Tampilkan Daftar Buku
        #Tampilkan data
        print("-------------------------------------")
        show_buku()         
        
    elif choice == 5: # Tampilkan Daftar User
        #Tampilkan data
        print("-------------------------------------")
        show_user()         
        
    elif choice == 6:# Tampilkan Daftar Peminjaman
        #Tampilkan data
        print("-------------------------------------")
        show_trans()        
        
    elif choice == 7: # Cari Buku
        #Tampilkan data
        print("-------------------------------------")
        cari_buku()                 
        
    elif choice == 8: # Pengembalian
        #Tampilkan data
        print("-------------------------------------")
        kembalikan_buku()            
        
        
    elif choice == 9: # Exit
        is_finished = input('Apakah anda ingin keluar? (Y/N) ').upper()
        
        if is_finished == 'Y':
            finished == True
            break # Aplikasi looping berhenti
        else:
            pass
            
    else:
        print("Masukan angka sesuai dengan menu!") # Defensive programming untuk angka yang tidak sesuai