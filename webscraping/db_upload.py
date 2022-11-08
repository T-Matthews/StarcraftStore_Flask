from sqlalchemy import create_engine

# Import data-frome from creation in 'unit_data'
from unit_data import df
import os


param_dic = {
    "host"      : "heffalump.db.elephantsql.com",
    "database"  : "ysxdgfvu",
    "user"      : "ysxdgfvu",
    "password"  : "AJbaHqPALPhgGHugprwDTOmrhcfLnHos"
}

csv_file = "../data/global-temp-monthly.csv"


connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
    param_dic['user'],
    param_dic['password'],
    param_dic['host'],
    param_dic['database']
)
def to_alchemy(df):
    """
    Using a dummy table to test this call library
    """
    engine = create_engine(connect)
    df.to_sql(
        'units', 
        con=engine, 
        index=False, 
        if_exists='replace'
    )
    print("to_sql() done (sqlalchemy)")


to_alchemy(df)



