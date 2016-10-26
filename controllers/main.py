# -*- coding: utf-8 -*-
# Copyright 2015 bloopark systems (<http://bloopark.de>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.report.controllers.main import ReportController
from openerp.addons.web.http import route, request
from openerp.tools.safe_eval import safe_eval as eval

import cStringIO
import re

from werkzeug import exceptions

try:
    from elaphe import barcode
except ImportError:
    pass


class ReportBarcodeController(ReportController):

    """The class of Report controller"""

    @route()
    def report_barcode(self, type, value, width=0, height=0,
                       humanreadable=0, **kw):
        """Contoller able to render barcode images thanks to elaphe.
        Samples:
            <img t-att-src="'/report/barcode?type=%s&amp;value=%s&amp;scale=%s&amp;extraopts=%s' %
                ('code128', o.name, 4.0, 'backgroundcolor:FFFF00,barcolor:00FFFF')"/>

        :param type: Accepted types: 'auspost', 'azteccode', 'codabar',
        'code11', 'code128', 'code25', 'code39', 'code93', 'datamatrix', 'ean',
        'i2of5', 'japanpost', 'kix', 'maxicode', 'msi', 'onecode', 'pdf417',
        'pharmacode', 'plessey', 'postnet', 'qrcode', 'royalmail', 'rss14',
        'symbol', 'upc'
        :param width: Accepted positive integer values
        :param height: Accepted positive integer values
        :param humanreadable: Used in the default method
        :param kw: Accepted values: 'elaphe' is 0 or 1, 'scale' and barmargin
        are float, and 'extraopts' is barcode settings(check elaphe doc)
        """
        if not int(kw.get('elaphe', 0)):
            return super(ReportBarcodeController, self).report_barcode(
                type, value, width, height, humanreadable
            )

        width = int(width)
        height = int(height)
        scale = float(kw.get('scale', 2.0))
        margin = float(kw.get('barmargin', 0))
        extra_opts = {}
        barcode_out = cStringIO.StringIO()
        if kw.get('extraopts', False):
            for opt in kw['extraopts'].split(','):
                key = opt.split(':')[0]
                values = opt.split(':')[1]
                if re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', values) is None:
                    values = eval(values)
                extra_opts[key] = values
        print type, str(value), extra_opts, scale, margin
        try:
            barcode_img = barcode(type, str(value), extra_opts, scale=scale,
                                  margin=margin)
            if width and height:
                barcode_img = barcode_img.resize((width, height))
            barcode_img.save(barcode_out, "png", resolution=100.0)
        except (ValueError, AttributeError):
            raise exceptions.HTTPException(
                description='Cannot convert into barcode.')

        return request.make_response(barcode_out.getvalue(),
                                     headers=[('Content-Type', 'image/png')])

