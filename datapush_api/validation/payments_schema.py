from marshmallow import Schema, fields, validates, validate, ValidationError


class BandPaymentsSchema(Schema):
    id = fields.UUID()
    contract_id = fields.UUID()
    contributor = fields.String(
        validate=validate.Length(min=1, error="String too short")
    )
    date = fields.Date()
    amount = fields.Float()

    @validates("amount")
    def validate_amount(self, amount):
        if not float(amount):
            raise ValidationError(
                "Amount have wrong format. Only whole numbers."
            )
