import sqlite3,sys,json

def json2dict(s):
    try:
        decoded_data = json.loads(s)
        if isinstance(decoded_data, str):
            agent_dict = json.loads(decoded_data)
        else:
            agent_dict = decoded_data
    except:
        return {}

    return agent_dict

def process_agent_data(db_path: str):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT session_id, agent_data, runs FROM agno_sessions;"
        cursor.execute(query)

        for session_id, agent_data_str, agent_run_str in cursor.fetchall():
            if not agent_data_str:
                print(f"Session ID: {session_id} -> No agent_data found.")
                continue

            agent_data_dict = json2dict(agent_data_str)
            print(agent_data_dict.keys())

            agent_run_dict = json2dict(agent_run_str)
            print (type(agent_run_dict))

            for l in agent_run_dict:
                if isinstance(l, list):
                    pass
                elif isinstance(l, dict):
                    print(l.keys())
                    print(f"----- {l['model']} ---")
                    if 'tools' in l:
                        print(l['tools'])
                    if 'metrics' in l:
                        print(l['metrics'])


    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # 6. Ensure the database connection is closed
        if conn:
            conn.close()

if __name__ == "__main__":
    # Replace 'your_database.db' with the actual path to your SQLite file
    database_file = sys.argv[1]
    process_agent_data(database_file)
