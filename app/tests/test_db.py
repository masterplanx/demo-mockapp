from sqlalchemy import Table, MetaData, create_engine
engine = create_engine('postgresql+psycopg2://username:secretpassword@demodb-postgresql.jx.svc.cluster.local/my-database')
with engine.connect() as conn:
  conn.execute("SELECT VERSION()")
  meta = MetaData()
  referring = Table('guests', meta,
  autoload=True, autoload_with=conn)
