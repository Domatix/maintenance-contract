# -*- coding: utf-8 -*-
from openerp import models, fields, api
import base64

class AccountAnalyticAccountInherit(models.Model):
    _inherit = 'account.analytic.invoice.line'

    @api.onchange('product_id')
    def on_change_productid_update_images_ids(self): 
        image_lines = []
        for imageProduct in self.product_id.image_ids: 
             image_lines.append((0,0,{
                        'image':imageProduct.image,
                        'image_fname': imageProduct.image_fname
                        }))           
        self.update({'image_ids':image_lines})        
    
    

    image_ids = fields.One2many(
        'line.images',
        'line_id',
        string='Line Images'
        )

    attachment_image_variant_id = fields.Many2one(
        'ir.attachment',
        string='Attachment'
        )
    image_variant = fields.Binary(
        string='Image Variant', 
        filters='*.png,*.jpg,*.gif',
        compute='_get_attachment_image_variant',
        inverse='_set_attachment_image_variant',
        )
    
    @api.one
    def _get_attachment_image_variant(self):
        self.image = self.attachment_image_variant_id and self.attachment_image_variant_id.datas

    @api.one
    def _set_attachment_image_variant(self):
        if self.image:
            #tools.image_resize_image_big(value)
            values = {
                'datas':self.image_variant,
                'name': self.image_fname,
                'datas_fname': self.image_fname,
                #'res_model': 'product.image',
                #'res_id': self.id,
            }
            attachment = self.env['ir.attachment'].create(values)
            self.attachment_image_variant_id = attachment.id


class ProductImages(models.Model):

    _name = "line.images"
    _rec_name = "image_fname"

    line_id = fields.Many2one(
        'account.analytic.invoice.line',
        string='Line'
        )
    attachment_id = fields.Many2one(
        'ir.attachment',
        string='Attachment'
        )
    image = fields.Binary(
        string='Image', 
        filters='*.png,*.jpg,*.gif',
        compute='_get_attachment_image',
        inverse='_set_attachment_image',
        )
    image_fname = fields.Char(
        string='File Name'
        )
    
    @api.one
    def _get_attachment_image(self):
        self.image = self.attachment_id and self.attachment_id.datas

    @api.one
    def _set_attachment_image(self):
        if self.image:
            #tools.image_resize_image_big(value)
            values = {
                'datas':self.image,
                'name': self.image_fname,
                'datas_fname': self.image_fname,
                #'res_model': 'product.image',
                #'res_id': self.id,
            }
            attachment = self.env['ir.attachment'].create(values)
            self.attachment_id = attachment.id

    