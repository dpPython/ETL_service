from marshmallow import Schema, fields, ValidationError, validates


class ContractSchema(Schema):
    id = fields.UUID(required=True)
    title = fields.String(required=True,
                          error_messages={'required':
                                          {'message': 'Title is required.',
                                           'code': 400
                                           }
                                          }
                          )
    amount = fields.Decimal(required=True,
                            error_messages={'required':
                                            {'message': 'Amount is required.',
                                             'code': 400
                                             }
                                            }
                            )
    start_date = fields.Date(required=True,
                             error_messages={'required':
                                             {'message': 'Start date is '
                                                         'required.',
                                              'code': 400
                                              }
                                             }
                             )
    end_date = fields.Date(required=True,
                           error_messages={'required':
                                           {'message': 'End is required.',
                                            'code': 400
                                            }
                                           }
                           )
    customer = fields.String(required=True,
                             error_messages={'required':
                                             {'message': 'customer is '
                                                         'required.',
                                              'code': 400
                                              }
                                             }
                             )
    executor = fields.String(required=True,
                             error_messages={'required':
                                             {'message': 'executor is '
                                                         'required.',
                                              'code': 400
                                              }
                                             }
                             )

    @validates('amount')
    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError("Amount can't be negative")
