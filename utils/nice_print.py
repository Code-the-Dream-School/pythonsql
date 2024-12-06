from sqlalchemy import inspect

def print_records(result_set):
    first = True
    attr_names=[]
    for record in result_set:
        if first:
            first=False
            inst = inspect(record)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
            row1 = '\t'.join(attr_names)
            print(row1)
            print('---------------------------')
        values = []
        for a_name in attr_names:
            att = getattr(record, a_name)
            if att:
                values.append(str(att))
            else:
                values.append("no_value")
        row = '\t'.join(values)
        print(row)

def print_record(record):
    inst = inspect(record)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    row1 = '\t'.join(attr_names)
    print(row1)
    print('---------------------------')
    values = []
    for a_name in attr_names:
        att = getattr(record, a_name)
        if att:
            values.append(str(att))
        else:
            values.append("no_value")
    row = '\t'.join(values)
    print(row)

def print_rows(rows):
    first = True
    for row in rows:
        if first:
            first = False
            keys = row._mapping.keys()
            keynames = '\t'.join(keys)
            print(keynames)
            print('------------------------')
        values = []
        for key in keys:
            values.append(str(row._mapping[key]))
        print('\t'.join(values))