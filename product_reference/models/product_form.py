# -*- coding: utf-8 -*-

import math
import re
from odoo import api, models


class ProductAutoBarcode(models.Model):
    _inherit = 'product.product'

    def your_action_method(self):
        for rec in self:
            rec.default_code = 'PL{}'.format(rec.id)

    @api.model
    def create(self, vals):
        res = super(ProductAutoBarcode, self).create(vals)
        counter = self.env['product.product'].search_count([])
        res.default_code = 'PL {}'.format(counter)
        return res


def ean_checksum(eancode):
    """returns the checksum of an ean string of length 6, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 6:
        return -1

    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    """returns True if eancode is a valid ean6 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 6:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])


def generate_ean(ean):
    """Creates and returns a valid ean6 from an invalid one"""
    if not ean:
        return "000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:6]
    if len(ean) < 6:
        ean = 'PL' + ean + '0' * (6 - len(ean))
    return ean[:-1] + str(ean_checksum(ean))


class ProductTemplateAutoBarcode(models.Model):
    _inherit = 'product.template'



    def your_action_method(self):
        for rec in self:
            rec.default_code = 'PL{}'.format(rec.id)


    @api.model
    def create(self, vals_list):
        templates = super(ProductTemplateAutoBarcode, self).create(vals_list)
        counter = self.env['product.template'].search_count([])
        templates.default_code = 'PL{}'.format(counter)
        return templates
