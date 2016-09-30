# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Gerarvisao
                                 A QGIS plugin
 Gera uma visão da base restringindo por estado
                             -------------------
        begin                : 2016-06-20
        copyright            : (C) 2016 by Silas Bittencourt
        email                : silas.bittencourt.k@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Gerarvisao class from file Gerarvisao.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Gerarvisao import Gerarvisao
    return Gerarvisao(iface)
