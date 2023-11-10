from odoo import fields ,api ,models


class PurchaseRequestLine(models.Model):
    _name ="purchase.request"
    _description = 'Purchase Request'
    
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], string='State', default='draft')
    analytical_account_id = fields.Many2one('account.analytic.account', string='Analytical Account')
    creation_date = fields.Datetime(string='Creation Date', default=lambda self: fields.Datetime.now(), readonly=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True)
    requested_by = fields.Many2one('res.users', string='Requested By')
    requested_on = fields.Date(string='Requested On', default=fields.Date.context_today)
    request_line_ids = fields.One2many('purchase.request.line', 'request_id', string='Purchase Request Lines')
    
    related_purchase_orders = fields.One2many(
        comodel_name='purchase.order',
        inverse_name='purchase_request_id',
        string='Related Purchase Orders',
    )
    
    
    
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        for request in self:
            grouped_lines = {}  
            for line in request.request_line_ids:
                vendor_id = line.vendor_id.id
                if vendor_id not in grouped_lines:
                    grouped_lines[vendor_id] = self.env['purchase.request.line'].browse([])
                grouped_lines[vendor_id] |= line

            for vendor_id, lines in grouped_lines.items():
                purchase_order = self.env['purchase.order'].create({
                    'partner_id': vendor_id,
                })
                for line in lines:
                    self.env['purchase.order.line'].create({
                        'order_id': purchase_order.id,
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity,
                        
                        
                    })
                    
            
            
          

    

            
        request.write({'state': 'confirmed'})
        

    def action_cancel(self):
        self.write({'state': 'draft'})

    
    


       
    
    
class PurchaseRequestLine(models.Model):
   
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    product_id = fields.Many2one('product.product', string='Product')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    quantity = fields.Float(string='Quantity')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure' ,domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    request_id = fields.Many2one('purchase.request', string='Purchase Request')

    
    
class PurchaseOrder(models.Model):
    
    _inherit = 'purchase.order'

    purchase_request_id = fields.Many2one('purchase.request', string='Purchase Request' )
    
    
    
    
    
    
    # purchase_request_ids = fields.Many2many('purchase.order', string='Purchase Orders', compute='_compute_purchase_request')

     
  
    # def _compute_purchase_request(self):
    #   for order in self:
    #     purchase_request = self.env['purchase.request'].search([(self.id,'=',order.id)])
    #     order.purchase_request_id = purchase_request.browse([0])
    #     print(order.purchase_request_id)
    
    # def open_one2many_line(self):
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Related Purchase Request',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'res_model': 'purchase.request',
    #             'res_id': self.purchase_request_id.id,
    #             'target': 'current',
    #         }
    
    
    
    
    
    