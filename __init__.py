# -*- coding: utf-8 -*-
"""
/***************************************************************************
 testecm
                                 A QGIS plugin
 testecm
                             -------------------
        begin                : 2016-01-15
        copyright            : (C) 2016 by Lidia
        email                : lidiakonno@hotmail.com
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
    """Load testecm class from file testecm.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .testecm import testecm
    return testecm(iface)
