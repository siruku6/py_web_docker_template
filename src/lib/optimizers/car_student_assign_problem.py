import pandas as pd
import pulp


class CarGroupOpt:
    def __init__(
        self, df_students: pd.DataFrame, df_cars: pd.DataFrame,
        name: str = "CarStudentCombination"
    ) -> None:
        self.df_students: pd.DataFrame = df_students
        self.df_cars: pd.DataFrame = df_cars
        self.name: str = name

        tmp_dict: dict = self._formulate()
        self.problem: pulp.LpProblem = tmp_dict["problem"]
        self.variables: dict = tmp_dict["variables"]
        self.lists: dict = tmp_dict["lists"]

    def _formulate(self) -> dict:
        prob = pulp.LpProblem(self.name, pulp.LpMinimize)

        # --------------------------------------------------------------
        # Make lists
        # --------------------------------------------------------------
        student_list: list = self.df_students["student_id"].to_list()
        car_list: list = self.df_cars["car_id"].to_list()
        grade_list: list = self.df_students.drop_duplicates(subset=["grade"])["grade"].to_list()

        combinations: list = [
            (student, car)
            for student in student_list
            for car in car_list
        ]
        students_with_license: pd.Series = self.df_students[self.df_students["license"] == 1]["student_id"]
        students_for_each_grade: dict = {
            grade: self.df_students[self.df_students["grade"] == grade]["student_id"]
            for grade in grade_list
        }

        students_male: pd.Series = self.df_students[self.df_students["gender"] == 0]["student_id"]
        students_female: pd.Series = self.df_students[self.df_students["gender"] == 1]["student_id"]
        capacities: list = self.df_cars["capacity"].to_list()

        # --------------------------------------------------------------
        x = pulp.LpVariable.dicts("x", combinations, cat="Binary")

        # --------------------------------------------------------------
        # Constraints
        # --------------------------------------------------------------
        # 学生一人一人に対するconstraints
        for student_id in student_list:
            prob += pulp.lpSum([x[student_id, car_id] for car_id in car_list]) == 1

        # 各車に対するconstraints
        for car_id in car_list:
            prob += pulp.lpSum([x[student_id, car_id] for student_id in student_list]) <= capacities[car_id]
            prob += pulp.lpSum([x[student_id, car_id] for student_id in students_with_license]) >= 1

            for grade in students_for_each_grade.keys():
                prob += pulp.lpSum([x[student_id, car_id] for student_id in students_for_each_grade[grade]]) >= 1

            prob += pulp.lpSum([x[student_id, car_id] for student_id in students_male]) >= 1
            prob += pulp.lpSum([x[student_id, car_id] for student_id in students_female]) >= 1

        return {
            "problem": prob,
            "variables": {"x": x},
            "lists": {"students": student_list, "cars": car_list}
        }

    def solve(self) -> dict:
        status = self.problem.solve()
        status_display: str = pulp.LpStatus[status]
        if status_display != "Optimal":
            return {"success": False, "status": status_display, "result": None}

        assignment_result: dict = {
            car_id: [
                student_id for student_id in self.lists["students"]
                if self.variables["x"][student_id, car_id].value() == 1
            ]
            for car_id in self.lists["cars"]
        }
        # max_people: dict = dict(zip(self.df_cars["car_id"], self.df_cars["capacity"]))

        for car_id, student_ids in assignment_result.items():
            print("Car ID: {}".format(car_id))
            # print("Number of students: {} ({})".format(len(student_ids), max_people[car_id]) )
            print("Student IDs: {}\n".format(student_ids))

        assignment_table: dict = [
            {"student_id": student_id, "car_id": car_id}
            for car_id, students in assignment_result.items()
            for student_id in students
        ]
        df_result: pd.DataFrame = pd.DataFrame(assignment_table)

        return {"success": True, "status": status_display, "result": df_result}
