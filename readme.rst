bp_reportbarcode_elaphe
=================

.. Report barcode elaphe to provide more options of barcodes and settings

This module has been built to override the method _report_barcode_ of the class _ReportController_ and provide more types and settings of barcode.
The behavior is the same as before, as you can see in the snippet below, but we have added a new query parameter(**extraopts**):
```html
<img t-att-src="'/report/barcode/QR/%s' % o.name"/>
```
or
```html
<img t-att-src="'/report/barcode?type=%s&amp;value=%s&amp;width=%s&amp;height=%s' %
                ('QR', o.name, 200, 200)"/>
```

To pass some one of those settings, you need to use the new query parameter **extraopts** and instead you write **option = value**, you need to write **option : value**. Look at this example:
`
extraopts=backgroundcolor:FFFF00,barcolor:00FFFF
`

E.g, HTML img tag:
```html

<img t-att-src="'/report/barcode?type=%s&amp;value=%s&amp;width=%s&amp;height=%s&amp;extraopts=%s' %
                ('CODE128', o.name, 200, 200, 'backgroundcolor:FFFF00,barcolor:00FFFF')"/>

```
The snippet above changes the color of the bars and the background of the barcode.
The new options of setting can be found in the [Barcode Writer in Pure PostScript documentation](https://github.com/bwipp/postscriptbarcode/wiki).
