from marshmallow import Schema, fields, ValidationError, validates, post_load, validate


class PaymentSchema(Schema):
    id = fields.UUID(required=True, nullable=False, validate=validate.Length(min=1, error="String too short"))
    contributor = fields.String(validate=validate.Length(min=1, error="String too short"))
    amount = fields.Float()
    date = fields.LocalDateTime(validate=validate.Length(min=1, error="String too short"))
    contract_id = fields.UUID(
        required=True,
        validate=validate.Length(min=36, error="String too short"),
        error_meassages={"required": "Contact ID is required."},
    )

    @validates("amount")
    def validate_amount(self, amount):
        if not float(amount):
            raise ValidationError("Amount have wrong format. Only whole numbers.")

    @validates("contributor")
    def validate_contributor(self, contributor):
        if len(contributor) > 30:
            raise ValidationError("Too much symbols")

    @post_load
    def to_model(self, data):
        return data
