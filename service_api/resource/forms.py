from marshmallow import Schema, fields, ValidationError, validates


class ContractSchema(Schema):
    id = fields.UUID()
    title = fields.String()
    amount = fields.Decimal()
    start_date = fields.Date()
    end_date = fields.Date()
    customer = fields.String()
    executor = fields.String()

    @validates('amount')
    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError("Amount can't be negative")
