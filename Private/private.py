# Database access info

config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'unfpa',
    'raise_on_warnings': True
}

query_user_background = ("SELECT us.id, us.sex, us.region, us.city, us.community, us.school, us.grade, us.created_at, us.updated_at, tst.date\
                    FROM user as us\
                    LEFT JOIN user_tests_state as tst\
                    ON us.id = tst.user_id\
                    WHERE tst.lesson_type = 1")

query_pretest_results = ("SELECT us.id, us.sex, us.region, us.city, us.community, us.school, us.grade, tst.test_id, tst.answer, tst.time, tst.`status`, tst.date\
                    FROM user as us\
                    LEFT JOIN pre_tests_res as tst\
                    ON tst.user_id = us.id")

query_questions = ("SELECT id, question, right_answers\
                FROM tests_question")

answers = ("Select id, right_answers\
        FROM tests_question")