from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PosSession(models.Model):
    _name = 'pos.session'
    # picking_ids=self.env['pos.session'].picking_id

    @api.depends('picking_ids', 'picking_ids.state')
    def _compute_picking_count(self):
        for session in self:
            session.picking_count = self.env['stock.picking'].search_count([('pos_session_id', '=', session.id)])
            session.failed_pickings = bool(
                self.env['stock.picking'].search([('pos_session_id', '=', session.id), ('state', '!=', 'done')],
                                                 limit=1))

    def action_view_pos_inventory(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('stock.action_picking_tree_ready')
        action['context'] = {}
        action['domain'] = [('id', 'in', self.picking_ids.ids)]
        return action
        # return {
        #     'name': _('Inventory'),
        #     'res_model': 'stock.picking',
        #     'view_mode': 'tree,form',
        #     'views': [
        #         (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
        #         (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
        #     ],
        #     'type': 'ir.actions.act_window',
        #     'domain': [('session_id', 'in', self.ids)],
        # }

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#     inventory_stock = fields.Many2one('pos.session')