from calendar import c
from turtle import color
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import E
from cv2 import CAP_PROP_XI_COUNTER_SELECTOR
from numpy import double
import pyodbc
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout
#Conexion================================================================================
server="localhost"
dbs="dbDragonBar"
user="juliop"
passw="1234"
iid={}
try:
    con=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server};SERVER='+server+';DATABASE='+dbs+';UID='+user+';PWD='+passw)
except Exception as e:
    print("Ocurrio un error al conectar con SQL Server: ",e)
#Login de Empleados======================================================================
class login(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("login.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_ing.clicked.connect(self.conectar)
    def conectar(self):
        with con.cursor() as cursor:
            consul=("select iId_emp,vcont from empleados where iId_emp=? and vcont=?")
            nombre=str(self.text_cod.text())
            iid[0]=nombre
            cont=str(self.text_cont.text())
            cursor.execute(consul,(nombre,cont))
            resulta=cursor.fetchall()
            if resulta:
                self.maiin=Cuerpo()
                self.maiin.show()
                self.close()
            else:
                self.text_cont.clear()
                self.text_cod.clear()
                self.text_adv.setHidden(False)
                self.text_img.setHidden(False)                
#Cuerpo o main del programa================================================================
class Cuerpo(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("main.ui",self)
        #Boton producto
        self.boton_productos.clicked.connect(self.conectar_prod)
        self.boton_cerrar.clicked.connect(self.salir)
        self.boton_ventas.clicked.connect(self.conectar_ventas)
        self.boton_est.clicked.connect(self.conectar_estadis)
        self.boton_clientes.clicked.connect(self.conectar_clientes)
        self.boton_emp.clicked.connect(self.conectar_emp)
        self.boton_prov.clicked.connect(self.conectar_prov)
    #Funcion del boton Proveedores
    def conectar_prov(self):
        self.prov=Proveedores()
        self.prov.show()
    #Funcion del boton empleados
    def conectar_emp(self):
        self.empl=empleados()
        self.empl.show()
    #Funcion del boton ventas
    def conectar_ventas(self):
        self.ventass=ventas()
        self.ventass.show()
    #Funcion del boton producto
    def conectar_prod(self):
        self.prodc=prod()
        self.prodc.show()
    #Funcion del boton estadisticas
    def conectar_estadis(self):
        self.estas=estadis()
        self.estas.show()
    #Funcion del boton cerrar
    def salir(self):
        self.close()
        self.log=login()
        self.log.show()
    #Funcion del boton clientes
    def conectar_clientes(self): 
        self.cli=clientes()
        self.cli.show()
#Clase producto===========================================================================
class prod(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("opc_prod.ui",self)
        self.btn_add.clicked.connect(self.secur)
        self.btn_view.clicked.connect(self.view_prod)
    def secur(self):
        self.serc=Adv()
        self.serc.show()
        self.close()
    def view_prod(self):
        self.vieww=view_prod()
        self.vieww.show()
        self.close()
#Add Prod
class Add_prod(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("add_prod.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        try:
            with con.cursor() as cursor:
                resultt=cursor.execute("select iId_Prov from proveedores")
                for row_number, row_data in enumerate(resultt):
                    for column_number, data in enumerate(row_data):
                        self.text_idprov.addItem(str(data))
        except Exception as e:
            print("Error",e)
        self.btn_accep.clicked.connect(self.save)
        self.btn_addprov.clicked.connect(self.add_pprov)
    def save(self):
        try:
            with con.cursor() as cursor:
                to_ven=0
                cursor.execute("insert into productos (vnombre,vcosto,vcant_exis,vtipo,iId_Prov,itotal_ven) values(?,?,?,?,?,?)",self.text_prod.text(),self.text_costo.text(),self.text_total.text(),self.text_tipo.currentText(),self.text_idprov.currentText(),to_ven)
            self.text_adv.setHidden(False)
            self.text_img.setHidden(False)
            self.btn_accep.setEnabled(False)
        except Exception as e:
            print("Error",e)
    def add_pprov(self):
        self.add=Adv_prov()
        self.add.show()
        self.close()      
#View Prod
class view_prod(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("view_prod.ui",self)
        self.btn_delete.setHidden(True)
        self.btn_update.setHidden(True)
        self.btn_buscar.clicked.connect(self.buscar_prod)
        self.btn_delete.clicked.connect(self.delete_prod)
        self.btn_update.clicked.connect(self.update_prodc)
        try:
            with con.cursor() as cursor:
                comand="select * from productos"
                resultt=cursor.execute(comand)
                self.table_prod.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_prod.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_prod.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
    def buscar_prod(self):
        self.btn_delete.setHidden(False)
        self.btn_update.setHidden(False)
        self.table_prod.clearContents()
        try:
            with con.cursor() as cursor:
                comand="select * from productos where iId_prod=?"
                contra=int(self.text_buscar.text())
                resultt=cursor.execute(comand,[contra])
                self.table_prod.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_prod.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_prod.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                iid[1]=str(contra)
        except Exception as e:
            print(e)
    def delete_prod(self):
        try:
            with con.cursor() as cursor:
                comand="delete from productos where iId_Prod=?"
                contra=int(self.text_buscar.text())
                comand2="select * from productos"
                cursor.execute(comand,[contra])
                resultado=cursor.execute(comand2)
                self.table_prod.setRowCount(0)
                for row_number, row_data in enumerate(resultado):
                    self.table_prod.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_prod.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
        self.text_buscar.clear()
    def update_prodc(self):
        self.up=update_prod()
        self.up.show()
        self.close()
#update productos
class update_prod(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("update_prod.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_accep.clicked.connect(self.update)
        try:
            with con.cursor() as cursor:
                self.text_idprod.setText(iid[1])
                #consulta 1=========================================
                prov="select iId_Prov from productos where iId_Prod=?"
                id_prov=int(self.text_idprod.text())
                resultado=cursor.execute(prov,[id_prov])
                self.text_idprov.addItem(str(resultado.fetchone()[0]))
                #consulta 2=========================================
                vnombre="select vnombre from productos where iId_Prod=?"
                nombre=int(self.text_idprod.text())
                resultado=cursor.execute(vnombre,[nombre])
                self.text_prod.setText(str(resultado.fetchone()[0]))
                #consulta 3=========================================
                vcosto="select vcosto from productos where iId_Prod=?"
                costo=int(self.text_idprod.text())
                resultado=cursor.execute(vcosto,[costo])
                self.text_costo.setText(str(resultado.fetchone()[0]))
                #consulta 4=========================================
                vcan="select vcant_exis from productos where iId_Prod=?"
                cantidad=int(self.text_idprod.text())
                resultado=cursor.execute(vcan,[cantidad])
                self.text_total.setText(str(resultado.fetchone()[0]))
                #consulta 5=========================================
                vtipo="select vtipo from productos where iId_Prod=?"
                tipo=int(self.text_idprod.text())
                resultado=cursor.execute(vtipo,[tipo])
                self.text_tipo.addItem(str(resultado.fetchone()[0]))

        except Exception as e:
            print(e)
    def update(self):
        try:
            #update=========================================
            with con.cursor() as cursor:
                upda="update productos set iId_prov=?,vnombre=?,vcosto=?,vcant_exis=?,vtipo=? where iId_Prod=?"
                iId_prov=int(self.text_idprov.currentText())
                iId_prod=int(self.text_idprod.text())
                vnom=str(self.text_prod.text())
                vcosto=str(self.text_costo.text())
                vcan_exis=str(self.text_total.text())
                vtipo=str(self.text_tipo.currentText())
                cursor.execute(upda,[iId_prov,vnom,vcosto,vcan_exis,vtipo,iId_prod])
                self.text_adv.setHidden(False)
                self.text_img.setHidden(False)
                self.btn_accep.setEnabled(False)
        except Exception as e:
            print(e)
        
#Advertencia 
class Adv_vemp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("advertencia.ui",self)        
        self.btn_aceppt.clicked.connect(self.add_emp)
    def add_emp(self):
        with con.cursor() as cursor:
            consul=("select iId_emp,vcont from empleados where iId_emp=1001 and vcont=?")
            contra=str(self.text_cont.text())
            cursor.execute(consul,(contra))
            resulta=cursor.fetchall()
            if resulta:
                self.add=view_empleados()
                self.add.show()
                self.close()
            else:
                self.close()
                print("error")  
#Advertencia 
class Adv(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("advertencia.ui",self)        
        self.btn_aceppt.clicked.connect(self.add_prod)
    def add_prod(self):
        nombre=iid[0]
        with con.cursor() as cursor:
            consul=("select iId_emp,vcont from empleados where iId_emp=1001 and vcont=?")
            contra=str(self.text_cont.text())
            cursor.execute(consul,(contra))
            resulta=cursor.fetchall()
            if resulta:
                self.add=Add_prod()
                self.add.show()
                self.close()
            else:
                self.close()
                print("error")
#Advertencia 
class Adv_emp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("advertencia.ui",self)        
        self.btn_aceppt.clicked.connect(self.add_emp)
    def add_emp(self):
        with con.cursor() as cursor:
            consul=("select iId_emp,vcont from empleados where iId_emp=1001 and vcont=?")
            contra=str(self.text_cont.text())
            cursor.execute(consul,(contra))
            resulta=cursor.fetchall()
            if resulta:
                self.add=Add_empleados()
                self.add.show()
                self.close()
            else:
                self.close()
                print("error")
#Advertencia 
class Adv_prov(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("advertencia.ui",self)        
        self.btn_aceppt.clicked.connect(self.add_prov)
    def add_prov(self):
        with con.cursor() as cursor:
            consul=("select iId_emp,vcont from empleados where iId_emp=1001 and vcont=?")
            contra=str(self.text_cont.text())
            cursor.execute(consul,(contra))
            resulta=cursor.fetchall()
            if resulta:
                self.add=Add_proveedores()
                self.add.show()
                self.close()
            else:
                self.close()
                print("error")
#Clase ventas===============================================================================
class ventas(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("opc_ventas.ui",self)
        self.btn_add.clicked.connect(self.new_sale)
        self.btn_view.clicked.connect(self.view_sale)
    def new_sale(self):
        self.new=new_salee()
        self.new.show()
        self.close()
    def view_sale(self):
        self.view=view_salee()
        self.view.show()
        self.close()
#new sale
class new_salee(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("add_venta.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_accep.clicked.connect(self.calcular)
        try:
            with con.cursor() as cursor:
                #Cargar productos
                resultado=cursor.execute("select iId_Prod from productos")
                for row_numbe, row_dat in enumerate(resultado):
                    for column_number, dat in enumerate(row_dat):
                        self.text_cod.addItem(str(dat))
                #Cargar membresias
                resultt=cursor.execute("select vtipo_mem from membresias")
                for row_number, row_data in enumerate(resultt):
                    for column_number, data in enumerate(row_data):
                        self.text_mem.addItem(str(data))
        except Exception as e:
            print("Error",e)
    def calcular(self):
        try:
            with con.cursor() as cursor:
                #Costo de la tabla productos====================================
                consul=("select vcosto from productos where iId_Prod=?")
                contra=str(self.text_cod.currentText())
                precio=cursor.execute(consul,(contra))
                self.lbl_prec.setText(str(precio.fetchone()[0]))
                pre=int(self.lbl_prec.text())
                #Cantidad======================================================
                can=int(self.text_can.text())
                #Membresia======================================================
                consu=("select vdescuento from membresias where vtipo_mem=?")
                cont=str(self.text_mem.currentText())
                vcosto=cursor.execute(consu,(cont))
                self.lbl_desc.setText(str(vcosto.fetchone()[0]))
                costo=int(self.lbl_desc.text())
                #Operacion=======================================================
                sub=pre*can
                self.lbl_sub.setText(str(sub))
                vdes=costo/100
                des=sub*vdes
                p=sub-des
                self.lbl_total.setText(str(p))
                #Id descuento==================================================== 
                consult=("select iId_membresia from membresias where vtipo_mem=?")
                contt=str(self.text_mem.currentText())
                viid=cursor.execute(consult,(contt))
                idd=str(viid.fetchone()[0])
                #Cant existencia===================================================
                consultar=("select vcant_exis from productos where iId_Prod=?")
                cantidad=int(self.text_cod.currentText())
                totalprod=cursor.execute(consultar,(cantidad))
                exis=int(totalprod.fetchone()[0])
                ife=exis-can
                if ife < 0:
                    self.close()
                else:
                    vcant=str(ife)
                    idprod=int(self.text_cod.currentText())
                    #Add cant vendida===================================================
                    addv=("select itotal_ven from productos where iId_Prod=?")
                    cant_v=cursor.execute(addv,(idprod))
                    cantv=int(cant_v.fetchone()[0])+can
                    upd_cantv=("update productos set itotal_ven=? where iId_Prod=?")
                    cursor.execute(upd_cantv,(cantv,idprod))
                    #Update=============================================================
                    update=("update productos set vcant_exis=? where iId_Prod=?")
                    cursor.execute(update,(vcant,idprod))
                    #Save=============================================================
                    fecha=str(datetime.today().strftime('%Y-%m-%d'))
                    cursor.execute("insert into factura (iId_Prod,vcosto,vcan_comp,iId_mem,vfecha,vtotal,iId_Emp) values(?,?,?,?,?,?,?)",int(self.text_cod.currentText()),str(pre),str(can),int(idd),fecha,str(p),int(iid[0]))
                    self.text_adv.setHidden(False)
                    self.text_img.setHidden(False)
                    self.btn_accep.setEnabled(False)
        except Exception as e:
            print(e)    
#view sale
class view_salee(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("view_venta.ui",self)
        self.btn_delete.setHidden(True)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_delete.clicked.connect(self.delete)
        try:
            with con.cursor() as cursor:
                comand="select * from factura"
                resultt=cursor.execute(comand)
                self.table_venta.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_venta.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_venta.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
    def buscar(self):
        self.btn_delete.setHidden(False)
        self.table_venta.clearContents()
        try:
            with con.cursor() as cursor:
                comand="select * from factura where iId_fac=?"
                contra=int(self.text_venta.text())
                resultt=cursor.execute(comand,[contra])
                self.table_venta.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_venta.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_venta.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
    def delete(self):
        try:
            with con.cursor() as cursor:
                comand="delete from factura where iId_fac=?"
                contra=int(self.text_venta.text())
                comand2="select * from factura"
                cursor.execute(comand,[contra])
                resultado=cursor.execute(comand2)
                self.table_venta.setRowCount(0)
                for row_number, row_data in enumerate(resultado):
                    self.table_venta.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_venta.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
        self.text_venta.clear()
#Clase estadisticas===============================================================================
class estadis(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("statistics.ui",self)
        self.btn_accep.clicked.connect(self.graf)
        try:
            with con.cursor() as cursor:
                comand="SELECT TOP 10 vnombre,itotal_ven,vcosto FROM productos order by itotal_ven desc"
                resultt=cursor.execute(comand)
                self.table_sts.setRowCount(0)
                datos={}
                i=0
                for row_number, row_data in enumerate(resultt):
                    self.table_sts.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_sts.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                        datos[i]=str(data)
                        i=i+1
                ntop1=datos[0]
                ntop2=datos[3]
                ntop3=datos[6]
                ntop4=datos[9]
                ntop5=datos[12]
                ntop6=datos[15]
                ntop7=datos[18]
                ntop8=datos[21]
                ntop9=datos[24]
                ntop10=datos[27]
                top1=datos[1]
                top2=datos[4]
                top3=datos[7]
                top4=datos[10]
                top5=datos[13]
                top6=datos[16]
                top7=datos[19]
                top8=datos[22]
                top9=datos[25]
                top10=datos[28]
                eje_x=[ntop10,ntop9,ntop8,ntop7,ntop6,ntop5,ntop4,ntop3,ntop2,ntop1]
                eje_y=[top10,top9,top8,top7,top6,top5,top4,top3,top2,top1]
                plt.title("Top 10 mejores vendidos")
                plt.bar(eje_x, height=eje_y,color="blue",width=0.5)   
        except Exception as e:
            print(e) 
    def graf(self):
        plt.show()
#Clase clientes===============================================================================
class clientes(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("clientes.ui",self)
        self.btn_delete.setHidden(True)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_delete.clicked.connect(self.delete)
        try:
            with con.cursor() as cursor:
                comand="select * from clientes"
                resultt=cursor.execute(comand)
                self.table_cli.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_cli.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_cli.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e) 
    def buscar(self):
        self.btn_delete.setHidden(False)
        self.table_cli.clearContents()
        try:
            with con.cursor() as cursor:
                comand="select * from clientes where iId_cliente=?"
                contra=int(self.text_emp.text())
                resultt=cursor.execute(comand,[contra])
                self.table_cli.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_cli.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_cli.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
    def delete(self):
        try:
            with con.cursor() as cursor:
                comand="delete from clientes where iId_cliente=?"
                contra=int(self.text_emp.text())
                comand2="select * from clientes"
                cursor.execute(comand,[contra])
                resultado=cursor.execute(comand2)
                self.table_cli.setRowCount(0)
                for row_number, row_data in enumerate(resultado):
                    self.table_cli.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_cli.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
        self.text_emp.clear()
#Clase empleados===============================================================================
class empleados(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("opc_empleados.ui",self)
        self.btn_add.clicked.connect(self.add_emp)
        self.btn_view.clicked.connect(self.view_emp)
    def add_emp(self):
        self.adve=Adv_emp()
        self.adve.show()
        self.close()
    def view_emp(self):
        self.view=Adv_vemp()
        self.view.show()
        self.close()
#view Empleados
class view_empleados(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("view_Emp.ui",self)
        self.btn_delete.setHidden(True)
        self.btn_update.setHidden(True)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_update.clicked.connect(self.update_emp)
        try:
            with con.cursor() as cursor:
                comand="select * from empleados"
                resultt=cursor.execute(comand)
                self.table_Emp.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_Emp.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_Emp.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
    def buscar(self):
        self.btn_delete.setHidden(False)
        self.btn_update.setHidden(False)
        self.table_Emp.clearContents()
        try:
            with con.cursor() as cursor:
                comand="select * from empleados where iId_emp=?"
                contra=int(self.text_emp.text())
                resultt=cursor.execute(comand,[contra])
                self.table_Emp.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_Emp.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_Emp.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                iid[2]=str(contra)
        except Exception as e:
            print(e)
    def delete(self):
        try:
            with con.cursor() as cursor:
                comand="delete from empleados where iId_emp=?"
                contra=int(self.text_emp.text())
                comand2="select * from empleados"
                cursor.execute(comand,[contra])
                resultado=cursor.execute(comand2)
                self.table_Emp.setRowCount(0)
                for row_number, row_data in enumerate(resultado):
                    self.table_Emp.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_Emp.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
        self.text_emp.clear()
    def update_emp(self):
        self.up=update_emp()
        self.up.show()
        self.close()
#update Empleados
class update_emp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("update_Emp.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_accep.clicked.connect(self.update)
        try:
            with con.cursor() as cursor:
                self.text_cod.setText(iid[2])
                #consulta 1=========================================
                vpue="select iId_pues from empleados where iId_emp=?"
                pue=int(self.text_cod.text())
                resultado=cursor.execute(vpue,[pue])
                self.text_pues.setText(str(resultado.fetchone()[0]))
                #consulta 2=========================================
                vnombre="select vnombre from empleados where iId_emp=?"
                nombre=int(self.text_cod.text())
                resultado=cursor.execute(vnombre,[nombre])
                self.text_nom.setText(str(resultado.fetchone()[0]))
                #consulta 3=========================================
                vpat="select vap_pat from empleados where iId_emp=?"
                pat=int(self.text_cod.text())
                resultado=cursor.execute(vpat,[pat])
                self.text_pat.setText(str(resultado.fetchone()[0]))
                #consulta 4=========================================
                vmat="select vap_mat from empleados where iId_emp=?"
                mat=int(self.text_cod.text())
                resultado=cursor.execute(vmat,[mat])
                self.text_mat.setText(str(resultado.fetchone()[0]))
                #consulta 5=========================================
                vtel="select vtel from empleados where iId_emp=?"
                tel=int(self.text_cod.text())
                resultado=cursor.execute(vtel,[tel])
                self.text_tel.setText(str(resultado.fetchone()[0]))
                #consulta 6=========================================
                vcont="select vcont from empleados where iId_emp=?"
                cont=int(self.text_cod.text())
                resultado=cursor.execute(vcont,[cont])
                self.text_cont.setText(str(resultado.fetchone()[0]))
        except Exception as e:
            print(e)
    def update(self):
        try:
            #update=========================================
            with con.cursor() as cursor:
                upda="update empleados set iId_pues=?,vnombre=?,vap_pat=?,vap_mat=?,vtel=?,vcont=? where iId_emp=?"
                iId_emp=int(self.text_cod.text())
                iId_pues=int(self.text_pues.text())
                vnom=str(self.text_nom.text())
                vap_pat=str(self.text_pat.text())
                vap_mat=str(self.text_mat.text())
                vtel=str(self.text_tel.text())
                vcont=str(self.text_cont.text())
                cursor.execute(upda,[iId_pues,vnom,vap_pat,vap_mat,vtel,vcont,iId_emp])
                self.text_adv.setHidden(False)
                self.text_img.setHidden(False)
                self.btn_accep.setEnabled(False)
        except Exception as e:
            print(e)
#Add Empleados
class Add_empleados(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("add_Emp.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_accep.clicked.connect(self.add_empl)
    def add_empl(self):
        try:
            with con.cursor() as cursor:
                cursor.execute("insert into empleados (iId_emp,iId_pues,vnombre,vap_pat,vap_mat,vtel,vcont) values(?,?,?,?,?,?,?)",self.text_cod.text(),self.text_pues.text(),self.text_nom.text(),self.text_pat.text(),self.text_mat.text(),self.text_tel.text(),self.text_cont.text())
            self.text_adv.setHidden(False)
            self.text_img.setHidden(False)
            self.btn_accep.setEnabled(False)
        except Exception as e:
            print("Error",e)
#Clase Proveedores===============================================================================
class Proveedores(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("opc_provee.ui",self)
        self.btn_add.clicked.connect(self.add_prov)
        self.btn_view.clicked.connect(self.view_prov)
    def add_prov(self):
        self.adve=Adv_prov()
        self.adve.show()
        self.close()
    def view_prov(self):
        self.view=view_prov()
        self.view.show()
        self.close()
#Add Proveedores
class Add_proveedores(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("add_prov.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_accep.clicked.connect(self.add_prov)
    def add_prov(self):
        try:
            with con.cursor() as cursor:
                cursor.execute("insert into proveedores (Vnom,Vtel) values(?,?)",self.text_nom.text(),self.text_tel.text())
            self.text_adv.setHidden(False)
            self.text_img.setHidden(False)
            self.btn_accep.setEnabled(False)
        except Exception as e:
            print("Error",e)
#view Proveedores
class view_prov(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("view_Prov.ui",self)
        self.btn_delete.setHidden(True)
        self.btn_update.setHidden(True)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_update.clicked.connect(self.update_prov)
        try:
            with con.cursor() as cursor:
                comand="select * from proveedores"
                resultt=cursor.execute(comand)
                self.table_prov.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_prov.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_prov.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)   
    def buscar(self):
        self.btn_delete.setHidden(False)
        self.btn_update.setHidden(False)
        self.table_prov.clearContents()
        try:
            with con.cursor() as cursor:
                comand="select * from proveedores where iId_Prov=?"
                contra=int(self.text_prov.text())
                resultt=cursor.execute(comand,[contra])
                self.table_prov.setRowCount(0)
                for row_number, row_data in enumerate(resultt):
                    self.table_prov.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_prov.setItem(row_number,column_number, QTableWidgetItem(str(data)))
                iid[3]=str(contra)
        except Exception as e:
            print(e)
    def delete(self):
        try:
            with con.cursor() as cursor:
                comand="delete from proveedores where iId_Prov=?"
                contra=int(self.text_prov.text())
                comand2="select * from proveedores"
                cursor.execute(comand,[contra])
                resultado=cursor.execute(comand2)
                self.table_prov.setRowCount(0)
                for row_number, row_data in enumerate(resultado):
                    self.table_prov.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.table_prov.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(e)
        self.text_prov.clear()
    def update_prov(self):
        self.up=update_prov()
        self.up.show()
        self.close()
#update Proveedores
class update_prov(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("update_prov.ui",self)
        self.text_adv.setHidden(True)
        self.text_img.setHidden(True)
        self.btn_accep.clicked.connect(self.update)
        try:
            with con.cursor() as cursor:
                self.text_cod.setText(iid[3])
                #consulta 1=========================================
                vnom="select Vnom from proveedores where iId_Prov=?"
                nom=int(self.text_cod.text())
                resultado=cursor.execute(vnom,[nom])
                self.text_nom.setText(str(resultado.fetchone()[0]))
                #consulta 2=========================================
                vtel="select Vtel from proveedores where iId_Prov=?"
                tel=int(self.text_cod.text())
                resultado=cursor.execute(vtel,[tel])
                self.text_tel.setText(str(resultado.fetchone()[0]))
        except Exception as e:
            print(e)
    def update(self):
        try:
            #update=========================================
            with con.cursor() as cursor:
                upda="update proveedores set Vnom=?,Vtel=? where iId_Prov=?"
                iId_Prov=int(self.text_cod.text())
                vnom=str(self.text_nom.text())
                vtel=str(self.text_tel.text())
                cursor.execute(upda,[vnom,vtel,iId_Prov])
                self.text_adv.setHidden(False)
                self.text_img.setHidden(False)
                self.btn_accep.setEnabled(False)
        except Exception as e:
            print(e)        
#=============================================================================================
#Ejecucion del programa 
def mainy():
    app=QApplication(sys.argv)
    principal=login()
    principal.show()
    app.exec_() 
if __name__=="__main__":
    mainy()