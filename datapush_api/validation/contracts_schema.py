from marshmallow import Schema, fields, validates, validate, ValidationError


class BandContractsSchema(Schema):
    id = fields.UUID()
    title = fields.String(
        validate=validate.Length(min=1, error="String too short")
    )
    customer = fields.String(
        validate=validate.Length(min=1, error="String too short")
    )
    executor = fields.String(
        validate=validate.Length(min=1, error="String too short")
    )
    start_date = fields.Date()
    end_date = fields.Date()
    amount = fields.Float()

    @validates("amount")
    def validate_amount(self, amount):
        if not float(amount):
            raise ValidationError(
                "Amount have wrong format. Only whole numbers."
            )
