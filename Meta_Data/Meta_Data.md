# Meta Data

Table_1: Chose_test_res
    -> user_id
    -> item_id
    -> status
    -> test_id
    -> time

Table_2: drag_test_res
    -> user_id
    -> test_id
    -> time
    -> global_lesson_id

Table_3: hardest_age_res
    -> user_id
    -> test_id
    -> answer
    -> time
    -> status

Table_4: Lessons_test
    -> test_id
    -> type
    -> lesson_id
    -> sorting

Table_5: pre_tests_res
    -> user_id
    -> test_id
    -> answer
    -> time
    -> count
    -> status
    -> date

Table_6: pre_test_id
    -> pre_test_id
    -> question
    -> answer_#

Table_7: user_pretests_all
    -> user_id
    -> lesson_id
    -> lesson_status
    -> point
    -> date

Table_8: user_test_state
    -> user_id
    -> status
    -> grade
    -> lesson_id
    -> point
    -> lesson_type
    -> type


========================================================================================

For summative evaluation the following tables will be processed:

    ->
    ->

For formative evaluation the following tables will be processed:

    ->
    ->

=======================================================================================
Data processing pipline:

Collect (SQLDB) -> Data transformation and cleaning -> store in a remote DB -> Analyze it (repeat the process on a scheduler).

Collect: This step includes:
    -> Connecting to the remote server
    -> Connecting to the SQL DB on that server
    -> Send SQL Queries
    -> Store the tabels

Data transformation:
    -> Check & Transform: In this step first we check for irregularities and implememnt transformation if needed. By the end of this step we need to have
    the database in such format that can be analyized.
        -> Checking the expected data type vs the observed one (e.g., time stemps, int, str etc.):
            -> if returns false -> implement data type transformations
                -> check again
                    -> if false -> store a warning and pass the results to the next stage: Send a notification to the analyist. 
            -> if retunrs true -> register as success and store the message
        -> Check whether the results in each table column fall into an expected range:
            -> if returns false register a warning and store it (notify the analyist)
        -> Check for missing data (percentage of missing per column, table and overall) and report to the analyist:

