# -*- coding: utf-8 -*-
"""
/***************************************************************************
 testecm
                                 A QGIS plugin
 testecm
                              -------------------
        begin                : 2016-01-15
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Lidia
        email                : lidiakonno@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from testecm_dialog import testecmDialog
from testecm_dialog2 import testecmDialog2
from testecm_dialog3 import testecmDialog3
from testecm_dialog4 import testecmDialog4
import os.path
import psycopg2
import os
from time import sleep
import csv


class testecm:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

		
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'testecm_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = testecmDialog()
        self.dlg2 = testecmDialog2()
        self.dlg3 = testecmDialog3()
        self.dlg4 = testecmDialog4()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&testecm')
        # TODO: We are going to let the user set this up in a future iteration


#----------------------------------------------------------------------------------------------

  

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('testecm', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.toolbar = self.iface.addToolBar(u'testecm')
        self.toolbar.setObjectName(u'testecm')

        icon_path = ':/plugins/testecm/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'criar projeto_'),
            callback=self.run,
            parent=self.iface.mainWindow())

        icon_path1 = ':/plugins/testecm/icon1.png'
        self.add_action(
            icon_path1,
            text=self.tr(u'exporta'),
            callback=self.run2,
            parent=self.iface.mainWindow())

        icon_path2 = ':/plugins/testecm/icon2.png'
        self.add_action(
            icon_path2,
            text=self.tr(u'importar'),
            callback=self.run3,
            parent=self.iface.mainWindow())

        icon_path3 = ':/plugins/testecm/icon3.png'
        self.add_action(
            icon_path3,
            text=self.tr(u'visualizar'),
            callback=self.run4,
            parent=self.iface.mainWindow())
        
#----------------# add Pushbutton  ---------------~##
        self.dlg.Button_add_obra.clicked.connect(self.add_obra_clicked_r)  
        self.dlg.Button_add_lo_r.clicked.connect(self.add_lotes_clicked_r)     
    
        self.dlg.Button_add_obra_l.clicked.connect(self.add_obra_clicked_lin)          
        self.dlg.Button_add_lot_l.clicked.connect(self.add_lotes_clicked_lin) 
        
        self.dlg2.Button_selec_o.clicked.connect(self.table) 
        self.dlg2.pushButton.clicked.connect(self.select_output_file)
        self.dlg2.Button_salvar.clicked.connect(self.salvar)

        self.dlg3.pushButton_2.clicked.connect(self.select_input_file)
        self.dlg3.Button_salvar_2.clicked.connect(self.salvar_2)

        self.dlg4.Button_show_proc_r.clicked.connect(self.visu_proc_r)
        self.dlg4.Button_show_proc_l.clicked.connect(self.visu_proc_lin)
        self.dlg4.Button_show_fim_r.clicked.connect(self.visu_fim_r)
        self.dlg4.Button_show_fim_l.clicked.connect(self.visu_fim_l)
#-------------------------------------------------------------------------------------

## Lista de comboBox 
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        cur.execute("""SELECT nome FROM tipo_obra_radial """)
        rows = cur.fetchall()
        self.dlg.Cbx_tipo_o_r.clear()
        for row in rows:      
            self.dlg.Cbx_tipo_o_r.addItem(row[0])


        cur.execute("""SELECT nome FROM tipo_obra_linear """)
        rows = cur.fetchall()
        self.dlg.Cbx_tipo_o_l.clear()
        for row in rows:      
            self.dlg.Cbx_tipo_o_l.addItem(row[0])

#--------------------------------------------------------------            
        cur.close()
        conn.close()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&testecm'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):

        # alimentando combobox

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()

        cur.execute("""SELECT obra.nome FROM obra, obra_l WHERE obra.id_obra not in (SELECT lotes_benef.id_obra FROM lotes_benef) AND obra.id_obra=obra_l.id_obra """ )
        self.dlg.Cbx_sel_o_l.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg.Cbx_sel_o_l.addItem(nome[0]) 


#--------------------------------------------------------------            

        cur.execute("""SELECT obra.nome FROM obra, obra_r WHERE obra.id_obra not in (SELECT lotes_benef.id_obra FROM lotes_benef) AND obra.id_obra=obra_r.id_obra """ )
        self.dlg.Cbx_sel_o_r.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg.Cbx_sel_o_r.addItem(nome[0])    

#------------------------------------------------------------------------------------------
        #conn.commit()
        cur.close()
        conn.close()
        
        
        """Run method that performs all the real work"""
        ## nomes dos layers 
        layers1 = QgsMapLayerRegistry.instance().mapLayers().values()

        for layer in layers1:
            if layer.name() == 'limite_municipal':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'perimetro_urbano':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'limite_bairros':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'arruamento':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'quadras':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'lotes':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'curso_agua':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        ## conectando com o banco

        
        # add layers para a PRIMEIRA visualizacao
        #conectando com o banco
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")
        
        # limite municipal
        uri.setDataSource("pe", "lpal_municipio_a", "geom")
        layer_base1 = QgsVectorLayer(uri.uri(), "limite_municipal", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base1.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base1)

        #perimetro urbano
        uri.setDataSource("ge", "cb_area_urbana_isolada_a", "geom")
        layer_base2 = QgsVectorLayer(uri.uri(), "perimetro_urbano", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base2.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base2)

        # limite dos bairros
        uri.setDataSource("pe", "lpal_distrito_a", "geom")
        layer_base3 = QgsVectorLayer(uri.uri(), "limite_bairros", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base3.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base3)
        
        #arruamento
        uri.setDataSource("ge", "cb_trecho_arruamento_l", "geom")
        layer_base4 = QgsVectorLayer(uri.uri(), "arruamento", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base4.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base4)

        #quadras
        uri.setDataSource("ge", "cb_quadra_a", "geom")
        layer_base5 = QgsVectorLayer(uri.uri(False), "quadras", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base5.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base5)

        #lotes
        uri.setDataSource("pe", "lpal_area_construida_a", "geom")
        layer_base6 = QgsVectorLayer(uri.uri(), "lotes", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base6.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base6)

        #Curso d agua
        uri.setDataSource("pe", "hid_trecho_drenagem_l", "geom")
        layer_base7 = QgsVectorLayer(uri.uri(), "curso_agua", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base7.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base7)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        #conn.commit()
        cur.close()
        conn.close()




        result = self.dlg.exec_()
        # See if OK was pressed
#----------------------------

            
        if result == 1:
            pass
    def add_obra_clicked_r(self):
## inseri informações da obra no BDG 

        ## adicionando 
        add_nm_obra = self.dlg.line_nm_obra.text() # nome da obra
        add_custo = self.dlg.line_custo.text() # custo da obra
        add_tipo_obraR = self.dlg.Cbx_tipo_o_r.currentText() # tipo da obra
        add_nm_rua = self.dlg.line_nm_log.text() # nome da rua


        ## conectando com o BD
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        
       
        cur.execute("INSERT INTO obra (nome, custo, tipo_obra, log_endereco) VALUES (%s,%s,  %s, %s);", [add_nm_obra, add_custo, add_tipo_obraR, add_nm_rua])

        # mostrando a rua selecionada
        cur.execute("""CREATE OR REPLACE VIEW rua_selec AS
        SELECT ge.cb_trecho_arruamento_l.id, ge.cb_trecho_arruamento_l.nome, ge.cb_trecho_arruamento_l.geom 
        FROM ge.cb_trecho_arruamento_l 
        WHERE ge.cb_trecho_arruamento_l.nome='%s'""" % add_nm_rua)


        conn.commit()
        cur.close()
        conn.close()


        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")

        uri.setDataSource("public", "rua_selec", "geom", " ", "id")
        layer_base8 = QgsVectorLayer(uri.uri(False), "rua_selecionada", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base8)

        # zoom na rua selecionada

        canvas=self.iface.mapCanvas()
        extent=layer_base8.extent
        canvas.setExtent(extent())

        # mostrando o layer obra

        uri.setDataSource("public", "obra_r", "geom")
        layer_base9 = QgsVectorLayer(uri.uri(), "obra", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(layer_base9)

            # Do something useful here - delete the line containing pass and
            # substitute with your code.

    #    conn.commit()
        cur.close()
        conn.close()


        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()

        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[add_nm_obra])

        for row in cur.fetchall():
            valor = row[0]

        QMessageBox.information(QWidget(), "Inserir Obra "," Copie o Id da obra: %s" %valor, QMessageBox.Close)

        conn.commit()
        cur.close()
        conn.close()

        self.dlg.close()
        self.dlg.line_nm_obra.clear()
        self.dlg.line_custo.clear()
        self.dlg.line_nm_log.clear()
            

    def add_obra_clicked_lin(self):
## inseri informações da obra no BDG 

         ## conectando com o BD
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        ## adicionando
        add_nm_obra_l = self.dlg.line_nm_obra_l.text() # nome da obra
        add_custo_l = self.dlg.line_custo_l.text() # custo da obra
        add_tipo_obraL = self.dlg.Cbx_tipo_o_l.currentText() # tipo da obra
        add_nm_rua_l = self.dlg.line_nm_log_l.text() # nome da rua
          
        # consulta rua selecionada
        cur.execute("INSERT INTO obra (nome, custo, tipo_obra, log_endereco) VALUES (%s, %s, %s, %s);", [add_nm_obra_l, add_custo_l, add_tipo_obraL, add_nm_rua_l])
        cur.execute("""CREATE OR REPLACE VIEW rua_selec AS
        SELECT ge.cb_trecho_arruamento_l.id, ge.cb_trecho_arruamento_l.nome, ge.cb_trecho_arruamento_l.geom 
        FROM ge.cb_trecho_arruamento_l 
        WHERE ge.cb_trecho_arruamento_l.nome='%s'""" % add_nm_rua_l)
        # mostrando a rua selecionada
        conn.commit()
        cur.close()
        conn.close()
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")

        ## rua selecionada

        uri.setDataSource("public", "rua_selec", "geom", " ", "id")
        layer_base10 = QgsVectorLayer(uri.uri(False), "rua_selecionada", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base10)

        canvas=self.iface.mapCanvas()
        extent=layer_base10.extent
        canvas.setExtent(extent())

        uri.setDataSource("public", "obra_l", "geom")
        layer_base11 = QgsVectorLayer(uri.uri(), "obra", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer(layer_base11)
        # Do something useful here - delete the line containing pass and
        # substitute with your code.

            #conn.commit()
        cur.close()
        conn.close()


        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[add_nm_obra_l])

        for row in cur.fetchall():
            valor = row[0]
        QMessageBox.information(QWidget(), "Inserir Obra ","Copie o Id da obra: %s" %valor, QMessageBox.Close)

        conn.commit()
        cur.close()
        conn.close()

        self.dlg.close()
        self.dlg.line_nm_obra_l.clear()
        self.dlg.line_custo_l.clear()
        self.dlg.line_nm_log_l.clear()
  


    def add_lotes_clicked_r(self):      
## cria os lotes beneficiados        
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 
        
        sel_nm_obrar = self.dlg.Cbx_sel_o_r.currentText() # nome da obra (obra.nome)
        nraio = int(self.dlg.spinBox.value())
        nraio = nraio*100
        zero=0
        nao='nao'
        # selecionando o atributo id_obra a partir do nome da obra
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_nm_obrar])
        
        for row in cur.fetchall():
            add_id_o_r = row[0]
        
        conn.commit()
        cur.close()
        conn.close()    
        #--------------------------------
        
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 
          
        # inserir lotes beneficiados
        cur.execute("INSERT INTO lotes_benef(id_obra, id, indfisc, area, testada, dist, valorizacao, rco, cvi, cm, isentos, geom) \
        SELECT \
        obra.id_obra,  pe.lpal_area_construida_a.id, \
        pe.lpal_area_construida_a.indfisc, st_area(pe.lpal_area_construida_a.geom), %s,\
        st_Distance(pe.lpal_area_construida_a.geom,obra_r.geom), %s, %s, %s, %s, %s, pe.lpal_area_construida_a.geom \
        FROM pe.lpal_area_construida_a, obra_r, obra \
        WHERE St_Intersects(pe.lpal_area_construida_a.geom, St_Buffer(obra_r.geom, %s)) \
        AND obra_r.id_obra = %s  AND obra.id_obra=obra_r.id_obra ", [zero, zero, zero, zero, zero, nao, nraio, add_id_o_r])

        subst = 'SEM CADASTRO'
        cur.execute(""" UPDATE lotes_benef SET indfisc = 'NULL' where lotes_benef.indfisc = %s""" ,[subst])
        
        conn.commit()
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
         # faz uma view dos lotes beneficiados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_benef_r AS
        SELECT lotes_benef.*
        FROM lotes_benef
        WHERE lotes_benef.id_obra='%s' """ % add_id_o_r)



        # faz uma view da obra selecionada 
        cur.execute("""CREATE OR REPLACE VIEW obra_selec_r AS
        SELECT obra.*, obra_r.geom
        FROM obra, obra_r
        WHERE obra.id_obra =%s AND obra.id_obra=obra_r.id_obra""" % add_id_o_r)

        conn.commit()
        cur.close()
        conn.close()

        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")

        uri.setDataSource("public", "lotes_benef_r", "geom", " ", "id_lotes")
        layer_base12 = QgsVectorLayer(uri.uri(False), "lotes_benef_r", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base12)

        uri.setDataSource("public", "obra_selec_r", "geom", " ", "id_obra")
        layer_base13 = QgsVectorLayer(uri.uri(False), "obra_selec_r", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base13)

        canvas=self.iface.mapCanvas()
        extent=layer_base12.extent
        canvas.setExtent(extent())

        cur.close()
        conn.close()

        self.dlg.close()

    def add_lotes_clicked_lin(self):
## cria os lotes beneficiados 
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()

        # Ler valores das lines 
        sel_nm_obral = self.dlg.Cbx_sel_o_l.currentText()
        add_larg_r =int( self.dlg.line_l_rua.text()) # nome da rua
        add_larg_r = (add_larg_r/2)+10
        zero=0
        nao='nao'

        # selecionando o atributo id_obra a partir do nome da obra
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_nm_obral])
        
        for row in cur.fetchall():
            add_id_o_l = row[0]

        conn.commit()
        cur.close()
        conn.close()    
        #--------------------------------

         ## conectando com o BD
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        
        # inserir os lotes beneficiados de acordo com a obra e a area da obra
        cur.execute("INSERT INTO lotes_benef(id_obra, id, indfisc,area,testada, dist,valorizacao, rco, cvi, cm, isentos, geom)\
                    SELECT obra.id_obra, pe.lpal_area_construida_a.id, pe.lpal_area_construida_a.indfisc, st_area(pe.lpal_area_construida_a.geom), %s, %s, %s, %s, %s, %s, %s, pe.lpal_area_construida_a.geom \
                    FROM pe.lpal_area_construida_a, obra_l, obra \
                    WHERE St_Intersects(pe.lpal_area_construida_a.geom, St_Buffer(obra_l.geom, %s)) \
                    AND obra_l.id_obra = %s AND obra.id_obra=obra_l.id_obra  ", \
                    [zero, zero, zero, zero, zero, zero, nao, add_larg_r, add_id_o_l])
        
        subst = 'SEM CADASTRO'
        cur.execute(""" UPDATE lotes_benef SET indfisc = 'NULL' where lotes_benef.indfisc = %s""" ,[subst])
        
        conn.commit()
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 
        
        # faz uma view dos lotes beneficiados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_benef_l AS
        SELECT lotes_benef.*
        FROM lotes_benef
        WHERE lotes_benef.id_obra='%s' """% add_id_o_l)
                

        # faz uma view da obra selecionada
        
        cur.execute("""CREATE OR REPLACE VIEW obra_selec_l AS
        SELECT obra.*, obra_l.geom
        FROM obra, obra_l
        WHERE obra.id_obra =%s AND obra.id_obra=obra_l.id_obra""" % add_id_o_l)

            
        conn.commit()
        cur.close()
        conn.close()
         
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")


        uri.setDataSource("public", "lotes_benef_l", "geom", " ", "id_lotes")
        layer_base14 = QgsVectorLayer(uri.uri(False), "lotes_benef_l", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base14)

        uri.setDataSource("public", "obra_selec_l", "geom", " ", "id_obra")
        layer_base15 = QgsVectorLayer(uri.uri(False), "obra_selec_l", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base15)
        
        canvas=self.iface.mapCanvas()
        extent=layer_base14.extent
        canvas.setExtent(extent())

        cur.close()
        conn.close()
        
        self.dlg.close()
        self.dlg.line_l_rua.clear()
        self.dlg.close()


    def run2(self):

## segundo ícone
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
#-------------------------------------------------------------------------------
        # apresenta obras que possuem lotes beneficiados - TODOS 
        cur.execute("""SELECT obra.nome FROM obra WHERE obra.id_obra in (SELECT lotes_benef.id_obra FROM lotes_benef) AND obra.id_obra NOT in (SELECT lotes_def.id_obra FROM lotes_def)""")
        self.dlg2.Cbx_table.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg2.Cbx_table.addItem(nome[0])        
        self.dlg2.show()
        result = self.dlg2.exec_()
        # See if OK was pressed
#----------------------------
        cur.close()
        conn.close()

        if result == 1:
            pass
    def table(self):
        
        t_sel_obra = self.dlg2.Cbx_table.currentText()

        #--------------------------- 
        #visualizando a tabela no plugin
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        cur.execute("""SELECT lotes_benef.indfisc,  lotes_benef.testada, lotes_benef.area, lotes_benef.dist, lotes_benef.valorizacao, lotes_benef.rco, lotes_benef.cvi, lotes_benef.cm, lotes_benef.isentos FROM obra, lotes_benef WHERE lotes_benef.id_obra=obra.id_obra AND obra.nome=%s""", [t_sel_obra])
        self.dlg2.tableWidget.clear()
        self.dlg2.tableWidget.setColumnCount(9)
        self.dlg2.tableWidget.setHorizontalHeaderLabels(['indfisc', 'testada', 'area (m^2)', 'dist (m)', 'valorizacao', 'RCO', 'CVI', 'CM', 'isentos'])
        row1 = 0
        for nome in cur.fetchall():
            self.dlg2.tableWidget.insertRow(row1)
            indfisc_t = QTableWidgetItem(str(nome[0])) #indicacao fiscal
            testada_t = QTableWidgetItem(str(nome[1])) #testada
            area_t = QTableWidgetItem(str(round(nome[2], 3))) #area
            dist_t = QTableWidgetItem(str(round(nome[3],3))) #distancia
            valorizacao_t = QTableWidgetItem(str(nome[4])) #valorizacao
            rco_t = QTableWidgetItem(str(nome[5])) #rco
            cvi_t = QTableWidgetItem(str(nome[6])) #cvi
            cm_t = QTableWidgetItem(str(nome[7])) #cm
            isentos_t = QTableWidgetItem(str(nome[8])) #isentos

            self.dlg2.tableWidget.setItem(row1, 0, indfisc_t)
            self.dlg2.tableWidget.setItem(row1, 1, testada_t)
            self.dlg2.tableWidget.setItem(row1, 2, area_t)
            self.dlg2.tableWidget.setItem(row1, 3, dist_t)
            self.dlg2.tableWidget.setItem(row1, 4, valorizacao_t)
            self.dlg2.tableWidget.setItem(row1, 5, rco_t)
            self.dlg2.tableWidget.setItem(row1, 6, cvi_t)
            self.dlg2.tableWidget.setItem(row1, 7, cm_t)
            self.dlg2.tableWidget.setItem(row1, 8, isentos_t)

            row1 = row1 + 1

                  
        conn.commit()
        cur.close()
        conn.close()
        
    def select_output_file(self):
        
        filename = QFileDialog.getSaveFileName(self.dlg2, "Select output file ","", '*.csv')
        self.dlg2.lineEdit.setText(filename)

    def salvar(self):

        t_sel_obra = self.dlg2.Cbx_table.currentText()
        diretorio= self.dlg2.lineEdit.text()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        

        cur.execute("""SELECT lotes_benef.indfisc, lotes_benef.testada,lotes_benef.area, lotes_benef.dist, lotes_benef.valorizacao, lotes_benef.rco, lotes_benef.cvi, lotes_benef.cm, lotes_benef.isentos  FROM obra, lotes_benef WHERE lotes_benef.id_obra=obra.id_obra AND obra.nome=%s""", [t_sel_obra])

        result=cur.fetchall()
#-------------------------------------------------------------------------------------------------

#        first=pd.DataFrame(result, columns=["nome", "indifisc", "dist"])
#        first.to_csv("%s" % diretorio, index = False)
#-------------------------------------------------------------------------------------------------
        c=csv.writer(open("%s" % diretorio, "wb"))
        c.writerow(['indfisc', 'testada', 'area (m^2)', 'dist (m)', 'valorizacao', 'RCO', 'CVI', 'CM', 'isentos'])
        for row in result:
            c.writerow(row)
        QMessageBox.information(QWidget(), "Salvar ","Nome da obra: %s" % t_sel_obra, QMessageBox.Close)
        self.dlg2.lineEdit.clear()
            
        conn.commit()
        cur.close()
        conn.close()

        self.dlg2.close()
        self.dlg2.lineEdit.clear()

    def run3(self):
# terceiro ícone
        
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()        
        #-------------------------------------------------------------------------------
        # apresenta obras que possuem lotes beneficiados -TODOS que ainda nao foram definidos 
        cur.execute("""SELECT obra.nome FROM obra WHERE obra.id_obra not in (SELECT lotes_def.id_obra FROM lotes_def) AND obra.id_obra in (SELECT lotes_benef.id_obra FROM lotes_benef)""")
        self.dlg3.Cbx_imp_o.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg3.Cbx_imp_o.addItem(nome[0])

        cur.close()
        conn.close()


        
        self.dlg3.show()

        result = self.dlg3.exec_()
        # See if OK was pressed
#----------------------------

        if result == 1:
            pass
    def select_input_file(self):

        filename_2 = QFileDialog.getOpenFileName(self.dlg3, "Open Data file","", '*.csv')
        self.dlg3.lineEdit_2.setText(filename_2)
        
    def salvar_2(self):
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 

        importar= self.dlg3.lineEdit_2.text()
        sel_obra_imp = self.dlg3.Cbx_imp_o.currentText()

        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_obra_imp])

        for row in cur.fetchall():
            add_id_o = row[0]
        conn.commit()
        cur.close()
        conn.close()

        # le arquivo csv e depois salva no banco
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()
        csv_data=csv.reader(file('%s' %importar))
        next(csv_data)
        for row in csv_data:
            indfisc_t = row[0]
            testada_t = row[1]
            area_t = row[2]
            dist_t = row [3]
            valorizacao_t = row[4]
            rco_t = row[5]
            cvi_t = row[6]
            cm_t = row[7]
            isentos_t = row[8]
            cur.execute("""INSERT INTO lotes_def( indfisc, testada, area, dist, valorizacao, RCO, CVI, CM, isentos, id_obra)\
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",\
            [indfisc_t, testada_t, area_t, dist_t, valorizacao_t, rco_t, cvi_t, cm_t, isentos_t, add_id_o])

        conn.commit()
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 

        # faz uma view dos lotes beneficiados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_beneficiados AS
        SELECT lotes_def.*, pe.lpal_area_construida_a.geom
        FROM lotes_def, pe.lpal_area_construida_a
        WHERE lotes_def.id_obra=%s AND pe.lpal_area_construida_a.indfisc = lotes_def.indfisc""" %add_id_o)

        cur.execute("""CREATE OR REPLACE VIEW lotes_isentos AS
        SELECT lotes_def.*, pe.lpal_area_construida_a.geom
        FROM lotes_def, pe.lpal_area_construida_a
        WHERE lotes_def.id_obra=%s AND pe.lpal_area_construida_a.indfisc = lotes_def.indfisc AND lotes_def.isentos='sim'""" %add_id_o)

        # faz uma view da obra selecionada
        cur.execute("""CREATE OR REPLACE VIEW obra_finalizada_r AS
        SELECT obra.*, obra_r.geom
        FROM obra, obra_r
        WHERE obra.id_obra =%s AND obra.id_obra=obra_r.id_obra """ % add_id_o)

        cur.execute("""CREATE OR REPLACE VIEW obra_finalizada_l AS
        SELECT obra.*, obra_l.geom
        FROM obra, obra_l
        WHERE obra.id_obra = %s AND obra.id_obra=obra_l.id_obra """ % add_id_o)

            
        conn.commit()
        cur.close()
        conn.close()
        
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")


        uri.setDataSource("public", "lotes_beneficiados", "geom", " ", "id_lotes_def")
        layer_base20 = QgsVectorLayer(uri.uri(False), "lotes_beneficiados", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base20)

        uri.setDataSource("public", "lotes_isentos", "geom", " ", "id_lotes_def")
        layer_base201 = QgsVectorLayer(uri.uri(False), "lotes_isentos", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base201)

        uri.setDataSource("public", "obra_finalizada_r", "geom", " ", "id_obra")
        layer_base21 = QgsVectorLayer(uri.uri(False), "obra_finalizada_r", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base21)

        uri.setDataSource("public", "obra_finalizada_l", "geom", " ", "id_obra")
        layer_base22 = QgsVectorLayer(uri.uri(False), "obra_finalizada_l", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base22)
        
        
        canvas=self.iface.mapCanvas()
        extent=layer_base20.extent
        canvas.setExtent(extent())
        
        cur.close()
        conn.close()
        self.dlg3.close()

    def run4(self):
## quarto ícone
## apresenta novamente as camadas da base
        layers1 = QgsMapLayerRegistry.instance().mapLayers().values()

        for layer in layers1:
            if layer.name() == 'limite_municipal':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'perimetro_urbano':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'limite_bairros':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'arruamento':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'quadras':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'lotes':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
            elif layer.name() == 'hidrografia':
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        ## conectando com o banco

        
        # add layers para a PRIMEIRA visualizacao
        #conectando com o banco
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")
        
        # limite municipal
        uri.setDataSource("pe", "lpal_municipio_a", "geom")
        layer_base1 = QgsVectorLayer(uri.uri(), "limite_municipal", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base1.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base1)

        #perimetro urbano
        uri.setDataSource("ge", "cb_area_urbana_isolada_a", "geom")
        layer_base2 = QgsVectorLayer(uri.uri(), "perimetro_urbano", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base2.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base2)

        # limite dos bairros
        uri.setDataSource("pe", "lpal_distrito_a", "geom")
        layer_base3 = QgsVectorLayer(uri.uri(), "limite_bairros", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base3.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base3)
        
        #arruamento
        uri.setDataSource("ge", "cb_trecho_arruamento_l", "geom")
        layer_base4 = QgsVectorLayer(uri.uri(), "arruamento", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base4.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base4)

        #quadras
        uri.setDataSource("ge", "cb_quadra_a", "geom")
        layer_base5 = QgsVectorLayer(uri.uri(False), "quadras", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base5.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base5)

        #lotes
        uri.setDataSource("pe", "lpal_area_construida_a", "geom")
        layer_base6 = QgsVectorLayer(uri.uri(), "lotes", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base6.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base6)

        #hidrografia
        uri.setDataSource("pe", "hid_trecho_drenagem_l", "geom")
        layer_base7 = QgsVectorLayer(uri.uri(), "hidrografia", "postgres")
        QgsMapLayerRegistry.instance().removeMapLayer(layer_base7.id())
        QgsMapLayerRegistry.instance().addMapLayer(layer_base7)

        # show the dialog
        # Run the dialog event loop
        #conn.commit()
        #cur.close()
        #conn.close()

        
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()        
#-------------------------------------------------------------------------------
#       Apresenta as obras do tipo radial em processo
        cur.execute("""SELECT obra.nome FROM obra, obra_r WHERE obra.id_obra in (SELECT lotes_benef.id_obra FROM lotes_benef) AND obra.id_obra=obra_r.id_obra AND obra.id_obra NOT in (SELECT lotes_def.id_obra FROM lotes_def)""")
        self.dlg4.Cbx_show_r.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg4.Cbx_show_r.addItem(nome[0])  
            
#       Apresenta as obras do tipo linear em processo
        cur.execute("""SELECT obra.nome FROM obra, obra_l WHERE obra.id_obra in (SELECT lotes_benef.id_obra FROM lotes_benef) AND obra.id_obra=obra_l.id_obra AND obra.id_obra NOT in (SELECT lotes_def.id_obra FROM lotes_def)""")
        self.dlg4.Cbx_show_l.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg4.Cbx_show_l.addItem(nome[0])

#      Apresenta as obras ja finalizadas
        cur.execute("""SELECT obra.nome FROM obra, obra_r WHERE obra.id_obra in (SELECT lotes_def.id_obra FROM lotes_def) AND obra.id_obra=obra_r.id_obra """)
        self.dlg4.Cbx_show_fim_r.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg4.Cbx_show_fim_r.addItem(nome[0])


        cur.execute("""SELECT obra.nome FROM obra, obra_l WHERE obra.id_obra in (SELECT lotes_def.id_obra FROM lotes_def) AND obra.id_obra=obra_l.id_obra""")
        self.dlg4.Cbx_show_fim_l.clear()
        for nome in cur.fetchall():
            #attrs = feature.atributes('nome')
            self.dlg4.Cbx_show_fim_l.addItem(nome[0])



        cur.close()
        conn.close()


        
        self.dlg4.show()
        result = self.dlg4.exec_()
        # See if OK was pressed
#----------------------------

        if result == 1:
            pass

    def visu_proc_lin(self):


        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()       
        # ler a obra selecionada
        sel_nm_obral_2 = self.dlg4.Cbx_show_l.currentText()

        # selecionando o atributo id_obra a partir do nome da obra
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_nm_obral_2])
        
        for row in cur.fetchall():
            add_id_o_l = row[0]
        
        conn.commit()
        cur.close()
        conn.close() 
              
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor()  
        
        # faz uma view dos lotes beneficiados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_benef_l AS
        SELECT lotes_benef.*
        FROM lotes_benef, obra_l, obra
        WHERE lotes_benef.id_obra='%s'AND lotes_benef.id_obra=obra_l.id_obra AND obra.id_obra=obra_l.id_obra"""% add_id_o_l)

        # faz uma view da obra selecionada
        
        cur.execute("""CREATE OR REPLACE VIEW obra_selec_l AS
        SELECT obra.*, obra_l.geom
        FROM obra, obra_l
        WHERE obra.id_obra =%s AND obra.id_obra=obra_l.id_obra""" % add_id_o_l)
            
        conn.commit()
        cur.close()
        conn.close()
         
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")
        
        uri.setDataSource("public", "lotes_benef_l", "geom", " ", "id_lotes")
        layer_base16 = QgsVectorLayer(uri.uri(False), "lotes_benef_l", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base16)
        
        uri.setDataSource("public", "obra_selec_l", "geom", " ", "id_obra")
        layer_base17 = QgsVectorLayer(uri.uri(False), "obra_selec_l", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base17)
        
        canvas=self.iface.mapCanvas()
        extent=layer_base16.extent
        canvas.setExtent(extent())

        
        cur.close()
        conn.close()
        
        self.dlg4.close()

    def visu_proc_r(self):

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 
        
        sel_nm_obrar_2 = self.dlg4.Cbx_show_r.currentText()

        # selecionando o atributo id_obra a partir do nome da obra
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_nm_obrar_2])

        for row in cur.fetchall():
            add_id_o_r = row[0]

        conn.commit()
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 

        # faz uma view dos lotes beneficiados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_benef_r AS
        SELECT lotes_benef.*
        FROM lotes_benef
        WHERE lotes_benef.id_obra='%s' """ % add_id_o_r)

        # faz uma view da obra selecionada
        cur.execute("""CREATE OR REPLACE VIEW obra_selec_r AS
        SELECT obra.*, obra_r.geom
        FROM obra, obra_r
        WHERE obra.id_obra =%s AND obra.id_obra=obra_r.id_obra""" % add_id_o_r)
            
        conn.commit()
        cur.close()
        conn.close()
        
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")

        
        uri.setDataSource("public", "lotes_benef_r", "geom", " ", "id_lotes")
        layer_base18 = QgsVectorLayer(uri.uri(False), "lotes_benef_r", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base18)
        
        uri.setDataSource("public", "obra_selec_r", "geom", " ", "id_obra")
        layer_base19 = QgsVectorLayer(uri.uri(False), "obra_selec_r", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base19)
        
        canvas=self.iface.mapCanvas()
        extent=layer_base18.extent
        canvas.setExtent(extent())
        
        cur.close()
        conn.close()
        self.dlg4.close()

    def visu_fim_r(self):

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 
        
        sel_nm_obrar_3= self.dlg4.Cbx_show_fim_r.currentText()

        # selecionando o atributo id_obra a partir do nome da obra
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_nm_obrar_3])

        for row in cur.fetchall():
            add_id_o_r = row[0]

        conn.commit()
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 

        # faz uma view dos lotes finalizados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_beneficiados AS
        SELECT lotes_def.*, pe.lpal_area_construida_a.geom
        FROM lotes_def, pe.lpal_area_construida_a
        WHERE lotes_def.id_obra=%s AND pe.lpal_area_construida_a.indfisc = lotes_def.indfisc"""% add_id_o_r)

        cur.execute("""CREATE OR REPLACE VIEW lotes_isentos AS
        SELECT lotes_def.*, pe.lpal_area_construida_a.geom
        FROM lotes_def, pe.lpal_area_construida_a
        WHERE lotes_def.id_obra=%s AND pe.lpal_area_construida_a.indfisc = lotes_def.indfisc AND lotes_def.isentos='sim'""" %add_id_o_r)


        # faz uma view da obra selecionada
        cur.execute("""CREATE OR REPLACE VIEW obra_finalizada_r AS
        SELECT obra.*, obra_r.geom
        FROM obra, obra_r
        WHERE obra.id_obra =%s AND obra.id_obra=obra_r.id_obra""" % add_id_o_r)

        conn.commit()
        cur.close()
        conn.close()
        

        
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")

        uri.setDataSource("public", "lotes_beneficiados", "geom", " ", "id_lotes_def")
        layer_base20 = QgsVectorLayer(uri.uri(False), "lotes_beneficiados", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base20)

        uri.setDataSource("public", "lotes_isentos", "geom", " ", "id_lotes_def")
        layer_base201 = QgsVectorLayer(uri.uri(False), "lotes_isentos", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base201)

        uri.setDataSource("public", "obra_finalizada_r", "geom", " ", "id_obra")
        layer_base21 = QgsVectorLayer(uri.uri(False), "obra_finalizada_r", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base21)

        canvas=self.iface.mapCanvas()
        extent=layer_base20.extent
        canvas.setExtent(extent())
        
        cur.close()
        conn.close()
        self.dlg4.close()

    def visu_fim_l(self):
        
        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 
        
        sel_nm_obral_3= self.dlg4.Cbx_show_fim_l.currentText()

        # selecionando o atributo id_obra a partir do nome da obra
        cur.execute(""" SELECT obra.* FROM obra WHERE obra.nome= %s""" ,[sel_nm_obral_3])

        for row in cur.fetchall():
            add_id_o_l = row[0]

        conn.commit()
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname = 'sjp' port = '5432' user ='postgres' host = 'localhost' password = 'xxxx'")
        cur = conn.cursor() 

        # faz uma view dos lotes finalizados conforme a selecao da obra
        cur.execute("""CREATE OR REPLACE VIEW lotes_beneficiados AS
        SELECT lotes_def.*, pe.lpal_area_construida_a.geom
        FROM lotes_def, pe.lpal_area_construida_a
        WHERE lotes_def.id_obra=%s AND pe.lpal_area_construida_a.indfisc = lotes_def.indfisc"""% add_id_o_l)

        cur.execute("""CREATE OR REPLACE VIEW lotes_isentos AS
        SELECT lotes_def.*, pe.lpal_area_construida_a.geom
        FROM lotes_def, pe.lpal_area_construida_a
        WHERE lotes_def.id_obra=%s AND pe.lpal_area_construida_a.indfisc = lotes_def.indfisc AND lotes_def.isentos='sim'""" %add_id_o_l)


        # faz uma view da obra selecionada
        cur.execute("""CREATE OR REPLACE VIEW obra_finalizada_l AS
        SELECT obra.*, obra_l.geom
        FROM obra, obra_l
        WHERE obra.id_obra = %s AND obra.id_obra=obra_l.id_obra """ % add_id_o_l)

        conn.commit()
        cur.close()
        conn.close()
        

        
        uri = QgsDataSourceURI()
        uri.setConnection("localhost", "5432", "sjp", "postgres", "xxxx")

        uri.setDataSource("public", "lotes_beneficiados", "geom", " ", "id_lotes_def")
        layer_base20 = QgsVectorLayer(uri.uri(False), "lotes_beneficiados", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base20)

        uri.setDataSource("public", "lotes_isentos", "geom", " ", "id_lotes_def")
        layer_base201 = QgsVectorLayer(uri.uri(False), "lotes_isentos", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base201)

        uri.setDataSource("public", "obra_finalizada_l", "geom", " ", "id_obra")
        layer_base21 = QgsVectorLayer(uri.uri(False), "obra_finalizada_l", "postgres")
        QgsMapLayerRegistry.instance().addMapLayer( layer_base21)

        canvas=self.iface.mapCanvas()
        extent=layer_base20.extent
        canvas.setExtent(extent())
        
        cur.close()
        conn.close()
        self.dlg4.close()
        