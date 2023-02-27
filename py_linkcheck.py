from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import mysql.connector as mysql
import worker

# Agent function
def agent(my_queue):
    # Connect to mysql dBase pool. If this is the first run, make pool else
    # just connect to the pool.
    my_db = mysql.connect(
        option_files="my.ini",
        pool_size=5,
        pool_name="linkcheck"
    )

    # Need cursor to communicate with the dBase pool connection
    cursor = my_db.cursor()
    # float_id is the lowest entry id the script will query
    float_id = 0
    found = False

    while not found:
        # Query dBase for first unused entry with ID above float_id 
        execline = "SELECT * FROM weblinks WHERE Result = 0 AND ID >= "
        execline = execline + str(float_id) + " LIMIT 1; "
        cursor.execute(execline)

        # Grab the returned data in 'results'
        results = cursor.fetchone()
        if cursor.rowcount < 0:
            break

        # Unpack 'results' to get my_id and my_url from the returned data
        (my_id, my_url, *_) = results
        # If float_id < my_id then set it to my_id
        float_id = max(float_id, my_id)

        # If my_id is not in my_queue then it's fresh and can be analysed
        if my_id not in my_queue:
            my_queue.append(my_id)
            found = True
        else:
            # If my_id was already in my_queue then add 1 to float_id and try
            # again
            float_id += 1

    # Set 'Result = 1' so that other agents can't use this id/URL.
    execline = "UPDATE `weblinks` SET `Result` = 1 WHERE `id` =" + str(my_id)
    cursor.execute(execline)
    my_db.commit()

    # OK, find out the response code for calling my_url
    resp_code = worker.webcall(my_url)

    # The call is complete so take my_id out of the my_queue process line
    my_queue.remove(my_id)

    
    # Now submit the response code for my_id with a timestamp to the DB.
    execline = f"UPDATE `weblinks` SET `Result` = '{resp_code}' "

    # Cook up a timestamp
    # now = datetime.now()
    # date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # execline += f", `Date` = '{date_time}' "
    
    execline += f"WHERE `weblinks`.`ID` = '{my_id}';"

    cursor.execute(execline)
    my_db.commit()
    my_db.close()


# Main function
def main():  # sourcery skip: for-index-underscore
    """
    py_linkcheck:
    script to check the availability/validity of a large number of URLs

    Put the URLs into a database and then run the script.
    """
    # workers sets how many (web)agents should be started 
    workers = 5
    # my_queue is a holder so that the agents can check that their URL is not
    # already in use
    my_queue = []

    # Connect to the DB, make a connection pool big enough for all worker procs
    my_db = mysql.connect(
        option_files="my.ini",
        pool_size=workers,
        pool_name="linkcheck"
    )

    cursor = my_db.cursor()
    execline = "SELECT COUNT(*) FROM weblinks WHERE Result = 0"
    cursor.execute(execline)

    # Grab the returned data in 'results'
    jobstodo = cursor.fetchone()[0]
    my_db.close()

    print(f"Target to do: {jobstodo}")

    with ThreadPoolExecutor(max_workers=workers,
        thread_name_prefix='ag-') as executor:
 
        for x in range(jobstodo):
            executor.submit(agent, my_queue)


if __name__ == "__main__":
    main()