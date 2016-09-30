# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Gerarvisao
                                 A QGIS plugin
 Gera uma visão da base restringindo por estado
                              -------------------
        begin                : 2016-06-20
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Silas Bittencourt
        email                : silas.bittencourt.k@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
from qgis.core import QgsDataSourceURI
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import qgis.utils
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Gerarvisao_dialog import GerarvisaoDialog
import os.path
from os.path import expanduser
import getpass

class Gerarvisao:
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
            'Gerarvisao_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = GerarvisaoDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&IBGE bases Estados')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Gerarvisao')
        self.toolbar.setObjectName(u'Gerarvisao')

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
        return QCoreApplication.translate('Gerarvisao', message)


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
        bases = ["bc100grj_base","bc250_base","bcim_base","sc10_base","ptcon_base","rj25_base"] 
        estados=["SC","PR","RJ","SP","MS","DF","MG","GO","SE","AL","BA","RO","MT","PE","AC","PB","TO","RN","CE","PI","MA","AM","PA","AP","ES","RS","RR","BRASIL"]
        estados.sort() 
        self.dlg.comboBox2.addItems(bases) #adicionar uma combobox 
        self.dlg.comboBox.addItems(estados)
        self.dlg.pushButton.pressed.connect(self.Adicionar)
        self.dlg.checkBox.setChecked(False)
        self.dlg.checkBox2.setChecked(False)
       
        
        
        user = getpass.getuser()
        caminho = "C:\Users\\" + user + "\.qgis2\python\plugins\Gerarvisao\IBGE.png"
        ca =  caminho
        icon_path = ca 
        
        self.add_action(
            icon_path,
            text=self.tr(u'Gera uma visão da base limitando por estado'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&IBGE bases Estados'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result==1:
            print self.dlg.lineEdit.text()
           
            pass
    
    
        
    
        
    
    
    def Adicionar(self):
        #problema no ES,DF e PE. os retangulos minimos foram gerados de forma imprecisa
        
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            
            msg.setInformativeText("SELECIONAR TABLES OU VIEWS")
            msg.setWindowTitle("ERRO")
            
            DF=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-48.3154248012742,-16.0925256872088),ST_Point(-47.2442922813961,-15.4482045928759)),4674))"
            ES=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-42.0815156147037,-21.5056436708075),ST_Point(-38.8640140990544,-17.6807566649591)),4674))"
            PE=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-41.5233775966829,-9.79295320440056),ST_Point(-33.8243561128078,-7.1500055308315)),4674))"
            AM=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-73.8014755559999,-9.81805555599998),ST_Point(-56.072542834,2.24660333299999)),4674))"
            PA=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-58.895460494,-9.8446245479999),ST_Point(-46.0518016219999,2.59092977199998)),4674))"
            AP=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-54.876921656,-1.236187835),ST_Point(-49.866696519,4.47682997599996)),4674))"
            RR=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-64.825069436,-1.59177628600008),ST_Point(-58.8867790479999,5.27178990699993)),4674))"
            AC=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-73.991437778,-11.142860556),ST_Point(-66.6243555559999,-7.111842778)),4674))"
            RN=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-38.581567425,-6.98277639600001),ST_Point(-34.968392281,-4.83169751900004)),4674))"
            CE=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-41.4231369169999,-7.85821843400009),ST_Point(-37.2525309639999,-2.78464608700001)),4674))"
            TO=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-38.7653740439999,-8.30296742200005),ST_Point(-34.7933117099998,-6.02596000699992)),4674))"
            SE=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-38.238820983,-11.568316797),ST_Point(-36.3968120549999,-9.51583238300006)),4674))"
            AL=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-38.2387361349999,-10.503960864),ST_Point(-35.1471022099999,-8.813087543)),4674))"
            PI=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-45.9953510249999,-10.9241847570001),ST_Point(-40.370528458,-2.74370819700004)),4674))"
            MA=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-48.7575454299998,-10.26177525),ST_Point(-41.7889157199999,-1.04999211500001)),4674))"
            RO=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-66.810202778,-13.6932783330001),ST_Point(-59.771975631,-7.969357222)),4674))"
            BA=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-46.617045825,-18.3507048889999),ST_Point(-37.341338945,-8.52476498600004)),4674))"
            TO=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-50.7410868649999,-13.467721818),ST_Point(-45.696034374,-5.16977692600003)),4674))"
            MG=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-51.049366,-22.922748),ST_Point(-39.8567878569999,-14.232144789)),4674))"
            GO=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-53.2479888889999,-19.478212),ST_Point(-45.90691787,-12.395215887)),4674))"
            MT=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-61.6333122219999,-18.041561),ST_Point(-50.209140259,-7.34808755000004)),4674))"
            RJ=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-44.8953823889998,-23.367199005),ST_Point(-40.9568661159999,-20.763237222)),4674))"
            SP=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-53.1144859999999,-25.31227032),ST_Point(-44.1631784119999,-19.7826299999999)),4674))"
            MS=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-58.1701906579999,-24.0701349370001),ST_Point(-50.9198079999999,-17.167893978)),4674))"
            PR=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-54.619900122,-26.7172419250001),ST_Point(-48.0231773019999,-22.5170339999999)),4674))"
            SC=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-53.837236523,-29.351423),ST_Point(-48.3591488829999,-25.9555528590001)),4674))"
            RS=r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-57.6438019999999,-33.750969),ST_Point(-49.691627506,-27.082396076)),4674))"
            BRASIL= None
            
            x = r"ST_Intersects(geom,ST_SetSRID(ST_MakeBox2D(ST_Point(-43.55702,-22.99089),ST_Point(-43.39439,-22.85297)),4674))"
            
            #BC250
            tablebc250 = ["complexo_habitacional","area_estrut_transporte","zona_lin_ener_comunicacao","posto_fiscal","area_agropec_ext_veg_pesca","area_saude","est_med_fenomenos","dep_saneamento","complexo_lazer","ponto_duto","edif_pub_civil","area_edificada","natureza_fundo","veg_cultivada","posto_pol_rod","antena_comunic","area_abast_agua","area_politico_admin","arquibancada","edif_saude","trecho_comunic","estrut_transp_patio","funicular","galeria_bueiro","trecho_drenagem","hidrovia","identificador_trecho_rod","area_industrial","caminho_aereo","pista_competicao","instituicao_publica","nome_local","passag_elevada_viaduto","pto_geod_topo_controle","trecho_ferroviario","vegetacao","inst_pub_inst_pub","ponte","curso_dagua","atracadouro","area_energia_eletrica","rocha_em_agua","banco_areia","org_civ_mil_edif_pub_civil","edif_comunic","org_agropec_ext_veg_pesca","via_ferrea","trecho_curso_dagua","edif_const_portuaria","edif_comerc_serv","area_urbana_isolada","posic_geo_localidade","edif_industrial","area_ruinas","eclusa","org_civ_mil_org_civ_mil","trecho_rod_via_rod","torre_energia","area_descontinuidade","edif_constr_est_med","travessia","obstaculo_navegacao","delimitacao_fisica","foz_maritima","fundeadouro","edif_ensino","area_habitacional","area_especial","area_ensino","girador_ferroviario","elemento_fisiografico","trecho_hidroviario","piscina","ponto_hipsometrico","ar_prop_part_lin_lim","coreto_tribuna","queda_dagua","bacia_hidrografica","sinalizacao_hidrovia","eixo_rodoviario","complexo_comunicacao","barragem","dep_abast_agua","area_comunicacao","edif_const_turistica","patio","est_gerad_energia_eletrica","area_comerc_serv","cemiterio","deposito_geral","pista_ponto_pouso","trecho_duto","equip_agropec","edif_pub_militar","area_de_litigio","edif_religiosa","estrut_transporte","edif_const_lazer","localidade","linha_de_limite","ar_especial_lin_lim","corredeira","complexo_abast_agua","org_ext_mineral","area_duto","faixa_seguranca","edificacao","est_med_fen_est_med_fen","edif_habitacional","ar_lit_ar_pol_admin","edif_agropec_ext_veg_pesca","edif_rodoviaria","passagem_nivel","edif_abast_agua","lin_lim_localidade","via_rodoviaria","org_industrial","torre_comunic","compl_ger_energia_eletrica","ar_lit_linha_de_limite","ext_mineral","ponto_rodoviario_fer","area_de_propriedade_part","edif_saneamento","sumidouro_vertedouro","pto_est_med_fenomenos","reservatorio_hidrico","area_saneamento","edif_servico_social","org_civil_militar","area_religiosa","marco_de_limite","entroncamento","org_comerc_serv","local_critico","limite_massa_dagua","veg_area_contato","terreno_sujeito_inundacao","tunel","trecho_energia","quebramar_molhe","area_servico_social","area_est_med_fenomenos","massa_dagua","travessia_pedestre","ruina","campo_quadra","area_lazer","terreno_exposto","posto_combustivel","sinalizacao","cremalheira","org_civil_militar_ar_es","ponto_trecho_energia","area_umida","edif_energia","fonte_dagua","ponto_hidroviario","duto","edif_metro_ferroviaria","recife","complexo_saneamento","grupo_transformadores","lin_lim_ar_pol_admin","comporta","edif_ext_mineral","subest_trans_dist_ener_elet","isolinha_hipsometrica","area_ext_mineral","ponto_drenagem","campo","edif_constr_aeroportuaria","plataforma","ponto_extremo"] 
            viewsBC250 = ['adm_area_pub_civil_a', 'adm_area_pub_militar_a', 'adm_edif_pub_civil_a', 'adm_edif_pub_civil_p', 'adm_edif_pub_militar_a', 'adm_edif_pub_militar_p', 'adm_posto_fiscal_a', 'adm_posto_fiscal_p', 'adm_posto_pol_rod_a', 'adm_posto_pol_rod_p', 'asb_area_abast_agua_a', 'asb_area_saneamento_a', 'asb_cemiterio_a', 'asb_cemiterio_p', 'asb_dep_abast_agua_a', 'asb_dep_abast_agua_p', 'asb_dep_saneamento_a', 'asb_dep_saneamento_p', 'asb_edif_abast_agua_a', 'asb_edif_abast_agua_p', 'asb_edif_saneamento_a', 'asb_edif_saneamento_p', 'eco_area_agropec_ext_vegetal_pesca_a', 'eco_area_comerc_serv_a', 'eco_area_ext_mineral_a', 'eco_area_industrial_a', 'eco_deposito_geral_a', 'eco_deposito_geral_p', 'eco_edif_agropec_ext_vegetal_pesca_a', 'eco_edif_agropec_ext_vegetal_pesca_p', 'eco_edif_comerc_serv_a', 'eco_edif_comerc_serv_p', 'eco_edif_ext_mineral_a', 'eco_edif_ext_mineral_p', 'eco_edif_industrial_a', 'eco_edif_industrial_p', 'eco_equip_agropec_a', 'eco_equip_agropec_l', 'eco_equip_agropec_p', 'eco_ext_mineral_a', 'eco_ext_mineral_p', 'eco_plataforma_a', 'eco_plataforma_p', 'edu_area_ensino_a', 'edu_area_lazer_a', 'edu_area_religiosa_a', 'edu_area_ruinas_a', 'edu_arquibancada_a', 'edu_arquibancada_p', 'edu_campo_quadra_a', 'edu_campo_quadra_p', 'edu_coreto_tribuna_a', 'edu_coreto_tribuna_p', 'edu_edif_const_lazer_a', 'edu_edif_const_lazer_p', 'edu_edif_const_turistica_a', 'edu_edif_const_turistica_p', 'edu_edif_ensino_a', 'edu_edif_ensino_p', 'edu_edif_religiosa_a', 'edu_edif_religiosa_p', 'edu_piscina_a', 'edu_pista_competicao_l', 'edu_ruina_a', 'edu_ruina_p', 'enc_antena_comunic_p', 'enc_area_comunicacao_a', 'enc_area_energia_eletrica_a', 'enc_edif_comunic_a', 'enc_edif_comunic_p', 'enc_edif_energia_a', 'enc_edif_energia_p', 'enc_est_gerad_energia_eletrica_a', 'enc_est_gerad_energia_eletrica_l', 'enc_est_gerad_energia_eletrica_p', 'enc_grupo_transformadores_a', 'enc_grupo_transformadores_p', 'enc_hidreletrica_a', 'enc_hidreletrica_l', 'enc_hidreletrica_p', 'enc_ponto_trecho_energia_p', 'enc_termeletrica_a', 'enc_termeletrica_p', 'enc_torre_comunic_p', 'enc_torre_energia_p', 'enc_trecho_comunic_l', 'enc_trecho_energia_l', 'enc_zona_linhas_energia_comunicacao_a', 'hid_area_umida_a', 'hid_bacia_hidrografica_a', 'hid_banco_areia_a', 'hid_banco_areia_l', 'hid_barragem_a', 'hid_barragem_l', 'hid_barragem_p', 'hid_comporta_l', 'hid_comporta_p', 'hid_confluencia_p', 'hid_corredeira_a', 'hid_corredeira_l', 'hid_corredeira_p', 'hid_fonte_dagua_p', 'hid_foz_maritima_a', 'hid_foz_maritima_l', 'hid_foz_maritima_p', 'hid_ilha_a', 'hid_ilha_l', 'hid_ilha_p', 'hid_limite_massa_dagua_l', 'hid_massa_dagua_a', 'hid_natureza_fundo_a', 'hid_natureza_fundo_l', 'hid_natureza_fundo_p', 'hid_ponto_drenagem_p', 'hid_ponto_inicio_drenagem_p', 'hid_quebramar_molhe_a', 'hid_quebramar_molhe_l', 'hid_queda_dagua_a', 'hid_queda_dagua_l', 'hid_queda_dagua_p', 'hid_recife_a', 'hid_recife_l', 'hid_recife_p', 'hid_reservatorio_hidrico_a', 'hid_rocha_em_agua_a', 'hid_rocha_em_agua_p', 'hid_sumidouro_vertedouro_p', 'hid_terreno_sujeito_inundacao_a', 'hid_trecho_drenagem_l', 'hid_trecho_massa_dagua_a', 'lim_area_de_litigio_a', 'lim_area_de_propriedade_particular_a', 'lim_area_desenvolvimento_controle_a', 'lim_area_desenvolvimento_controle_p', 'lim_area_uso_comunitario_a', 'lim_area_uso_comunitario_p', 'lim_bairro_a', 'lim_delimitacao_fisica_l', 'lim_distrito_a', 'lim_limite_area_especial_l', 'lim_limite_intra_municipal_administrativo_l', 'lim_limite_operacional_l', 'lim_limite_particular_l', 'lim_limite_politico_administrativo_l', 'lim_linha_de_limite_l', 'lim_marco_de_limite_p', 'lim_municipio_a', 'lim_outras_unid_protegidas_a', 'lim_outras_unid_protegidas_p', 'lim_outros_limites_oficiais_l', 'lim_pais_a', 'lim_regiao_administrativa_a', 'lim_sub_distrito_a', 'lim_terra_indigena_a', 'lim_terra_indigena_p', 'lim_terra_publica_a', 'lim_terra_publica_p', 'lim_unidade_conservacao_nao_snuc_a', 'lim_unidade_conservacao_nao_snuc_p', 'lim_unidade_federacao_a', 'lim_unidade_protecao_integral_a', 'lim_unidade_protecao_integral_p', 'lim_unidade_uso_sustentavel_a', 'lim_unidade_uso_sustentavel_p', 'loc_aglomerado_rural_de_extensao_urbana_a', 'loc_aglomerado_rural_de_extensao_urbana_p', 'loc_aglomerado_rural_isolado_a', 'loc_aglomerado_rural_isolado_p', 'loc_aldeia_indigena_a', 'loc_aldeia_indigena_p', 'loc_area_edificada_a', 'loc_area_habitacional_a', 'loc_area_urbana_isolada_a', 'loc_capital_a', 'loc_capital_p', 'loc_cidade_a', 'loc_cidade_p', 'loc_edif_habitacional_a', 'loc_edif_habitacional_p', 'loc_edificacao_a', 'loc_edificacao_p', 'loc_hab_indigena_a', 'loc_hab_indigena_p', 'loc_nome_local_p', 'loc_posic_geo_localidade_p', 'loc_vila_a', 'loc_vila_p', 'pto_area_est_med_fenomenos_a', 'pto_edif_constr_est_med_a', 'pto_edif_constr_est_med_p', 'pto_ponto_extremo_p', 'pto_pto_controle_p', 'pto_pto_est_med_fenomenos_p', 'pto_pto_ref_geod_topo_p', 'rel_alteracao_fisiografica_antropica_a', 'rel_alteracao_fisiografica_antropica_l', 'rel_curva_batimetrica_l', 'rel_curva_nivel_l', 'rel_dolina_a', 'rel_dolina_p', 'rel_duna_a', 'rel_duna_p', 'rel_elemento_fisiografico_natural_a', 'rel_elemento_fisiografico_natural_l', 'rel_elemento_fisiografico_natural_p', 'rel_gruta_caverna_p', 'rel_pico_p', 'rel_ponto_cotado_altimetrico_p', 'rel_ponto_cotado_batimetrico_p', 'rel_rocha_a', 'rel_rocha_p', 'rel_terreno_exposto_a', 'sau_area_saude_a', 'sau_area_servico_social_a', 'sau_edif_saude_a', 'sau_edif_saude_p', 'sau_edif_servico_social_a', 'sau_edif_servico_social_p', 'tra_area_duto_a', 'tra_atracadouro_a', 'tra_atracadouro_l', 'tra_atracadouro_p', 'tra_caminho_aereo_l', 'tra_condutor_hidrico_l', 'tra_cremalheira_l', 'tra_cremalheira_p', 'tra_eclusa_a', 'tra_eclusa_l', 'tra_eclusa_p', 'tra_edif_constr_aeroportuaria_a', 'tra_edif_constr_aeroportuaria_p', 'tra_edif_constr_portuaria_a', 'tra_edif_constr_portuaria_p', 'tra_edif_metro_ferroviaria_a', 'tra_edif_metro_ferroviaria_p', 'tra_edif_rodoviaria_a', 'tra_edif_rodoviaria_p', 'tra_entroncamento_p', 'tra_faixa_seguranca_a', 'tra_fundeadouro_a', 'tra_fundeadouro_l', 'tra_fundeadouro_p', 'tra_funicular_l', 'tra_funicular_p', 'tra_galeria_bueiro_l', 'tra_galeria_bueiro_p', 'tra_girador_ferroviario_p', 'tra_identificador_trecho_rodoviario_p', 'tra_local_critico_a', 'tra_local_critico_l', 'tra_local_critico_p', 'tra_obstaculo_navegacao_a', 'tra_obstaculo_navegacao_l', 'tra_obstaculo_navegacao_p', 'tra_passag_elevada_viaduto_l', 'tra_passag_elevada_viaduto_p', 'tra_passagem_nivel_p', 'tra_patio_a', 'tra_patio_p', 'tra_pista_ponto_pouso_a', 'tra_pista_ponto_pouso_l', 'tra_pista_ponto_pouso_p', 'tra_ponte_l', 'tra_ponte_p', 'tra_ponto_duto_p', 'tra_ponto_ferroviario_p', 'tra_ponto_hidroviario_p', 'tra_ponto_rodoviario_p', 'tra_posto_combustivel_a', 'tra_posto_combustivel_p', 'tra_sinalizacao_p', 'tra_travessia_l', 'tra_travessia_p', 'tra_travessia_pedestre_l', 'tra_travessia_pedestre_p', 'tra_trecho_duto_l', 'tra_trecho_ferroviario_l', 'tra_trecho_hidroviario_l', 'tra_trecho_rodoviario_l', 'tra_tunel_l', 'tra_tunel_p', 'veg_brejo_pantano_a', 'veg_caatinga_a', 'veg_campinarana_a', 'veg_campo_a', 'veg_cerrado_cerradao_a', 'veg_estepe_a', 'veg_floresta_a', 'veg_macega_chavascal_a', 'veg_mangue_a', 'veg_veg_area_contato_a', 'veg_veg_cultivada_a', 'veg_veg_restinga_a']
            tablebc250.sort()
            viewsBC250.sort()
           
           #BC100GRJ_BASE
            viewsbc100=["adm_edif_pub_civil_a","adm_edif_pub_civil_p","asb_area_saneamento_a","asb_cemiterio_a","eco_area_comerc_serv_a","eco_area_ext_mineral_a","eco_edif_industrial_p","eco_equip_agropec_l","edu_campo_quadra_p","edu_coreto_tribuna_a","edu_coreto_tribuna_p","enc_grupo_transformadores_p","enc_hidreletrica_a","hid_area_umida_a","hid_bacia_hidrografica_a","hid_quebramar_molhe_l","hid_queda_dagua_a","lim_area_desenvolvimento_controle_p","lim_area_uso_comunitario_a","lim_area_uso_comunitario_p","loc_aglomerado_rural_de_extensao_urbana_a","loc_aglomerado_rural_de_extensao_urbana_p","loc_aglomerado_rural_isolado_a","pto_edif_constr_est_med_a","pto_edif_constr_est_med_p","rel_elemento_fisiografico_natural_a","rel_elemento_fisiografico_natural_l","sau_area_servico_social_a","sau_edif_saude_a","sau_edif_saude_p","tra_fundeadouro_a","tra_fundeadouro_l","tra_fundeadouro_p","tra_travessia_p","tra_travessia_pedestre_l","adm_area_pub_civil_a","lim_area_desenvolvimento_controle_a","pto_area_est_med_fenomenos_a","adm_area_pub_militar_a","adm_edif_pub_militar_a","adm_edif_pub_militar_p","adm_posto_fiscal_a","adm_posto_fiscal_p","adm_posto_pol_rod_a","adm_posto_pol_rod_p","asb_area_abast_agua_a","asb_cemiterio_p","asb_dep_abast_agua_a","asb_dep_abast_agua_p","asb_dep_saneamento_a","asb_dep_saneamento_p","asb_edif_abast_agua_a","asb_edif_abast_agua_p","asb_edif_saneamento_a","asb_edif_saneamento_p","eco_area_agropec_ext_vegetal_pesca_a","eco_area_industrial_a","eco_deposito_geral_a","eco_deposito_geral_p","eco_edif_agropec_ext_vegetal_pesca_a","eco_edif_agropec_ext_vegetal_pesca_p","eco_edif_comerc_serv_a","eco_edif_comerc_serv_p","eco_edif_ext_mineral_a","eco_edif_ext_mineral_p","eco_edif_industrial_a","eco_equip_agropec_p","eco_equip_agropec_a","eco_ext_mineral_a","eco_ext_mineral_p","eco_plataforma_a","eco_plataforma_p","edu_area_ensino_a","edu_area_lazer_a","edu_area_religiosa_a","edu_area_ruinas_a","edu_arquibancada_a","edu_arquibancada_p","edu_campo_quadra_a","edu_edif_const_lazer_a","edu_edif_const_lazer_p","edu_edif_const_turistica_a","edu_edif_const_turistica_p","edu_edif_ensino_a","edu_edif_ensino_p","edu_edif_religiosa_a","edu_edif_religiosa_p","edu_piscina_a","edu_pista_competicao_l","edu_ruina_a","edu_ruina_p","enc_antena_comunic_p","enc_area_comunicacao_a","enc_area_energia_eletrica_a","enc_edif_comunic_a","enc_edif_comunic_p","enc_edif_energia_a","enc_edif_energia_p","enc_est_gerad_energia_eletrica_a","enc_est_gerad_energia_eletrica_l","enc_est_gerad_energia_eletrica_p","enc_grupo_transformadores_a","enc_hidreletrica_l","enc_hidreletrica_p","enc_ponto_trecho_energia_p","enc_termeletrica_a","enc_termeletrica_p","enc_torre_comunic_p","enc_torre_energia_p","enc_trecho_comunic_l","enc_trecho_energia_l","enc_zona_linhas_energia_comunicacao_a","hid_banco_areia_a","hid_banco_areia_l","hid_barragem_a","hid_barragem_l","hid_barragem_p","hid_comporta_l","hid_comporta_p","hid_confluencia_p","hid_corredeira_a","hid_corredeira_l","hid_corredeira_p","hid_fonte_dagua_p","hid_foz_maritima_a","hid_foz_maritima_l","hid_foz_maritima_p","hid_ilha_a","hid_ilha_l","hid_ilha_p","hid_limite_massa_dagua_l","hid_massa_dagua_a","hid_natureza_fundo_a","hid_natureza_fundo_l","hid_natureza_fundo_p","hid_ponto_drenagem_p","hid_ponto_inicio_drenagem_p","hid_quebramar_molhe_a","hid_queda_dagua_l","hid_queda_dagua_p","hid_recife_a","hid_recife_l","hid_recife_p","hid_reservatorio_hidrico_a","hid_rocha_em_agua_a","hid_rocha_em_agua_p","hid_sumidouro_vertedouro_p","hid_terreno_sujeito_inundacao_a","hid_trecho_drenagem_l","hid_trecho_massa_dagua_a","lim_area_de_litigio_a","lim_area_de_propriedade_particular_a","lim_area_descontinuidade_a","lim_bairro_a","lim_delimitacao_fisica_l","lim_distrito_a","lim_limite_area_especial_l","lim_limite_intra_municipal_administrativo_l","lim_limite_operacional_l","lim_limite_particular_l","lim_limite_politico_administrativo_l","lim_linha_de_limite_l","lim_marco_de_limite_p","lim_municipio_a","lim_outras_unid_protegidas_a","lim_outras_unid_protegidas_p","lim_outros_limites_oficiais_l","lim_pais_a","lim_regiao_administrativa_a","lim_sub_distrito_a","lim_terra_indigena_a","lim_terra_indigena_p","lim_terra_publica_a","lim_terra_publica_p","lim_unidade_conservacao_nao_snuc_a","lim_unidade_conservacao_nao_snuc_p","lim_unidade_federacao_a","lim_unidade_protecao_integral_a","lim_unidade_protecao_integral_p","lim_unidade_uso_sustentavel_a","lim_unidade_uso_sustentavel_p","loc_aglomerado_rural_isolado_p","loc_aldeia_indigena_a","loc_aldeia_indigena_p","loc_area_edificada_a","loc_area_habitacional_a","loc_area_urbana_isolada_a","loc_capital_a","loc_capital_p","loc_cidade_a","loc_cidade_p","loc_edif_habitacional_a","loc_edif_habitacional_p","loc_edificacao_a","loc_edificacao_p","loc_hab_indigena_a","loc_hab_indigena_p","loc_nome_local_p","loc_posic_geo_localidade_p","loc_vila_a","loc_vila_p","pto_ponto_extremo_p","pto_pto_controle_p","pto_pto_est_med_fenomenos_p","pto_pto_ref_geod_topo_p","rel_alteracao_fisiografica_antropica_a","rel_alteracao_fisiografica_antropica_l","rel_curva_batimetrica_l","rel_curva_nivel_l","rel_dolina_a","rel_dolina_p","rel_duna_a","rel_duna_p","rel_elemento_fisiografico_natural_p","rel_gruta_caverna_p","rel_pico_p","rel_ponto_cotado_altimetrico_p","rel_ponto_cotado_batimetrico_p","rel_rocha_a","rel_rocha_p","rel_terreno_exposto_a","sau_area_saude_a","sau_edif_servico_social_a","sau_edif_servico_social_p","tra_area_duto_a","tra_area_estrut_transporte_a","tra_arruamento_l","tra_atracadouro_a","tra_atracadouro_l","tra_atracadouro_p","tra_caminho_aereo_l","tra_ciclovia_l","tra_condutor_hidrico_l","tra_cremalheira_l","tra_cremalheira_p","tra_eclusa_a","tra_eclusa_l","tra_eclusa_p","tra_edif_const_portuaria_a","tra_edif_const_portuaria_p","tra_edif_constr_aeroportuaria_a","tra_edif_constr_aeroportuaria_p","tra_edif_metro_ferroviaria_a","tra_edif_metro_ferroviaria_p","tra_edif_rodoviaria_a","tra_edif_rodoviaria_p","tra_eixo_rodoviario_l","tra_entroncamento_p","tra_faixa_seguranca_a","tra_funicular_l","tra_funicular_p","tra_galeria_bueiro_l","tra_galeria_bueiro_p","tra_girador_ferroviario_p","tra_identificador_trecho_rodoviario_p","tra_local_critico_a","tra_local_critico_l","tra_local_critico_p","tra_obstaculo_navegacao_a","tra_obstaculo_navegacao_l","tra_obstaculo_navegacao_p","tra_passag_elevada_viaduto_l","tra_passag_elevada_viaduto_p","tra_passagem_nivel_p","tra_patio_a","tra_patio_p","tra_pista_ponto_pouso_a","tra_pista_ponto_pouso_l","tra_pista_ponto_pouso_p","tra_ponte_l","tra_ponte_p","tra_ponto_duto_p","tra_ponto_ferroviario_p","tra_ponto_hidroviario_p","tra_ponto_rodoviario_p","tra_posto_combustivel_a","tra_posto_combustivel_p","tra_sinalizacao_p","tra_travessia_l","tra_travessia_pedestre_p","tra_trecho_duto_l","tra_trecho_ferroviario_l","tra_trecho_hidroviario_l","tra_trecho_rodoviario_l","tra_trilha_picada_l","tra_tunel_l","tra_tunel_p","veg_brejo_pantano_a","veg_caatinga_a","veg_campinarana_a","veg_campo_a","veg_cerrado_cerradao_a","veg_estepe_a","veg_floresta_a","veg_macega_chavascal_a","veg_mangue_a","veg_veg_area_contato_a","veg_veg_cultivada_a","veg_veg_restinga_a"]
            tablesbc100=["area_ruinas","ar_lit_ar_pol_admin","area_energia_eletrica","ar_lit_linha_de_limite","ar_prop_part_lin_lim","area_descontinuidade","area_ext_mineral","subest_trans_dist_ener_elet","area_estrut_transporte","via_rodoviaria","duto","via_ferrea","complexo_comunicacao","org_civ_mil_org_civ_mil","trecho_curso_dagua","est_med_fenomenos","org_industrial","est_med_fen_est_med_fen","coreto_tribuna","org_ext_mineral","inst_pub_inst_pub","curso_dagua","edif_energia","edif_metro_ferroviaria","campo_quadra","area_especial","area_abast_agua","area_duto","campo","eclusa","ext_mineral","edif_constr_aeroportuaria","atracadouro","dep_abast_agua","complexo_habitacional","edif_const_lazer","pista_competicao","est_gerad_energia_eletrica","ponto_trecho_energia","natureza_fundo","isolinha_hipsometrica","posic_geo_localidade","ponto_hidroviario","localidade","edificacao","edif_religiosa","ponto_drenagem","trecho_drenagem","plataforma","nome_local","area_edificada","area_est_med_fenomenos","area_religiosa","galeria_bueiro","hidrovia","identificador_trecho_rod","obstaculo_navegacao","org_agropec_ext_veg_pesca","ponto_extremo","ponto_rodoviario_fer","trecho_rod_via_rod","veg_area_contato","area_de_litigio","cremalheira","edif_industrial","ruina","faixa_seguranca","fundeadouro","marco_de_limite","lin_lim_ar_pol_admin","edif_saneamento","area_umida","area_saneamento","posto_pol_rod","barragem","passagem_nivel","pto_geod_topo_controle","area_lazer","pista_ponto_pouso","travessia","edif_const_turistica","area_habitacional","org_civil_militar_ar_es","terreno_exposto","antena_comunic","entroncamento","edif_rodoviaria","area_agropec_ext_veg_pesca","quebramar_molhe","area_de_propriedade_part","trecho_energia","complexo_abast_agua","org_comerc_serv","torre_comunic","edif_habitacional","edif_pub_civil","limite_massa_dagua","local_critico","area_servico_social","org_civil_militar","banco_areia","cemiterio","ponte","posto_fiscal","trecho_comunic","trecho_ferroviario","arquibancada","torre_energia","reservatorio_hidrico","edif_agropec_ext_veg_pesca","queda_dagua","comporta","instituicao_publica","compl_ger_energia_eletrica","ponto_hipsometrico","deposito_geral","ponto_duto","travessia_pedestre","area_urbana_isolada","equip_agropec","linha_de_limite","edif_comunic","sumidouro_vertedouro","dep_saneamento","piscina","grupo_transformadores","foz_maritima","area_ensino","org_civ_mil_edif_pub_civil","patio","funicular","edif_const_portuaria","pto_est_med_fenomenos","caminho_aereo","zona_lin_ener_comunicacao","corredeira","rocha_em_agua","vegetacao","ar_especial_lin_lim","edif_servico_social","edif_constr_est_med","elemento_fisiografico","estrut_transporte","eixo_rodoviario","complexo_saneamento","posto_combustivel","massa_dagua","estrut_transp_patio","lin_lim_localidade","edif_abast_agua","tunel","edif_ext_mineral","fonte_dagua","area_saude","veg_cultivada","complexo_lazer","edif_ensino","trecho_hidroviario","bacia_hidrografica","terreno_sujeito_inundacao","recife","area_politico_admin","area_comerc_serv","sinalizacao","passag_elevada_viaduto","area_comunicacao","sinalizacao_hidrovia","delimitacao_fisica","edif_comerc_serv","trecho_duto","edif_pub_militar","area_industrial","girador_ferroviario","edif_saude"]
            viewsbc100.sort()
            tablesbc100.sort()
           
           #BCIM
            viewsbcim = ['adm_area_pub_civil_a', 'adm_area_pub_militar_a', 'adm_edif_pub_civil_a', 'adm_edif_pub_civil_p', 'adm_edif_pub_militar_a', 'adm_edif_pub_militar_p', 'adm_posto_fiscal_a', 'adm_posto_fiscal_p', 'adm_posto_pol_rod_a', 'adm_posto_pol_rod_p', 'asb_area_abast_agua_a', 'asb_area_saneamento_a', 'asb_cemiterio_a', 'asb_cemiterio_p', 'asb_dep_abast_agua_a', 'asb_dep_abast_agua_p', 'asb_dep_saneamento_a', 'asb_dep_saneamento_p', 'asb_edif_abast_agua_a', 'asb_edif_abast_agua_p', 'asb_edif_saneamento_a', 'asb_edif_saneamento_p', 'eco_area_agropec_ext_vegetal_pesca_a', 'eco_area_comerc_serv_a', 'eco_area_ext_mineral_a', 'eco_area_industrial_a', 'eco_deposito_geral_a', 'eco_deposito_geral_p', 'eco_edif_agropec_ext_vegetal_pesca_a', 'eco_edif_agropec_ext_vegetal_pesca_p', 'eco_edif_comerc_serv_a', 'eco_edif_comerc_serv_p', 'eco_edif_ext_mineral_a', 'eco_edif_ext_mineral_p', 'eco_edif_industrial_a', 'eco_edif_industrial_p', 'eco_equip_agropec_a', 'eco_equip_agropec_l', 'eco_equip_agropec_p', 'eco_ext_mineral_a', 'eco_ext_mineral_p', 'eco_plataforma_a', 'eco_plataforma_p', 'edu_area_ensino_a', 'edu_area_lazer_a', 'edu_area_religiosa_a', 'edu_area_ruinas_a', 'edu_arquibancada_a', 'edu_arquibancada_p', 'edu_campo_quadra_a', 'edu_campo_quadra_p', 'edu_coreto_tribuna_a', 'edu_coreto_tribuna_p', 'edu_edif_const_lazer_a', 'edu_edif_const_lazer_p', 'edu_edif_const_turistica_a', 'edu_edif_const_turistica_p', 'edu_edif_ensino_a', 'edu_edif_ensino_p', 'edu_edif_religiosa_a', 'edu_edif_religiosa_p', 'edu_piscina_a', 'edu_pista_competicao_l', 'edu_ruina_a', 'edu_ruina_p', 'enc_antena_comunic_p', 'enc_area_comunicacao_a', 'enc_area_energia_eletrica_a', 'enc_edif_comunic_a', 'enc_edif_comunic_p', 'enc_edif_energia_a', 'enc_edif_energia_p', 'enc_est_gerad_energia_eletrica_a', 'enc_est_gerad_energia_eletrica_l', 'enc_est_gerad_energia_eletrica_p', 'enc_grupo_transformadores_a', 'enc_grupo_transformadores_p', 'enc_hidreletrica_a', 'enc_hidreletrica_l', 'enc_hidreletrica_p', 'enc_ponto_trecho_energia_p', 'enc_termeletrica_a', 'enc_termeletrica_p', 'enc_torre_comunic_p', 'enc_torre_energia_p', 'enc_trecho_comunic_l', 'enc_trecho_energia_l', 'enc_zona_linhas_energia_comunicacao_a', 'hid_area_umida_a', 'hid_bacia_hidrografica_a', 'hid_banco_areia_a', 'hid_banco_areia_l', 'hid_barragem_a', 'hid_barragem_l', 'hid_barragem_p', 'hid_comporta_l', 'hid_comporta_p', 'hid_confluencia_p', 'hid_corredeira_a', 'hid_corredeira_l', 'hid_corredeira_p', 'hid_fonte_dagua_p', 'hid_foz_maritima_a', 'hid_foz_maritima_l', 'hid_foz_maritima_p', 'hid_ilha_a', 'hid_ilha_l', 'hid_ilha_p', 'hid_limite_massa_dagua_l', 'hid_massa_dagua_a', 'hid_natureza_fundo_a', 'hid_natureza_fundo_l', 'hid_natureza_fundo_p', 'hid_ponto_drenagem_p', 'hid_ponto_inicio_drenagem_p', 'hid_quebramar_molhe_a', 'hid_quebramar_molhe_l', 'hid_queda_dagua_a', 'hid_queda_dagua_l', 'hid_queda_dagua_p', 'hid_recife_a', 'hid_recife_l', 'hid_recife_p', 'hid_reservatorio_hidrico_a', 'hid_rocha_em_agua_a', 'hid_rocha_em_agua_p', 'hid_sumidouro_vertedouro_p', 'hid_terreno_sujeito_inundacao_a', 'hid_trecho_drenagem_l', 'hid_trecho_massa_dagua_a', 'lim_area_de_litigio_a', 'lim_area_de_propriedade_particular_a', 'lim_area_desenvolvimento_controle_a', 'lim_area_desenvolvimento_controle_p', 'lim_area_uso_comunitario_a', 'lim_area_uso_comunitario_p', 'lim_bairro_a', 'lim_delimitacao_fisica_l', 'lim_distrito_a', 'lim_limite_area_especial_l', 'lim_limite_intra_municipal_administrativo_l', 'lim_limite_operacional_l', 'lim_limite_particular_l', 'lim_limite_politico_administrativo_l', 'lim_linha_de_limite_l', 'lim_marco_de_limite_p', 'lim_municipio_a', 'lim_outras_unid_protegidas_a', 'lim_outras_unid_protegidas_p', 'lim_outros_limites_oficiais_l', 'lim_pais_a', 'lim_regiao_administrativa_a', 'lim_sub_distrito_a', 'lim_terra_indigena_a', 'lim_terra_indigena_p', 'lim_terra_publica_a', 'lim_terra_publica_p', 'lim_unidade_conservacao_nao_snuc_a', 'lim_unidade_conservacao_nao_snuc_p', 'lim_unidade_federacao_a', 'lim_unidade_protecao_integral_a', 'lim_unidade_protecao_integral_p', 'lim_unidade_uso_sustentavel_a', 'lim_unidade_uso_sustentavel_p', 'loc_aglomerado_rural_de_extensao_urbana_a', 'loc_aglomerado_rural_de_extensao_urbana_p', 'loc_aglomerado_rural_isolado_a', 'loc_aglomerado_rural_isolado_p', 'loc_aldeia_indigena_a', 'loc_aldeia_indigena_p', 'loc_area_edificada_a', 'loc_area_habitacional_a', 'loc_area_urbana_isolada_a', 'loc_capital_a', 'loc_capital_p', 'loc_cidade_a', 'loc_cidade_p', 'loc_edif_habitacional_a', 'loc_edif_habitacional_p', 'loc_edificacao_a', 'loc_edificacao_p', 'loc_hab_indigena_a', 'loc_hab_indigena_p', 'loc_nome_local_p', 'loc_posic_geo_localidade_p', 'loc_vila_a', 'loc_vila_p', 'pto_area_est_med_fenomenos_a', 'pto_edif_constr_est_med_a', 'pto_edif_constr_est_med_p', 'pto_ponto_extremo_p', 'pto_pto_controle_p', 'pto_pto_est_med_fenomenos_p', 'pto_pto_ref_geod_topo_p', 'rel_alteracao_fisiografica_antropica_a', 'rel_alteracao_fisiografica_antropica_l', 'rel_curva_batimetrica_l', 'rel_curva_nivel_l', 'rel_dolina_a', 'rel_dolina_p', 'rel_duna_a', 'rel_duna_p', 'rel_elemento_fisiografico_natural_a', 'rel_elemento_fisiografico_natural_l', 'rel_elemento_fisiografico_natural_p', 'rel_gruta_caverna_p', 'rel_pico_p', 'rel_ponto_cotado_altimetrico_p', 'rel_ponto_cotado_batimetrico_p', 'rel_rocha_a', 'rel_rocha_p', 'rel_terreno_exposto_a', 'sau_area_saude_a', 'sau_area_servico_social_a', 'sau_edif_saude_a', 'sau_edif_saude_p', 'sau_edif_servico_social_a', 'sau_edif_servico_social_p', 'tra_area_duto_a', 'tra_atracadouro_a', 'tra_atracadouro_l', 'tra_atracadouro_p', 'tra_caminho_aereo_l', 'tra_condutor_hidrico_l', 'tra_cremalheira_l', 'tra_cremalheira_p', 'tra_eclusa_a', 'tra_eclusa_l', 'tra_eclusa_p', 'tra_edif_constr_aeroportuaria_a', 'tra_edif_constr_aeroportuaria_p', 'tra_edif_constr_portuaria_a', 'tra_edif_constr_portuaria_p', 'tra_edif_metro_ferroviaria_a', 'tra_edif_metro_ferroviaria_p', 'tra_edif_rodoviaria_a', 'tra_edif_rodoviaria_p', 'tra_entroncamento_p', 'tra_faixa_seguranca_a', 'tra_fundeadouro_a', 'tra_fundeadouro_l', 'tra_fundeadouro_p', 'tra_funicular_l', 'tra_funicular_p', 'tra_galeria_bueiro_l', 'tra_galeria_bueiro_p', 'tra_girador_ferroviario_p', 'tra_identificador_trecho_rodoviario_p', 'tra_local_critico_a', 'tra_local_critico_l', 'tra_local_critico_p', 'tra_obstaculo_navegacao_a', 'tra_obstaculo_navegacao_l', 'tra_obstaculo_navegacao_p', 'tra_passag_elevada_viaduto_l', 'tra_passag_elevada_viaduto_p', 'tra_passagem_nivel_p', 'tra_patio_a', 'tra_patio_p', 'tra_pista_ponto_pouso_a', 'tra_pista_ponto_pouso_l', 'tra_pista_ponto_pouso_p', 'tra_ponte_l', 'tra_ponte_p', 'tra_ponto_duto_p', 'tra_ponto_ferroviario_p', 'tra_ponto_hidroviario_p', 'tra_ponto_rodoviario_p', 'tra_posto_combustivel_a', 'tra_posto_combustivel_p', 'tra_sinalizacao_p', 'tra_travessia_l', 'tra_travessia_p', 'tra_travessia_pedestre_l', 'tra_travessia_pedestre_p', 'tra_trecho_duto_l', 'tra_trecho_ferroviario_l', 'tra_trecho_hidroviario_l', 'tra_trecho_rodoviario_l', 'tra_tunel_l', 'tra_tunel_p', 'veg_brejo_pantano_a', 'veg_caatinga_a', 'veg_campinarana_a', 'veg_campo_a', 'veg_cerrado_cerradao_a', 'veg_estepe_a', 'veg_floresta_a', 'veg_macega_chavascal_a', 'veg_mangue_a', 'veg_veg_area_contato_a', 'veg_veg_cultivada_a', 'veg_veg_restinga_a']
            tablesbcim = ["posic_geo_localidade","sinalizacao","edif_pub_militar","area_est_med_fenomenos","ar_especial_lin_lim","area_duto","area_habitacional","complexo_lazer","coreto_tribuna","edif_comerc_serv","edif_ext_mineral","edif_habitacional","edif_saude","edif_servico_social","est_gerad_energia_eletrica","torre_comunic","fundeadouro","funicular","galeria_bueiro","terreno_sujeito_inundacao","org_ext_mineral","ponto_rodoviario_fer","cremalheira","fonte_dagua","torre_energia","trecho_drenagem","local_critico","posto_combustivel","complexo_saneamento","ponto_extremo","posto_fiscal","ar_lit_linha_de_limite","area_energia_eletrica","area_estrut_transporte","complexo_abast_agua","edif_agropec_ext_veg_pesca","ext_mineral","quebramar_molhe","lin_lim_ar_pol_admin","org_agropec_ext_veg_pesca","passag_elevada_viaduto","area_urbana_isolada","arquibancada","lin_lim_localidade","localidade","org_civil_militar_ar_es","org_comerc_serv","travessia_pedestre","trecho_curso_dagua","ruina","sumidouro_vertedouro","hidrovia","obstaculo_navegacao","via_rodoviaria","compl_ger_energia_eletrica","area_comerc_serv","org_industrial","duto","edif_religiosa","entroncamento","inst_pub_inst_pub","org_civil_militar","area_servico_social","patio","edificacao","estrut_transporte","recife","isolinha_hipsometrica","marco_de_limite","edif_constr_est_med","grupo_transformadores","equip_agropec","trecho_comunic","pto_geod_topo_controle","ponto_duto","sinalizacao_hidrovia","edif_const_portuaria","pista_competicao","dep_abast_agua","trecho_energia","area_abast_agua","plataforma","via_ferrea","vegetacao","area_especial","corredeira","edif_comunic","edif_constr_aeroportuaria","edif_rodoviaria","foz_maritima","ponto_drenagem","antena_comunic","identificador_trecho_rod","area_saneamento","trecho_rod_via_rod","edif_energia","delimitacao_fisica","massa_dagua","queda_dagua","area_saude","banco_areia","veg_area_contato","pto_est_med_fenomenos","edif_const_turistica","faixa_seguranca","dep_saneamento","trecho_ferroviario","area_de_litigio","estrut_transp_patio","campo_quadra","caminho_aereo","ponto_hidroviario","edif_const_lazer","trecho_hidroviario","trecho_duto","area_umida","edif_pub_civil","curso_dagua","passagem_nivel","area_lazer","veg_cultivada","subest_trans_dist_ener_elet","ar_prop_part_lin_lim","est_med_fen_est_med_fen","atracadouro","pista_ponto_pouso","area_de_propriedade_part","deposito_geral","area_ext_mineral","posto_pol_rod","area_ruinas","edif_industrial","piscina","natureza_fundo","bacia_hidrografica","area_descontinuidade","edif_metro_ferroviaria","linha_de_limite","eclusa","edif_ensino","instituicao_publica","ponte","ar_lit_ar_pol_admin","rocha_em_agua","est_med_fenomenos","zona_lin_ener_comunicacao","eixo_rodoviario","limite_massa_dagua","elemento_fisiografico","area_edificada","edif_abast_agua","org_civ_mil_org_civ_mil","tunel","edif_saneamento","terreno_exposto","area_ensino","ponto_trecho_energia","area_agropec_ext_veg_pesca","complexo_comunicacao","nome_local","ponto_hipsometrico","area_religiosa","org_civ_mil_edif_pub_civil","area_industrial","reservatorio_hidrico","area_politico_admin","area_comunicacao","comporta","barragem","cemiterio","complexo_habitacional","travessia","girador_ferroviario","campo"]
            viewsbcim.sort()
            tablesbcim.sort()
           
           #SC10
            tablesSC10 = ["trecho_drenagem"]
            tablesSC10.sort()
           
           #ptcon_base
            viewsPTCON = ["pontos_ativos"]
            tablesPTCON = ["img_croqui","exemplos","img_formulario","pontosgps","usuarios","img_foto","equipes"]
            viewsPTCON.sort()
            tablesPTCON.sort()
            
           
           #rj25
            viewsRJ25=["veg_mangue_a","adm_area_pub_civil_a","adm_area_pub_militar_a","adm_edif_pub_civil_a","adm_edif_pub_civil_p","adm_edif_pub_militar_a","adm_edif_pub_militar_p","adm_posto_fiscal_a","adm_posto_fiscal_p","adm_posto_pol_rod_a","adm_posto_pol_rod_p","asb_area_abast_agua_a","asb_area_saneamento_a","asb_cemiterio_a","asb_cemiterio_p","asb_dep_abast_agua_a","asb_dep_abast_agua_p","asb_dep_saneamento_a","asb_dep_saneamento_p","asb_edif_abast_agua_a","asb_edif_abast_agua_p","asb_edif_saneamento_a","asb_edif_saneamento_p","eco_area_agropec_ext_vegetal_pesca_a","eco_area_comerc_serv_a","eco_area_ext_mineral_a","eco_area_industrial_a","eco_deposito_geral_a","eco_deposito_geral_p","eco_edif_agropec_ext_vegetal_pesca_a","eco_edif_agropec_ext_vegetal_pesca_p","eco_edif_comerc_serv_a","eco_edif_comerc_serv_p","eco_edif_ext_mineral_a","eco_edif_ext_mineral_p","eco_edif_industrial_a","eco_edif_industrial_p","eco_equip_agropec_a","eco_equip_agropec_l","eco_equip_agropec_p","eco_ext_mineral_a","eco_ext_mineral_p","eco_plataforma_a","eco_plataforma_p","edu_area_ensino_a","edu_area_lazer_a","edu_area_religiosa_a","edu_area_ruinas_a","edu_arquibancada_a","edu_arquibancada_p","edu_campo_quadra_a","edu_campo_quadra_p","edu_coreto_tribuna_a","edu_coreto_tribuna_p","edu_edif_const_lazer_a","edu_edif_const_lazer_p","edu_edif_const_turistica_a","edu_edif_const_turistica_p","edu_edif_ensino_a","edu_edif_ensino_p","edu_edif_religiosa_a","edu_edif_religiosa_p","edu_piscina_a","edu_pista_competicao_l","edu_ruina_a","edu_ruina_p","enc_antena_comunic_p","enc_area_comunicacao_a","enc_area_energia_eletrica_a","enc_edif_comunic_a","enc_edif_comunic_p","enc_edif_energia_a","enc_edif_energia_p","enc_est_gerad_energia_eletrica_a","enc_est_gerad_energia_eletrica_l","enc_est_gerad_energia_eletrica_p","enc_grupo_transformadores_a","enc_grupo_transformadores_p","enc_hidreletrica_a","enc_hidreletrica_l","enc_hidreletrica_p","enc_ponto_trecho_energia_p","enc_termeletrica_a","enc_termeletrica_p","enc_torre_comunic_p","enc_torre_energia_p","enc_trecho_comunic_l","enc_trecho_energia_l","enc_zona_linhas_energia_comunicacao_a","hid_area_umida_a","hid_bacia_hidrografica_a","hid_banco_areia_a","hid_banco_areia_l","hid_barragem_l","hid_barragem_a","hid_barragem_p","hid_comporta_l","hid_comporta_p","hid_confluencia_p","hid_corredeira_a","hid_corredeira_l","hid_corredeira_p","hid_fonte_dagua_p","hid_foz_maritima_a","hid_foz_maritima_l","hid_foz_maritima_p","hid_ilha_a","hid_ilha_l","hid_ilha_p","hid_limite_massa_dagua_l","hid_massa_dagua_a","hid_natureza_fundo_a","hid_natureza_fundo_l","hid_natureza_fundo_p","hid_ponto_drenagem_p","hid_ponto_inicio_drenagem_p","hid_quebramar_molhe_a","hid_quebramar_molhe_l","hid_queda_dagua_l","hid_queda_dagua_a","hid_queda_dagua_p","hid_recife_a","hid_recife_l","hid_recife_p","hid_rocha_em_agua_p","hid_reservatorio_hidrico_a","hid_rocha_em_agua_a","hid_sumidouro_vertedouro_p","hid_terreno_sujeito_inundacao_a","hid_trecho_drenagem_l","hid_trecho_massa_dagua_a","lim_area_de_litigio_a","lim_area_de_propriedade_particular_a","lim_area_uso_comunitario_p","lim_area_descontinuidade_a","lim_area_desenvolvimento_controle_a","lim_area_desenvolvimento_controle_p","lim_bairro_a","lim_area_uso_comunitario_a","lim_delimitacao_fisica_l","lim_distrito_a","lim_limite_intra_municipal_administrativo_l","lim_limite_operacional_l","lim_limite_area_especial_l","lim_limite_particular_l","lim_marco_de_limite_p","lim_limite_politico_administrativo_l","lim_linha_de_limite_l","lim_municipio_a","lim_outras_unid_protegidas_a","lim_outras_unid_protegidas_p","lim_sub_distrito_a","lim_outros_limites_oficiais_l","lim_pais_a","lim_regiao_administrativa_a","lim_terra_indigena_a","lim_terra_indigena_p","lim_terra_publica_a","lim_terra_publica_p","lim_unidade_protecao_integral_a","lim_unidade_conservacao_nao_snuc_a","lim_unidade_conservacao_nao_snuc_p","lim_unidade_federacao_a","lim_unidade_protecao_integral_p","lim_unidade_uso_sustentavel_a","lim_unidade_uso_sustentavel_p","loc_aglomerado_rural_isolado_p","loc_aglomerado_rural_de_extensao_urbana_a","loc_aglomerado_rural_de_extensao_urbana_p","loc_aldeia_indigena_a","loc_aglomerado_rural_isolado_a","loc_aldeia_indigena_p","loc_area_edificada_a","loc_capital_p","loc_area_habitacional_a","loc_area_urbana_isolada_a","loc_capital_a","loc_cidade_a","loc_cidade_p","loc_edif_habitacional_a","loc_hab_indigena_a","loc_edif_habitacional_p","loc_edificacao_a","loc_edificacao_p","loc_hab_indigena_p","loc_nome_local_p","loc_posic_geo_localidade_p","loc_vila_a","loc_vila_p","pto_area_est_med_fenomenos_a","pto_edif_constr_est_med_a","pto_edif_constr_est_med_p","pto_ponto_extremo_p","pto_pto_ref_geod_topo_p","pto_pto_controle_p","pto_pto_est_med_fenomenos_p","rel_alteracao_fisiografica_antropica_a","rel_alteracao_fisiografica_antropica_l","rel_curva_batimetrica_l","rel_curva_nivel_l","rel_dolina_a","rel_dolina_p","rel_duna_a","rel_duna_p","rel_elemento_fisiografico_natural_a","rel_elemento_fisiografico_natural_l","rel_elemento_fisiografico_natural_p","rel_gruta_caverna_p","rel_pico_p","rel_ponto_cotado_altimetrico_p","rel_ponto_cotado_batimetrico_p","rel_rocha_a","rel_rocha_p","rel_terreno_exposto_a","sau_area_saude_a","sau_area_servico_social_a","sau_edif_saude_a","sau_edif_saude_p","sau_edif_servico_social_a","sau_edif_servico_social_p","tra_area_duto_a","tra_area_estrut_transporte_a","tra_arruamento_l","tra_atracadouro_a","tra_atracadouro_l","tra_atracadouro_p","tra_caminho_aereo_l","tra_ciclovia_l","tra_condutor_hidrico_l","tra_cremalheira_l","tra_cremalheira_p","tra_eclusa_a","tra_eclusa_l","tra_eclusa_p","tra_edif_const_portuaria_a","tra_edif_const_portuaria_p","tra_edif_constr_aeroportuaria_a","tra_edif_constr_aeroportuaria_p","tra_edif_metro_ferroviaria_a","tra_edif_metro_ferroviaria_p","tra_edif_rodoviaria_a","tra_edif_rodoviaria_p","tra_eixo_rodoviario_l","tra_entroncamento_p","tra_faixa_seguranca_a","tra_fundeadouro_a","tra_fundeadouro_l","tra_fundeadouro_p","tra_funicular_l","tra_funicular_p","tra_galeria_bueiro_l","tra_galeria_bueiro_p","tra_girador_ferroviario_p","tra_identificador_trecho_rodoviario_p","tra_local_critico_a","tra_local_critico_l","tra_local_critico_p","tra_obstaculo_navegacao_a","tra_obstaculo_navegacao_l","tra_obstaculo_navegacao_p","tra_passag_elevada_viaduto_l","tra_passag_elevada_viaduto_p","tra_passagem_nivel_p","tra_patio_a","tra_patio_p","tra_pista_ponto_pouso_a","tra_pista_ponto_pouso_l","tra_pista_ponto_pouso_p","tra_ponte_l","tra_ponte_p","tra_ponto_duto_p","tra_ponto_ferroviario_p","tra_ponto_hidroviario_p","tra_ponto_rodoviario_p","tra_posto_combustivel_a","tra_posto_combustivel_p","tra_sinalizacao_p","tra_travessia_l","tra_travessia_p","tra_travessia_pedestre_l","tra_travessia_pedestre_p","tra_trecho_duto_l","tra_trecho_ferroviario_l","tra_trecho_hidroviario_l","tra_trecho_rodoviario_l","tra_trilha_picada_l","tra_tunel_l","tra_tunel_p","veg_brejo_pantano_a","veg_caatinga_a","veg_campinarana_a","veg_campo_a","veg_cerrado_cerradao_a","veg_estepe_a","veg_floresta_a","veg_macega_chavascal_a","veg_veg_area_contato_a","veg_veg_cultivada_a","veg_veg_restinga_a","_Measurements_of_adm_posto_pol_rod_a ","_Invalid_geometries_of_hid_trecho_drenagem_l ","v_eixo_rodoviario_ca_cete"]
            tablesRJ25=["equip_agropec","edif_comerc_serv","area_abast_agua","area_edificada","area_agropec_ext_veg_pesca","barragem","caminho_aereo","campo","complexo_comunicacao","complexo_habitacional","delimitacao_fisica","comporta","edif_constr_est_med","edif_rodoviaria","edif_saude","eixo_rodoviario","grupo_transformadores","sumidouro_vertedouro","ponto_extremo","ponto_duto","edif_pub_militar","posto_pol_rod","area_ext_mineral","area_de_litigio","plataforma","edif_const_turistica","galeria_bueiro","limite_massa_dagua","zona_lin_ener_comunicacao","terreno_sujeito_inundacao","linha_de_limite","org_agropec_ext_veg_pesca","obstaculo_navegacao","ponto_hipsometrico","lin_lim_localidade","recife","reservatorio_hidrico","edificacao","lin_lim_ar_pol_admin","edif_constr_aeroportuaria","girador_ferroviario","nome_local","org_civ_mil_org_civ_mil","org_civil_militar","ponte","ponto_hidroviario","torre_energia","trecho_comunic","ponto_drenagem","marco_de_limite","corredeira","queda_dagua","ar_lit_linha_de_limite","area_politico_admin","torre_comunic","veg_area_contato","area_energia_eletrica","est_med_fen_est_med_fen","via_rodoviaria","area_duto","edif_habitacional","piscina","posic_geo_localidade","travessia","area_urbana_isolada","estrut_transporte","trecho_curso_dagua","edif_religiosa","terreno_exposto","passag_elevada_viaduto","pista_competicao","area_comerc_serv","area_umida","subest_trans_dist_ener_elet","cremalheira","foz_maritima","pto_est_med_fenomenos","area_religiosa","org_industrial","est_med_fenomenos","isolinha_hipsometrica","elemento_fisiografico","area_ensino","duto","estrut_transp_patio","natureza_fundo","edif_const_portuaria","hidrovia","trecho_drenagem","sinalizacao_hidrovia","ar_especial_lin_lim","area_saude","localidade","campo_quadra","ponto_rodoviario_fer","area_est_med_fenomenos","bacia_hidrografica","entroncamento","org_civil_militar_ar_es","ponto_trecho_energia","trecho_hidroviario","complexo_lazer","sinalizacao","org_civ_mil_edif_pub_civil","area_estrut_transporte","deposito_geral","dep_saneamento","identificador_trecho_rod","coreto_tribuna","area_comunicacao","area_lazer","funicular","edif_agropec_ext_veg_pesca","tunel","complexo_abast_agua","pto_geod_topo_controle","banco_areia","edif_saneamento","trecho_ferroviario","edif_metro_ferroviaria","eclusa","complexo_saneamento","via_ferrea","faixa_seguranca","area_servico_social","edif_ensino","travessia_pedestre","edif_abast_agua","inst_pub_inst_pub","org_comerc_serv","area_habitacional","edif_pub_civil","area_descontinuidade","ar_lit_ar_pol_admin","cemiterio","passagem_nivel","trecho_energia","dep_abast_agua","curso_dagua","edif_servico_social","fundeadouro","posto_combustivel","atracadouro","quebramar_molhe","trecho_duto","massa_dagua","pista_ponto_pouso","area_industrial","patio","ruina","antena_comunic","edif_const_lazer","edif_industrial","vegetacao","arquibancada","local_critico","tmp_checa_kickback","org_ext_mineral","edif_energia","edif_comunic","area_saneamento","edif_ext_mineral","fonte_dagua","area_de_propriedade_part","veg_cultivada","compl_ger_energia_eletrica","area_ruinas","trecho_rod_via_rod","posto_fiscal","rocha_em_agua","instituicao_publica","ext_mineral","est_gerad_energia_eletrica","area_especial","ar_prop_part_lin_lim"]
            viewsRJ25.sort()
            tablesRJ25.sort()
           
            estados=["SC","PR","RJ","SP","MS","DF","MG","GO","SE","AL","BA","RO","MT","PE","AC","PB","TO","RN","CE","PI","MA","AM","PA","AP","ES","RS","RR","BRASIL"]
            bases = ["bc100grj_base","bc250_base","bcim_base","sc10_base","ptcon_base","rj25_base"]
            
            base=self.dlg.comboBox2.currentText()
            
            if (self.dlg.checkBox.isChecked() or self.dlg.checkBox2.isChecked())== False:
                msg.exec_()
            
            if base == 'bc100grj_base':
                for e in estados:
                    if self.dlg.comboBox.currentText() == e:
                        if self.dlg.checkBox.isChecked():
                            for v in viewsbc100:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , v , "geom",eval(e), "id_objeto")
                                qgis.utils.iface.addVectorLayer(uri.uri(), v + "_"+e, "postgres")
                                
                        if self.dlg.checkBox2.isChecked():    
                            for t in tablesbc100:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , t , "geom",eval(e))
                                qgis.utils.iface.addVectorLayer(uri.uri(), t + "_"+e, "postgres")
                        
                            
                    
                
            if base == 'bc250_base':
                for e in estados:
                    if self.dlg.comboBox.currentText() == e:
                        if self.dlg.checkBox.isChecked():
                            for v in viewsBC250:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , v , "geom",eval(e), "id_objeto")
                                qgis.utils.iface.addVectorLayer(uri.uri(), v + "_"+e, "postgres")
                                
                        if self.dlg.checkBox2.isChecked():    
                            for t in tablebc250:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , t , "geom",eval(e))
                                qgis.utils.iface.addVectorLayer(uri.uri(), t + "_"+e, "postgres")
                                
                                
            if base == 'bcim_base':
                for e in estados:
                    if self.dlg.comboBox.currentText() == e:
                        if self.dlg.checkBox.isChecked():
                            for v in viewsbcim:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , v , "geom",eval(e), "id_objeto")
                                qgis.utils.iface.addVectorLayer(uri.uri(), v + "_"+e, "postgres")
                                
                        if self.dlg.checkBox2.isChecked():    
                            for t in tablesbcim:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , t , "geom",eval(e))
                                qgis.utils.iface.addVectorLayer(uri.uri(), t + "_"+e, "postgres")
                                
                                
            if base == 'sc10_base':
                for e in estados:
                    if self.dlg.comboBox.currentText() == e:
                                
                        if self.dlg.checkBox2.isChecked():    
                            for t in tablesSC10:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , t , "geom",eval(e))
                                qgis.utils.iface.addVectorLayer(uri.uri(), t + "_"+e, "postgres")
                                
                                
            if base == 'ptcon_base':
                for e in estados:
                    if self.dlg.comboBox.currentText() == e:
                        if self.dlg.checkBox.isChecked():
                            for v in viewsPTCON:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , v , "geom",eval(e), "id_objeto")
                                qgis.utils.iface.addVectorLayer(uri.uri(), v + "_"+e, "postgres")
                                
                        if self.dlg.checkBox2.isChecked():    
                            for t in tablesPTCON:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , t , "geom",eval(e))
                                qgis.utils.iface.addVectorLayer(uri.uri(), t + "_"+e, "postgres")
                                
                                
            if base == 'rj25_base':
                for e in estados:
                    if self.dlg.comboBox.currentText() == e:
                        if self.dlg.checkBox.isChecked():
                            for v in viewsRJ25:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , v , "geom",eval(e), "id_objeto")
                                qgis.utils.iface.addVectorLayer(uri.uri(), v + "_"+e, "postgres")
                                
                        if self.dlg.checkBox2.isChecked():    
                            for t in tablesRJ25:
                                uri = QgsDataSourceURI()
                                uri.setConnection("xposlucas02v", "5432", "gisdb", "", "")
                                uri.setDataSource(base , t , "geom",eval(e))
                                qgis.utils.iface.addVectorLayer(uri.uri(), t + "_"+e, "postgres")
           
                    
                        
                    
                    
                
    
    