from typing import Tuple, Optional, Any
import pandas as pd


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part: str) -> Tuple[Optional[str], Optional[str], Optional[Any]]:
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


def default_filter_query(df: pd.DataFrame, filter_query: str) -> pd.DataFrame:
    filtering_expressions = filter_query.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator == 'contains' and type(filter_value) is float:
            filter_value = str(int(filter_value))
        if dff[col_name].dtype.kind == 'O' and type(filter_value) is float:
            dff = dff.loc[getattr(dff[col_name].fillna(0).apply(lambda x: float(x)), operator)(filter_value)]
        elif operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains' and filter_value !='true' and filter_value !='false':
            dff = dff.loc[dff[col_name].str.contains(filter_value).fillna(False)]
        elif operator == 'contains' and filter_value == 'true' or filter_value == 'false':
            bool_val = True if filter_value == 'true' else False
            dff = dff[dff[col_name] == bool_val]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    return dff