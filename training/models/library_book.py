from odoo import models, fields, api
from datetime import timedelta


class LibraryBook(models.Model):
    _name = 'library.book'
    name = fields.Char('Title',required=True)
    date_release = fields.Date('Release Date')
    author_id = fields.Many2many('res.partner',string='auhtors')
    short_name = fields.Char('Short Title')
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State')
    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    # date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages')
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4),  # Optional precision (total, decimals),
    )
    cost_price = fields.Float('Book Cost', digits='Book Price')
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # optional: currency_field='currency_id',
    )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    category_id = fields.Many2one('library.book.category')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,  # optional
        compute_sudo=True  # optional
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
         'Book title must be unique.'),
        ('positive_page', 'CHECK(pages>0)',
         'No of pages must be positive')
    ]

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.validationError('Release Date must be in the past:')

    @api.depends('date_release')
    def _compute_age(self):
        today=fields.Date.today()
        for book in self:
            if book.date_release:
                delta=today-book.date_release
                book.age_days=delta.days
            else:
                book.age_days=0

    def _inverse_age(self):
        today = fields.Date.today()

        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    def name_get(self):
        result = []

        for record in self:
            result.append(
            (record.id,
             u"%s (%s)" % (record.name, record.date_release)
             ))
        return result

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
    # convert the operator:
    # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]


class ResPartner(models.Model):
    _inherit = 'res.partner'
    published_books_id = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids=fields.Many2many('library.book',string='Authored Books')


