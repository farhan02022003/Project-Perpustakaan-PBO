import os
import mysql.connector
from colorama import Fore, Style
from datetime import datetime

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'peminjaman_buku'
)

cur = db.cursor()

class Sistem_peminjaman_buku:
    def tambah_buku(self,kode, judul,penulis,penerbit, tahun):
        self.kode = kode
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun = tahun

        cur.execute(f"INSERT INTO buku(kode_buku, judul_buku, penulis, penerbit, tahun_terbit,status) VALUES ('{self.kode}','{self.judul}','{self.penulis}','{self.penerbit}','{self.tahun}','ada')")
        db.commit()
        print(Fore.GREEN + '\nData berhasil ditambahkan'+ Style.RESET_ALL)

    def tampilkan_buku(self):
        cur.execute(f"SELECT * FROM buku;")
        data = cur.fetchall()
        for i in data:
            print(f'kode buku      : {i[0]}')
            print(f'Judul          : {i[1]}')
            print(f'penulis        : {i[2]}')
            print(f'penerbit       : {i[3]}')
            print(f'tahun terbit   : {i[4]}')
            print(f'status         : {i[5]}')
            print('-'*50)


    def cari_buku(self, judul_buku):
        self.judul_buku = judul_buku
        cur.execute(f"SELECT * FROM buku WHERE judul_buku LIKE '%{self.judul_buku}%'")
        data = cur.fetchall()
        if data != []:
            for i in data:
                print(f'ID          : {i[0]}')
                print(f'Judul       : {i[1]}')
                print(f'Pengarang   : {i[2]}')
                print(f'Status      : {i[3]}')

        else:
            print(Fore.RED + '\nData tidak ditemukan ' + Style.RESET_ALL)


    def hapus_buku(self,kode_buku):
        self.kode_buku = kode_buku
        cur.execute(f"SELECT * FROM buku WHERE kode_buku = '{self.kode_buku}'")
        if cur.fetchall() != []:
            cur.execute(f"DELETE FROM buku WHERE kode_buku = '{self.kode_buku}' ")
            db.commit()
            print(Fore.GREEN + '\nData Berhasil Dihapus '+ Style.RESET_ALL)
        else:
            print(Fore.RED + '\nData tidak ditemukan ' + Style.RESET_ALL)


class peminjam:
    def pinjam(self, kode_buku, nama_peminjam,judul_buku):
        self.kode_buku = kode_buku
        self.nama_peminjam = nama_peminjam
        self.judul_buku = judul_buku
        cur.execute(f"SELECT status FROM buku WHERE kode_buku = '{self.kode_buku}';")
        data = cur.fetchall()
        if data != []:
            if 'ada' == data[0][0]:
                cur.execute(f"UPDATE buku SET status='dipinjam' WHERE kode_buku = '{self.kode_buku}'")
                cur.execute(f"INSERT INTO peminjam(kode_buku,nama_peminjam,judul_buku,tanggal_pinjam) VALUES ('{self.kode_buku}','{self.nama_peminjam}','{self.judul_buku}','{datetime.now()}')")
                db.commit()
                print(Fore.GREEN + 'Buku Berhasil Dipinjam ' + Style.RESET_ALL)
            else:
                print(Fore.RED + '\nMaaf buku tersebut sedang dipinjam' + Style.RESET_ALL)
        else:
            print(Fore.RED + '\nData buku tidak ditemukan' + Style.RESET_ALL)

    def kembali(self, kode_buku, id_peminjam):
        self.kode_buku = kode_buku
        self.id_peminjam = id_peminjam

        cur.execute(f"SELECT * FROM peminjam WHERE id_peminjam = {self.id_peminjam} AND kode_buku = {self.kode_buku} ")
        if cur.fetchall() != []:
            cur.execute(f"UPDATE buku SET status='ada' WHERE kode_buku = '{self.kode_buku}'")
            cur.execute(f"DELETE FROM peminjam WHERE id_peminjam = {self.id_peminjam} AND kode_buku = {self.kode_buku}")
            db.commit()
            print(Fore.GREEN + '\nBuku Berhasil Dikembalikan ' + Style.RESET_ALL)
        else:
            print(Fore.RED + "\ndata tidak ditemukan"+ Style.RESET_ALL)

    def tampilkan_peminjam(self):
        cur.execute(f"SELECT * FROM peminjam;")
        data = cur.fetchall()
        for i in data:
            print('')
            print(f'id peminjaman      : {i[0]}')
            print(f'Kode buku          : {i[1]}')
            print(f'Nama peminjam      : {i[2]}')
            print(f'Judul Buku         : {i[3]}')
            print(f'tanggal pinjam     : {i[4]}')
            print('-'*50)


s = Sistem_peminjaman_buku()
p = peminjam()

while True:
    os.system('cls')
    print(Fore.WHITE+'---- SELAMAT DATANG DI SISTEM PEMINJAMAN BUKU ----'+ Style.RESET_ALL)
    print('1.', Fore.BLUE +' Tambah data buku'+ Style.RESET_ALL)
    print('2.',Fore.RED + ' Hapus buku'+ Style.RESET_ALL)
    print('3.',Fore.GREEN + ' Tampil semua data buku'+ Style.RESET_ALL)
    print('4.', Fore.GREEN +' Tampil semua data peminjam'+ Style.RESET_ALL)
    print('5.',Fore.MAGENTA +' Cari buku'+ Style.RESET_ALL)
    print('6.',Fore.YELLOW +' Pinjam Buku'+ Style.RESET_ALL)
    print('7.',Fore.CYAN + ' Kembalikan Buku'+ Style.RESET_ALL)
    print('8.',Fore.RESET +' Exit'+ Style.RESET_ALL)
    menu = input('\nPilih salah satu Menu : ')
    if menu == '1':
        os.system('cls')
        kode = int(input(' Masukan ID Buku : '))
        judul = input(' Masukan Judul Buku : ')
        penulis = input(' Masukan penulis : ')
        penerbit = input(' Masukan penerbit Buku  : ')
        tahun = input(' Masukan tahun Buku : ')
        s.tambah_buku(kode, judul, penulis, penerbit,tahun)
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '2':
        os.system('cls')
        idBuku = int(input('Masukan ID Buku : '))
        s.hapus_buku(idBuku)
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '3':
        os.system('cls')
        print('='*19,'Data Buku','='*19)
        s.tampilkan_buku()
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '4':
        os.system('cls')
        print('='*17, 'Data Peminjam', '='*17 )
        p.tampilkan_peminjam()
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '5':
        os.system('cls')
        judul = input('Masukan Judul : ')
        print('='*20, 'Data Buku', '='*20)
        s.cari_buku(judul)
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '6':
        os.system('cls')
        kode = int(input('Masukan kode Buku : '))
        nama = input('Masukan nama: ')
        judul_buku = input('Masukan judul buku : ')
        p.pinjam(kode, nama, judul_buku)
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '7':
        os.system('cls')
        id_peminjam = int(input('Masukan id peminjam: '))
        kode_buku = int(input('Masukan kode buku : '))
        p.kembali(kode_buku,id_peminjam)
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')

    elif menu == '8':
        exit()
    else:
        print(Fore.RED + '\nMaaf Pilihan Menu Tidak Tersedia' + Style.RESET_ALL)
        input(Fore.YELLOW +'\nTekan Enter Untuk Melanjutkan.....')