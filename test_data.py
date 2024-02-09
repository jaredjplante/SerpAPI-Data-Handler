import main


def test_web_data():
    job_count = main.testable_get_job_results()
    assert job_count >= 50


def test_database():
    conn, cursor = main.open_db("test.sqlite")
    main.setup_db(cursor)
    main.write_to_database("Test Title",
                           "Test Company",
                           "Test Location",
                           "50000 days ago",
                           "This is a test description!",
                           "5 dollars",
                           "Yes",
                           "Must have 10 years of experience",
                           cursor)
    cursor.execute("SELECT company, location, age, salary FROM listings WHERE title = 'Test Title'")
    record = cursor.fetchone()
    assert record[0] == "Test Company"
    assert record[1] == "Test Location"
    assert record[2] == "50000 days ago"
    assert record[3] == "5 dollars"
    main.close_db(conn)
