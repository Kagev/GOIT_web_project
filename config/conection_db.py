import conection_config


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_database_connection(POSTGRES_HOST, POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD):
	return psycopg2.connect(
		host=POSTGRES_HOST,
		database=POSTGRES_NAME,
		user=POSTGRES_USER,
		password=POSTGRES_PASSWORD,
	)


# Функция для выполнения SQL-запросов с возможностью получения результатов как словарей
def execute_query(query, params=None):
	conn = get_database_connection()
	cursor = conn.cursor(cursor_factory=RealDictCursor)
	cursor.execute(query, params)
	result = cursor.fetchall()
	cursor.close()
	conn.close()
	return result
