# tugas4_python

Repository ini berisikan Project Library Management System (LMS) dengan Python untuk pemenuhan Tugas 4 Python Pacmann

**1. Tujuan Pengerjaan Project**

Terdapat beberapa objective pada proyek ini diantaranya adalah:
- Mebuat program LMS menggunakan Python
- Membuat program python yang dapat terhubung ke database relational
- Mengaplikasikan pembuatan program dengan paradigma pemograman berbasis fungsi atau pemograman berbasis objek
- Mengaplikasikan penulisan kode yang bersih (mengacu ke PEP 8)

**2. Detail / Deskripsi Task**

**a. Overview Proyek**
Proyek ini terdiri dari Library Management System Sederhana dengan beberapa fitur yaitu:
- Pendaftaran anggota perpustakaan
- Pendaftaran buku baru
- Peminjaman
- Menampilkan data anggota, buku, dan daftar peminjaman
- Melakukan pencarian buku

**b. Tools**
Proyek ini menggunakan Bahasa pemograman (Python) dan Database (MySQL)

**c. Alur Pengerjaan**
Proyek ini terdiri dari beberapa tahapan yaitu:

**- Tahap 1. Pembuatan Database (MySQL)**
Pembuatan database dummy sebagai data yang akan diakses oleh user. Adapun tahapan pada MySQL sebagai berikut:

```# Membuat database
CREATE DATABASE db_lib;

# Menggunakan database yang dibuat
USE db_lib;

# Membuat tabel daftar user perpustakaan
CREATE TABLE user(
	id_user INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nama_user VARCHAR(50),
    tanggal_lahir DATE,
    pekerjaan VARCHAR(50),
    alamat VARCHAR(100)
);

# Membuat tabel daftar buku
CREATE TABLE buku(
	  id_buku INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nama_buku VARCHAR(50),
    kategori VARCHAR(50),
    stock INT
);

# Membuat tabel transaksi pinjaman buku
CREATE TABLE peminjaman(
	  id_user INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	  id_buku INT,
    nama_user VARCHAR(50),
    nama_buku VARCHAR(50),
    tanggal_pinjam DATE,
    tanggal_kembali DATE
);

# Melakukan setting terhadap Foreign Key
ALTER TABLE peminjaman ADD FOREIGN KEY (id_user) REFERENCES user(id_user);
ALTER TABLE peminjaman ADD FOREIGN KEY (id_buku) REFERENCES buku(id_buku);
ALTER TABLE user AUTO_INCREMENT=15;

# Melakukan input data dummy terhadap tabel User
INSERT INTO user VALUES (01, 'Andi', '1995-02-15', 'Mahasiswa', 'Jakarta Pusat');
INSERT INTO user VALUES (02, 'Bambang', '1993-02-15', 'Pegawai Swasta', 'Cilincing');
INSERT INTO user VALUES (03, 'Cici', '1980-04-24', 'CEO', 'Sawangan');
INSERT INTO user VALUES (04, 'Dani', '2000-10-03', 'Pelajar', 'Grogol');
INSERT INTO user VALUES (05, 'Elvian', '1997-07-21', 'Mahasiswa', 'Mampang');
INSERT INTO user VALUES (06, 'Fahmi', '1986-06-27', 'Wiraswasta', 'Tanjung Barat');
INSERT INTO user VALUES (07, 'Geovanni', '1998-08-03', 'Mahasiswa', 'Pondok Kopi');
INSERT INTO user VALUES (08, 'Hafsah', '1989-01-17', 'PNS', 'Kalibata');
INSERT INTO user VALUES (09, 'Imran', '1990-11-04', 'Pegawai Swasta', 'Cibubur');
INSERT INTO user VALUES (10, 'Jaka', '1978-09-04', 'Wiraswasta', 'Rawamangun');
INSERT INTO user VALUES (11, 'Kido', '1995-09-02', 'Mahasiswa', 'Plumpang');
INSERT INTO user VALUES (12, 'Linda', '2002-11-03', 'Pelajar', 'Tebet');
INSERT INTO user VALUES (13, 'Mahdi', '1990-05-29', 'Pegawai BUMN', 'Cawang');
INSERT INTO user VALUES (14, 'Nanda', '1993-12-11', 'Pegawai Swaste', 'Ancol');
INSERT INTO user(nama_user, tanggal_lahir, pekerjaan, alamat) VALUES ('Opang', '2005-09-01', 'Pelajar', 'Duren Sawit');

# Melakukan input data dummy terhadap tabel buku
INSERT INTO buku VALUES (1001, 'Belajar Python', 'Teknologi', 4);
INSERT INTO buku VALUES (1002, 'Rich People Problems', 'Novel', 3);
INSERT INTO buku VALUES (1003, 'Cantik Itu Luka', 'Novel', 2);
INSERT INTO buku VALUES (1004, 'Rich Dad Poor Dad', 'Investasi', 1);
INSERT INTO buku VALUES (1005, 'Data Wrangling in SQL', 'Teknologi', 3);
INSERT INTO buku VALUES (1006, 'Laa Tazhan', 'Agama', 2);
INSERT INTO buku VALUES (1007, 'Guns, Germs, and Steel', 'Sejarah', 4);
INSERT INTO buku VALUES (1008, '7 Habits', 'Self-Development', 3);
INSERT INTO buku VALUES (1009, 'Belajar Technical Analysis Saham', 'Invenstasi', 1);
INSERT INTO buku VALUES (1010, 'Harimau Harimau', 'Novel', 1);
```
Adapun output ERM dari file SQL tersebut adalah sebagai berikut:

![image](https://user-images.githubusercontent.com/87402782/180632910-7449bd87-bd3d-41e1-b936-261f8df55405.png)

**- Tahap 2. Melakukan import modul yang dibutuhkan**

Berikut merupakan modul-modul yang dibutuhkan untuk pengerjaan proyek

```
import mysql.connector 
from mysql.connector import Error
import pandas as pd
import datetime
```
**- Tahap 3. Membuat connection antara python dan SQL**

Untuk melakukan koneksi python dan SQL digunakan mysql.connector, namun sebelumnya dibuat fungsi *create_db_connection*

```
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
```

Untuk melakukan koneksi, perlu didefiniskan nama host, user, password, dan database

```
# definisi parameter
nama_host = "localhost"
user = "root"
password = "Datascience2022"
db = "db_lib"

# koneksi ke database 'db_lib'
connection = create_db_connection(nama_host, user, password, db)
```

**- Tahap 4. Membuat fungsi add_new_user (Mendaftarkan user baru ke system perpustakaan)**

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Fungsi ini akan menerima inputan user yaitu :

a. nama_user (str), 
b. tgl_user / tanggal lahir user (date), 
c. pek_user / pekerjaan user (str)
d. alamat_user (str)

- Hasil inputkan tersebut dimasukan ke variabel sql menggunakan syntax SQL *INSER INTO user ___ VALUES ___*

- Selanjutnya dilakukan eksekusi dengan ```mycursor.execute(sql)``` dan dilakukan commit ```mydb.commit()```

- Print Query berhasil dieksekusi dan Data berhasil ditambahkan

```
def add_new_user():
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    nama_user = input("Masukkan Nama User: ")
    tgl_user = input("Masukkan Tanggal Lahir(YYYY-MM-DD): ")
    pek_user = input("Masukkan Pekerjaan: ")
    alamat_user = input("Masukkan Alamat: ")
    sql = f"INSERT INTO user(nama_user, tanggal_lahir, pekerjaan, alamat) VALUES ('{nama_user}', '{tgl_user}', '{pek_user}', '{alamat_user}')"         
    mycursor.execute(sql)
    mydb.commit()
    print("Query berhasil dieksekusi")
    print("-------------------------")
    print("Data berhasil ditambahkan")
```

**- Tahap 4. Membuat fungsi add_new_book (Mendaftarkan buku baru kedalam library)**

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Fungsi ini akan menerima inputan user yaitu :

a. id_buku (int), 
b. nama_buku (str), 
c. category_buku (str)
d. stock_buku (int)

- Hasil inputkan tersebut dimasukan ke variabel sql menggunakan syntax SQL *INSER INTO buku ___ VALUES ___*

- Selanjutnya dilakukan eksekusi dengan ```mycursor.execute(sql)``` dan dilakukan commit ```mydb.commit()```

- Print Query berhasil dieksekusi dan Data berhasil ditambahkan

```
def add_new_book():
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    id_buku = input("Masukkan Kode Buku: ")
    nama_buku = input("Masukkan Nama Buku: ")
    category_buku = input("Masukkan Kategori Buku: ")
    stock_buku = input("Masukkan Stock Buku: ")
    sql = f"INSERT INTO buku VALUES ({id_buku}, '{nama_buku}', '{category_buku}', {stock_buku})"         
    mycursor.execute(sql)
    mydb.commit()
    print("Query berhasil dieksekusi")
    print("-------------------------")
    print("Data berhasil ditambahkan")
```

**- Tahap 5. Membuat fungsi add_new_trans (Melakukan input terhadap peminjaman buku)**

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Fungsi ini akan menerima inputan user yaitu :

a. id_user_pinjam (int), 
b. id_buku_pinjam (int), 
c. nama_user_pinjam (str)
d. nama_buku_pinjam (str)

- Sedangkan varible berikut akan otomatis terisi
a. tanggal_pinjam (date) --> Otomatis tanggal pinjam hari ini
b. tanggal_kembali (date) --> Otomatis tanggal kembali adalah 3 hari dari tanggal peminjaman

- Hasil inputkan tersebut dimasukan ke variabel sql menggunakan syntax SQL *INSER INTO peminjaman ___ VALUES ___*

- Untuk mengakomodir fungsi stock buku yang berkurang, maka diinputkan ke var sql_update berupa update nilai stock buku, yaitu ```f"UPDATE buku SET stock = stock - 1 WHERE id_buku = {id_buku_pinjam}"```

- Selanjutnya dilakukan eksekusi dengan ```mycursor.execute(sql)```, ```mycursor.execute(sql_update)``` dan dilakukan commit ```mydb.commit()```

- Print Query berhasil dieksekusi dan ```print(f"Buku telah dipinjamkan ke: {nama_user_pinjam}")```

```
def add_new_trans():
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    id_user_pinjam = input("Masukkan ID Peminjaman: ")
    id_buku_pinjam = input("Masukkan ID Buku: ")
    nama_user_pinjam = input("Masukkan Nama Peminjam: ")
    nama_buku_pinjam = input("Masukkan Nama Buku: ")
    tanggal_pinjam = datetime.datetime.today()
    tanggal_kembali = tanggal_pinjam + datetime.timedelta(days=3)
    sql = f"INSERT INTO peminjaman VALUES ('{id_user_pinjam}', '{id_buku_pinjam}', '{nama_user_pinjam}', '{nama_buku_pinjam}','{tanggal_pinjam.strftime('%Y-%m-%d')}', '{tanggal_kembali.strftime('%Y-%m-%d')}')"
    sql_update = f"UPDATE buku SET stock = stock - 1 WHERE id_buku = {id_buku_pinjam}"
    mycursor.execute(sql)
    mycursor.execute(sql_update)
    mydb.commit()
    print("Query berhasil dieksekusi")
    print("-------------------------")
    print(f"Buku telah dipinjamkan ke: {nama_user_pinjam}")
```

**- Tahap 6. Membuat fungsi show_buku (Menampilkan seluruh buku yang telah terdaftar)**

- Set variable ```no = 0``` sebagai counter

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Untuk menampilkan seluruh buku, inputkan syntax Querry SQL ```'SELECT * FROM buku;'``` pada ```mycursor.execute```

- Tampilkan hasil Querry dengan ```mycursor.fetchall()```

- Menampilkan header kolom dengan ```print(mycursor.column_names)```

- Iterasi setiap baris hasil fetch dengan syntax berikut:

``` 
for data in cursor:
  no += 1
  print(data)
```

```
def show_buku():
    no = 0
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM buku;')
    cursor = mycursor.fetchall()
    print(mycursor.column_names)
    for data in cursor:
        no += 1
        print(data)
```

**- Tahap 7. Membuat fungsi show_user (Menampilkan seluruh user yang telah terdaftar)** 

- Set variable ```no = 0``` sebagai counter

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Untuk menampilkan seluruh buku, inputkan syntax Querry SQL ```'SELECT * FROM user;'``` pada ```mycursor.execute```

- Tampilkan hasil Querry dengan ```mycursor.fetchall()```

- Menampilkan header kolom dengan ```print(mycursor.column_names)```

- Iterasi setiap baris hasil fetch dengan syntax berikut:

``` 
for data in cursor:
  no += 1
  print(data)
```

```
def show_user():
    no = 0
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM user;')
    cursor = mycursor.fetchall()
    print(mycursor.column_names)
    for data in cursor:
        no += 1
        print(data)  
```

**- Tahap 8. Membuat fungsi show_trans (Menampilkan seluruh buku yang sedang dipinjam)** 

- Set variable ```no = 0``` sebagai counter

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Untuk menampilkan seluruh buku, inputkan syntax Querry SQL ```'SELECT * FROM peminjaman;'``` pada ```mycursor.execute```

- Tampilkan hasil Querry dengan ```mycursor.fetchall()```

- Menampilkan header kolom dengan ```print(mycursor.column_names)```

- Lakukan *defensive programming* apabila tidak terdapat peminjaman dengan 

```
    if mycursor.rowcount == 0:
        print("Belum terdapat peminjaman")
```

- Jika terdapat peminjaman, Iterasi setiap baris hasil fetch dengan syntax berikut:

```
    else:
        for data in result:
            no += 1
            print(data)  
```

```
def show_trans():
    no = 0
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM peminjaman;')
    result = mycursor.fetchall()
    print(mycursor.column_names)
    if mycursor.rowcount == 0:
        print("Belum terdapat peminjaman")
    else:
        for data in result:
            no += 1
            print(data)  
```

**- Tahap 9. Membuat fungsi cari_buku (Menampilkan daftar buku yang dicari menggunakan nama bukunya)** 

- Melakukan input nama buku dan assign ke variable search_book

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Untuk menampilkan buku yang dicari, inputkan syntax SQL ```f"SELECT * FROM buku WHERE nama_buku LIKE '%{seach_book}%';"``` pada ```mycursor.execute```

- Tampilkan hasil Querry dengan ```mycursor.fetchall()```

- Menampilkan header kolom dengan ```print(mycursor.column_names)```

- Lakukan *defensive programming* apabila tidak tersedia 

```
    if mycursor.rowcount == 0:
        print("Buku tidak tersedia")
```

- Jika tersedia, Iterasi setiap baris hasil fetch dengan syntax berikut:

```
    else:
        columns = mycursor.description
        result = []
        for value in cursor:
            tmp = {}
            for (index,column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
        print(pd.DataFrame(result))      
```

```
def cari_buku(): 
    seach_book = input("Masukkan Nama Buku: ")
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM buku WHERE nama_buku LIKE '%{seach_book}%';")
    cursor = mycursor.fetchall()
    if mycursor.rowcount == 0:
        print("Buku tidak tersedia")
    else:
        columns = mycursor.description
        result = []
        for value in cursor:
            tmp = {}
            for (index,column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
        print(pd.DataFrame(result))
```


**- Tahap 10. Membuat fungsi kembalikan_buku (Mengembalikan buku yang telah dipinjam)** 

- Membuat koneksi dengan mysql.connector.connect

```
mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
mycursor = mydb.cursor()
```

- Melakukan input pada variabel id_user_pinjam (int) dan id_buku_pinjam (int)

- Menghapus transaksi peminjaman untuk buku yang telah dikembalikan, inputkan syntax pada variabel sql ```f"DELETE FROM peminjaman WHERE id_user = {id_user_pinjam} AND id_buku = {id_buku_pinjam}"```

- Melakukan update pada stock buku yang telah dikembalikan, inputkan syntax pada variabel sql_update ```= f"UPDATE buku SET stock = stock + 1 WHERE id_buku = {id_buku_pinjam}"```

- Eksekusi syntax python yang ke sql menggunakan ```mycursor.execute(sql)``` dan ```mycursor.execute(sql_update)``` dan lakukan commit ```mydb.commit()```

- Menampilkan header kolom dengan ```print(mycursor.column_names)```

- Print pengembalian berhasil dengan ```print("Query berhasil dieksekusi")``` dan sebagai pembatas ```print("-------------------------")```

- Lakukan *defensive programming* apabila pengembalian buku yang tidak tersedia 

```
    if mycursor.rowcount == 0:
        print("Tidak ada peminjaman buku tersebut")
```

- Jika tersedia, print syntax berikut:

```
       print(f"Buku telah dikembalikan")   
```

```
def kembalikan_buku():
    mydb = mysql.connector.connect(host=nama_host, user=user, passwd=password, database=db)
    mycursor = mydb.cursor()
    id_user_pinjam = input("Masukkan ID Peminjaman: ")
    id_buku_pinjam = input("Masukkan ID Buku: ")
    sql = f"DELETE FROM peminjaman WHERE id_user = {id_user_pinjam} AND id_buku = {id_buku_pinjam}"
    sql_update = f"UPDATE buku SET stock = stock + 1 WHERE id_buku = {id_buku_pinjam}"
    mycursor.execute(sql)
    mycursor.execute(sql_update)
    mydb.commit()
    print("Query berhasil dieksekusi")
    print("-------------------------")
    if mycursor.rowcount == 0:
        print("Tidak ada peminjaman buku tersebut")
    else:
        print(f"Buku telah dikembalikan")
```


**- Tahap 11. Pembuatan Interface Program**

```
finished = False 
while not finished: # fungsi untuk membuat program looping terus menerus
    
    #Interface Program"
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
    
    choice = int(input('Masukkan nomor tugas:')) # fungsi percabangan untuk pilihan terhadap opsi program
    
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
            break  # stop looping, program berhenti
	else:
            pass
            
    else:
        print("Masukan angka sesuai dengan menu!") # defensive programming terhadap angka diluar yang 1-9
```

**3. Cara Running Program / Penggunaan Program**
- Pada terminal, akses directory sesuai dengan lokasi file ``main.py``

- Pastikan python sudah terinstall di terminal, jalankan syntax ```python main.py```

- Masukkan angka 1 - 8 sesuai dengan interface dari program. Masukkan Inputan yang diminta oleh program untuk mendapatkan hasil yang sesuai

- Masukkan angka 9 dan pilih Y untuk Exit program

**3. Hasil Case Test**
- Melakukan input user bernama Fandi, tanggal lahir 1995-06-03, pekerjaan PNS, dan alamat di Rawamangun

![Picture1](https://user-images.githubusercontent.com/87402782/180636923-61453445-5fa0-45b3-878f-b31cfdcb3332.png)

- Pengecekan ke Database Library, Fandi sudah masuk kedalam anggota perpustakaan

![Picture2](https://user-images.githubusercontent.com/87402782/180636940-20bdfa04-770d-41a4-9048-121bbdc45cca.png)

- Mendaftarkan buku baru dengan ID 1021, berjudul Kaizen, kategori Motivasi dengan Stock 4 buah

![Picture3](https://user-images.githubusercontent.com/87402782/180636973-f2cf2670-9018-417e-91a6-63c92ebb87eb.png)


- Pengecekan daftar buku, Kaizen berhasil ditambahkan 

![Picture4](https://user-images.githubusercontent.com/87402782/180636998-4ef9c27b-0173-49b7-b4d6-9c8f043fa82f.png)

- Fandi meminjam buku Belajar Python

![Picture5](https://user-images.githubusercontent.com/87402782/180637023-924a8c14-6033-4d32-8512-50cb28c83c40.png)

- Transaksi terhadap peminjaman buku oleh Fandi terhadap Belajar Python sudah masuk ke Daftar Peminjaman Buku

![Picture6](https://user-images.githubusercontent.com/87402782/180637046-bf9a5c68-cf78-41d6-892f-ffa64e6a296d.png)

- Stock buku Belajar Python berkurang dari 3 menjadi 2

![Picture7](https://user-images.githubusercontent.com/87402782/180637070-ed30f914-5de2-466b-a196-54b37571cada.png)

- Fandi mengembalikan buku Belajar Python

![Picture8](https://user-images.githubusercontent.com/87402782/180637095-06020199-e309-4dea-9480-e56af73cbb0e.png)

- Daftar peminjam buku atas nama Fandi dengan buku Belajar Python terhapus

![Picture9](https://user-images.githubusercontent.com/87402782/180637119-7e8e9ab4-2f11-4b36-ba53-fd8137130763.png)

- Stock buku Belajar Python kembali menjadi 3

![Picture10](https://user-images.githubusercontent.com/87402782/180637128-8a6576cd-2cce-4cd6-828b-7f3c1c5e404a.png)

- Mencari buku dengan keyword "Belajar" dan Exit Program

![Picture11](https://user-images.githubusercontent.com/87402782/180637145-311cf3b4-54e2-48bb-a734-370d127c0c30.png)

**4. Saran Perbaikan**

Saya menyadari butuh banyak perbaikan untuk aplikasi ini kedepannya, dikarekan keterbatasan waktu pengerjaan dan keterbatasan dari saya, adapun yang dapat di improve diantaranya:
1. Defensive Programming untuk setiap percabangan dan error yang mungkin terjadi untuk type data yang tidak sesuai perlu diperbaiki
2. Interface header kolom menggunakan pandas dataframe untuk interface yang lebih baik
3. Dikenakan program ini menggunakan konsep Functional Programming, dapat dicoba untuk membuat aplikasi berdasarkan Object Oriented Programming untuk memecah masing-masing fungsi ke dalam objek
