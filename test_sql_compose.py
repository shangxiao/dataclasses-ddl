# def column_sql_psycopg2(field):
#    name = sql.Identifier(field.name)
#
#    field_type = get_field_type(field)
#    db_type = sql.SQL(DB_TYPE_MAP[field_type])
#
#    constraint_details = {
#        "not_null": field.default is not None,
#        "default": (
#            quote_value(field.default)
#            if field.default is not None and type(field.default) != _MISSING_TYPE
#            else False
#        ),
#        "pk": field.name == "pk",
#        "fk": field.name if is_fk(field) else False,
#        "enum": (
#            (field.name, ", ".join(quote_value(value) for value in field.type))
#            if issubclass(field.type, Enum)
#            else False
#        ),
#    }
#    constraints = [
#        sql.SQL(constraint_map(constraint, value))
#        for constraint, value in constraint_details.items()
#        if value
#    ]
#
#    return sql.SQL(" ").join([name, db_type] + constraints)


# def create_table_sql_psycopg2(model_class):
#     table_name = sql.Identifier(model_class.__name__.lower())
#     columns = [column_sql_psycopg2(field) for field in fields(model_class)]
#     # constraints = ""
#
#     return sql.SQL("CREATE TABLE {table_name} ({columns}){constraints}").format(
#         table_name=table_name,
#         columns=sql.SQL(", ").join(columns),
#         constraints=sql.SQL(""),
#         # "constraints": constraints,
#     )
