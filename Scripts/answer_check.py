import pandas as pd
import numpy as np

class transform_answers:
    """ Class to check the correct users answers against an answer sheet:
    transform_answers(answers).add_correct_answers(user_answer, 1,3) """

    def __init__(self, correct_answers):
        self.correct = correct_answers
    
    def compare_columns(self,column_1, column_2):
        return column_1 == column_2

    def add_correct_answers(self, data, col_from, col_to):
        col_names = data.iloc[:, col_from : col_to].columns
        self.temp = pd.merge(data, self.correct,  on = "Question_id")
        for i in col_names:
            self.temp[i + "_correct"] = self.compare_columns(self.temp[i], self.temp[i+"_Answer"]).apply(lambda x: int(x))
        return self.temp