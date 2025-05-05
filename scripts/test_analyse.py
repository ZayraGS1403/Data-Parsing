import unittest
import pandas as pd
import numpy as np
import os
from .analyse import (
    load_and_clean_data,
    plot_salary_vs_age,
    plot_days_service_vs_vacation,
    plot_salary_distribution,
    plot_gender_salary_distribution,
    plot_gender_performance_distribution,
    plot_performance_distribution,
    plot_department_distribution,
    plot_gender_distribution,
    plot_education_distribution,
    plot_city_distribution,
    plot_state_distribution,
    plot_employee_level_distribution,
    plot_work_location_distribution,
    plot_shift_distribution,
    plot_status_distribution,
    analyze_data,
)

class TestEmployeeDataAnalysis(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.sample_data = pd.DataFrame(
            {
                "employee_id": ["EMP000000001", "EMP000000001", "EMP000000003"],  # Duplicate ID
                "first_name": ["Justin", "William", "Brian"],
                "last_name": ["Dodson", "Mendoza", "Garcia"],
                "email": [
                    "justin.dodson@company.com",
                    "william.mendoza@company.com",
                    "brian.garcia@company.com",
                ],
                "phone_number": [
                    "+1-268-903-3140x814",
                    "961-703-7758x823",
                    "+1-923-424-9237x232",
                ],
                "department": ["Marketing", "Logistics", "Legal"],
                "job_title": ["Content Strategist", "Logistics Manager", "Contract Specialist"],
                "hire_date": ["2021-04-01", "2020-05-17", "2021-09-07"],
                "days_service": [1491, 1810, 1332],
                "base_salary": [43300.94, 48293.73, 114368.52],
                "bonus_percentage": [2.71, 7.24, 6.61],
                "status": ["Active", "Active", "Active"],
                "birth_date": ["1974-07-08", "1980-05-30", "1971-08-21"],
                "address": [
                    "642 Albert Plaza",
                    "654 Bethany Prairie Suite 186",
                    "51257 Murray Crest Apt. 425",
                ],
                "city": ["Spokane", "New York", "Atlanta"],
                "state": ["WA", "NY", "GA"],
                "zip_code": ["83520", "20774", "34870"],
                "country": ["USA", "USA", "USA"],
                "gender": ["M", "M", "M"],
                "education": ["High School", "Professional", "Master"],
                "performance_score": [75.6, 68.62, 71.62],
                "last_review_date": ["2021-12-26", "2021-08-15", "2023-11-28"],
                "employee_level": ["Senior", "Senior", "Senior"],
                "vacation_days": [19, 21, 22],
                "sick_days": [6, 3, 7],
                "work_location": ["Office", "Remote", "Office"],
                "shift": ["Day", "Night", "Night"],
                "emergency_contact": ["6089985520", "644-435-2090x3593", "+1-680-568-0610x0856"],
                "ssn": ["694-96-8839", "741-91-7577", "645-22-0702"],
                "bank_account": [
                    "ISIH09445641824790",
                    "ZWKL89652489774496",
                    "ZLHA11113153048754",
                ],
            }
        )
        # Sample data with negative salary for testing error detection
        self.sample_data_negative_salary = pd.DataFrame(
            {
                "employee_id": ["EMP000000001", "EMP000000002", "EMP000000003"],
                "first_name": ["Justin", "William", "Brian"],
                "last_name": ["Dodson", "Mendoza", "Garcia"],
                "email": [
                    "justin.dodson@company.com",
                    "william.mendoza@company.com",
                    "brian.garcia@company.com",
                ],
                "phone_number": [
                    "+1-268-903-3140x814",
                    "961-703-7758x823",
                    "+1-923-424-9237x232",
                ],
                "department": ["Marketing", "Logistics", "Legal"],
                "job_title": ["Content Strategist", "Logistics Manager", "Contract Specialist"],
                "hire_date": ["2021-04-01", "2020-05-17", "2021-09-07"],
                "days_service": [1491, 1810, 1332],
                "base_salary": [43300.94, -5000.00, 114368.52],  # Negative salary
                "bonus_percentage": [2.71, 7.24, 6.61],
                "status": ["Active", "Active", "Active"],
                "birth_date": ["1974-07-08", "1980-05-30", "1971-08-21"],
                "address": [
                    "642 Albert Plaza",
                    "654 Bethany Prairie Suite 186",
                    "51257 Murray Crest Apt. 425",
                ],
                "city": ["Spokane", "New York", "Atlanta"],
                "state": ["WA", "NY", "GA"],
                "zip_code": ["83520", "20774", "34870"],
                "country": ["USA", "USA", "USA"],
                "gender": ["M", "M", "M"],
                "education": ["High School", "Professional", "Master"],
                "performance_score": [75.6, 68.62, 71.62],
                "last_review_date": ["2021-12-26", "2021-08-15", "2023-11-28"],
                "employee_level": ["Senior", "Senior", "Senior"],
                "vacation_days": [19, 21, 22],
                "sick_days": [6, 3, 7],
                "work_location": ["Office", "Remote", "Office"],
                "shift": ["Day", "Night", "Night"],
                "emergency_contact": ["6089985520", "644-435-2090x3593", "+1-680-568-0610x0856"],
                "ssn": ["694-96-8839", "741-91-7577", "645-22-0702"],
                "bank_account": [
                    "ISIH09445641824790",
                    "ZWKL89652489774496",
                    "ZLHA11113153048754",
                ],
            }
        )
        # Save sample data to temporary CSV files
        self.temp_file = "temp_sample_data.csv"
        self.sample_data.to_csv(self.temp_file, index=False)
        self.temp_file_negative_salary = "temp_sample_data_negative_salary.csv"
        self.sample_data_negative_salary.to_csv(self.temp_file_negative_salary, index=False)

    def test_load_and_clean_data(self):
        # Test with the temporary file (normal data)
        df = load_and_clean_data(self.temp_file)
        self.assertFalse(df.empty)
        self.assertTrue(all(df["base_salary"] >= 0))
        self.assertTrue(all(df["performance_score"] >= 0))
        self.assertTrue(all(df["performance_score"] <= 100))
        self.assertTrue(all(df["age"] >= 18))
        self.assertTrue(all(df["birth_date"] <= pd.Timestamp("2025-05-01")))
        self.assertTrue(all(df["hire_date"] <= pd.Timestamp("2025-05-01")))
        self.assertTrue(all(df["last_review_date"] <= pd.Timestamp("2025-05-01")))
        self.assertIn("age", df.columns)

        # Test with negative salary data
        df = load_and_clean_data(self.temp_file_negative_salary)
        self.assertEqual(len(df), 2)  # Should remove the row with negative salary
        self.assertTrue(all(df["base_salary"] >= 0))

        # Test with the actual dataset file (if available)
        if os.path.exists("scripts/employee_data.csv"):
            df = load_and_clean_data("scripts/employee_data.csv")
            self.assertFalse(df.empty)

    def test_plot_salary_vs_age(self):
        df = load_and_clean_data(self.temp_file)
        plot_salary_vs_age(df)
        self.assertTrue(os.path.exists("plotsBig/salary_vs_age.png"))
        os.remove("plotsBig/salary_vs_age.png")

    def test_plot_days_service_vs_vacation(self):
        df = load_and_clean_data(self.temp_file)
        plot_days_service_vs_vacation(df)
        self.assertTrue(os.path.exists("plotsBig/days_service_vs_vacation.png"))
        os.remove("plotsBig/days_service_vs_vacation.png")

    def test_plot_salary_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_salary_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/salary_distribution.png"))
        os.remove("plotsBig/salary_distribution.png")

    def test_plot_gender_salary_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_gender_salary_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/gender_salary_distribution.png"))
        os.remove("plotsBig/gender_salary_distribution.png")

    def test_plot_gender_performance_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_gender_performance_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/gender_performance_distribution.png"))
        os.remove("plotsBig/gender_performance_distribution.png")

    def test_plot_performance_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_performance_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/performance_distribution.png"))
        os.remove("plotsBig/performance_distribution.png")

    def test_plot_department_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_department_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/department_distribution.png"))
        os.remove("plotsBig/department_distribution.png")

    def test_plot_gender_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_gender_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/gender_distribution.png"))
        os.remove("plotsBig/gender_distribution.png")

    def test_plot_education_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_education_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/education_distribution.png"))
        os.remove("plotsBig/education_distribution.png")

    def test_plot_city_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_city_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/city_distribution.png"))
        os.remove("plotsBig/city_distribution.png")

    def test_plot_state_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_state_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/state_distribution.png"))
        os.remove("plotsBig/state_distribution.png")

    def test_plot_employee_level_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_employee_level_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/employee_level_distribution.png"))
        os.remove("plotsBig/employee_level_distribution.png")

    def test_plot_work_location_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_work_location_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/work_location_distribution.png"))
        os.remove("plotsBig/work_location_distribution.png")

    def test_plot_shift_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_shift_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/shift_distribution.png"))
        os.remove("plotsBig/shift_distribution.png")

    def test_plot_status_distribution(self):
        df = load_and_clean_data(self.temp_file)
        plot_status_distribution(df)
        self.assertTrue(os.path.exists("plotsBig/status_distribution.png"))
        os.remove("plotsBig/status_distribution.png")

    def test_analyze_data(self):
        df = load_and_clean_data(self.temp_file)
        analysis = analyze_data(df)
        self.assertIn("salary_stats", analysis)
        self.assertIn("performance_stats", analysis)
        self.assertIn("vacation_days_stats", analysis)
        self.assertIn("normality", analysis)
        self.assertFalse(analysis["normality"]["base_salary"]["is_normal"])
        self.assertFalse(analysis["normality"]["performance_score"]["is_normal"])
        self.assertFalse(analysis["normality"]["vacation_days"]["is_normal"])

    def tearDown(self):
        # Clean up the temporary CSV files
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.temp_file_negative_salary):
            os.remove(self.temp_file_negative_salary)
        # Clean up the plotsBig directory if it exists
        if os.path.exists("plotsBig"):
            for file in os.listdir("plotsBig"):
                os.remove(os.path.join("plotsBig", file))
            os.rmdir("plotsBig")

if __name__ == "__main__":
    unittest.main()