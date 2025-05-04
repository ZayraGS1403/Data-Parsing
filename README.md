# Employee Data Analysis Project
  
**Student:** Zayra Gutiérrez Solano

## Objective

The objective of this project is to analyze a synthetic dataset of employee records to identify patterns, relationships, and potential errors in the data. The dataset, `employee_data.csv`, contains employee information such as demographics, employment details, salary, performance scores, and work-related attributes. The project includes data cleaning, validation, visualization, and aims to explore distributions and relationships within the employee data, focusing on achieving a comprehensive understanding of workforce dynamics.

## Methodology

### Data Cleaning and Validation

The script performs the following steps:

- **Data Validation:**
  - Identifies unrealistic values:
    - Salaries: Detects negative salaries.
    - Performance Scores: Ensures scores are within 0-100.
    - Ages: Ensures no employees are under 18.
    - Vacation and Sick Days: Detects negative values.
    - Days of Service: Detects negative values.
  - Validates `employee_id` format (EMP followed by 9 digits).
  - Checks for duplicate `employee_id`.
  - Validates dates (no future dates for `birth_date`, `hire_date`, `last_review_date`).
  - Detects inconsistencies in `days_service` vs. `hire_date` (differences >30 days).

### Data Structure

The `employee_data.csv` file contains the following columns:

| Column                 | Description                                   | Data Type | Notes/Relationships                                            |
|------------------------|-----------------------------------------------|-----------|----------------------------------------------------------------|
| `employee_id`          | Unique employee ID                            | String    | Format: EMP + 9 digits (e.g., 'EMP000000001')                 |
| `first_name`           | Employee's first name                         | String    | N/A                                    |
| `last_name`            | Employee's last name                          | String    | N/A                                    |
| `email`                | Employee's email                              | String    | N/A                                    |
| `phone_number`         | Employee's phone number                       | String    | N/A                                    |
| `department`           | Department name                               | String    | Common: "Operations", "Security", "HHRR"                      |
| `job_title`            | Job title                                     | String    | N/A                                    |
| `hire_date`            | Date of hire (YYYY-MM-DD)                     | Date      | Range: 2020-05-01 to 2025-04-26                               |
| `days_service`         | Days employed                                 | Integer   | Range: 5-1826                                                  |
| `base_salary`          | Annual base salary ($)                        | Float     | Range: 30,000-195,061.88                                       |
| `bonus_percentage`     | Bonus as a percentage of salary               | Float     | Range: 0.0-10.87                                               |
| `status`               | Employment status (Active/Inactive/Leave)     | String    | 76.5% Active, 13.5% Inactive, 10.0% Leave                     |
| `birth_date`           | Date of birth (YYYY-MM-DD)                    | Date      | Range: 1959-07-18 to 2007-02-04                                |
| `address`              | Employee's address                            | String    | N/A                                    |
| `city`                 | City of residence                             | String    | Most frequent: "Springfield" (9.8%)                            |
| `state`                | State of residence                            | String    | Common: "WA", "NY", "GA"                                       |
| `zip_code`             | Zip code                                      | String    | N/A                                    |
| `country`              | Country (all USA)                             | String    | All values: "USA"                                              |
| `gender`               | Gender (M/F/Other)                            | String    | 45% M, 45% F, 10% Other                                        |
| `education`            | Education level                               | String    | 48% Professional, 28% Master, 16% High School, 8% PhD          |
| `performance_score`    | Performance score (0-100)                     | Float     | Range: 44.03-100.0                                             |
| `last_review_date`     | Date of last review (YYYY-MM-DD)              | Date      | Range: 2020-07-14 to 2025-04-30                                |
| `employee_level`       | Employee level (Senior/Mid/Entry)             | String    | 60% Senior, 20% Mid, 19.9% Entry                               |
| `vacation_days`        | Vacation days allocated                       | Integer   | Range: 5-25                                                    |
| `sick_days`            | Sick days allocated                           | Integer   | Range: 0-13                                                    |
| `work_location`        | Work location (Office/Remote/Hybrid)          | String    | 34.5% Office, 32.8% Remote, 32.7% Hybrid                      |
| `shift`                | Work shift (Day/Night/Flexible)               | String    | 34.8% Day, 34.6% Night, 30.6% Flexible                        |
| `emergency_contact`    | Emergency contact number                      | String    | N/A                                    |
| `ssn`                  | Social Security Number                        | String    | N/A                                    |
| `bank_account`         | Bank account number                           | String    | N/A                                    |

### Key Relationships

- **Salary vs. Age by Gender:** No strong correlation between age and salary. Men and women have similar salary distributions (mean ~$65,000).
- **Days of Service vs. Vacation Days by Employee Level:** Senior employees tend to have more days of service and slightly more vacation days.
- **Department Distribution:** Employees are distributed across departments like Operations, Security, and HHRR, with a fairly even spread.
- **Education and Employee Level:** Senior employees are more likely to have a "Master" or "Professional" education level, while Entry-level employees often have "High School" education.
- **City and State Distribution:** Springfield is the most frequent city (9.8%), and states like WA, NY, and GA are common.
- **Performance Scores:** Performance scores are right-skewed (mean ~75), with most employees scoring above 60.

### Data Visualization and Analysis

Visualizations:

#### **1. Distribution of Employees by Gender (`gender_distribution.png`)**

- **Analysis:** Pie chart showing gender distribution: 45% Male, 45% Female, 10% Other. Indicates a balanced gender representation with a notable presence of "Other" gender identities.
- **Good:** Reflects diversity in gender representation.
- **Bad:** The "Other" category may need further breakdown for more detailed analysis.
  


#### **2. Distribution of Employees by Education Level (`education_distribution.png`)**
- **Analysis:** Bar chart showing education levels: 48% Professional, 28% Master, 16% High School, 8% PhD. Suggests a workforce with a high level of professional and advanced education.
- **Good:** Highlights the educational attainment of the workforce.
- **Bad:** Limited categories may not capture all educational backgrounds.

#### **3. Distribution of Employees by City (Top 10) (`city_distribution.png`)**
- **Analysis:** Bar chart showing the top 10 cities: Springfield (9.8%), Atlanta (9.0%), Columbus (8.9%), etc. Indicates a concentration of employees in certain urban areas.
- **Good:** Identifies geographic distribution of employees.
- **Bad:** Only top 10 cities are shown, potentially missing smaller but significant clusters.

#### **4. Performance Score Distribution (`performance_distribution.png`)**
- **Analysis:** Histogram with KDE showing performance scores, right-skewed with a mean around 75. Most employees score above 60, indicating generally good performance.
- **Good:** Reflects overall employee performance trends.
- **Bad:** Skewness may indicate bias in performance evaluations.

#### **5. Distribution of Employees by Employee Level (`employee_level_distribution.png**)**
- **Analysis:** Pie chart showing employee levels: 60% Senior, 20% Mid, 19.9% Entry. Suggests a top-heavy organization with many experienced employees.
- **Good:** Highlights seniority distribution.
- **Bad:** High proportion of Senior employees may indicate limited growth opportunities for Entry-level staff.

#### **6. Distribution of Employees by Department (`department_distribution.png`)**
- **Analysis:** Bar chart showing department distribution: Fairly even across departments like Operations, Security, HHRR, etc. (each ~5-6% of total employees). Indicates a balanced departmental structure.
- **Good:** Reflects organizational diversity in departments.
- **Bad:** Even distribution may not reflect real-world organizational structures.

#### **7. Salary Distribution (`salary_distribution.png`)**
- **Analysis:** Histogram with KDE showing salary distribution, right-skewed with a mean around $65,000. Salaries range from $30,000 to $195,061.88, with a peak around $50,000.
- **Good:** Identifies salary trends and outliers.
- **Bad:** Skewness may indicate salary inequity.

#### **8. Salary vs. Age by Gender (`salary_vs_age.png`)**
- **Analysis:** Scatter plot showing salary vs. age by gender. No strong correlation between age and salary. Men, women, and others have similar salary distributions.
- **Good:** Validates lack of age-salary correlation.
- **Bad:** Dense plot makes it hard to identify specific trends.

#### **9. Days of Service vs. Vacation Days by Employee Level (`days_service_vs_vacation.png`)**
- **Analysis:** Scatter plot showing days of service vs. vacation days, colored by employee level. Senior employees have more days of service and slightly more vacation days.
- **Good:** Highlights relationship between tenure and benefits.
- **Bad:** Dense plot makes it hard to see individual data points.

#### **10. Distribution of Employees by State (`state_distribution.png`)**
- **Analysis:** Bar chart showing state distribution: Fairly even across states like WA, NY, GA, etc. Reflects a geographically diverse workforce.
- **Good:** Identifies geographic spread of employees.
- **Bad:** Even distribution may not reflect real-world patterns.

#### **11. Distribution of Employees by Work Location (`work_location_distribution.png`)**
- **Analysis:** Pie chart showing work location: 34.5% Office, 32.8% Remote, 32.7% Hybrid. Indicates a balanced approach to work arrangements.
- **Good:** Reflects modern work trends.
- **Bad:** May oversimplify complex work arrangements.

#### **12. Distribution of Employees by Shift (`shift_distribution.png`)**
- **Analysis:** Pie chart showing shift distribution: 34.8% Day, 34.6% Night, 30.6% Flexible. Suggests flexibility in scheduling.
- **Good:** Highlights shift diversity.
- **Bad:** Even distribution may not reflect operational needs.

#### **13. Distribution of Employees by Status (`status_distribution.png`)**
- **Analysis:** Pie chart showing status: 76.5% Active, 13.5% Inactive, 10.0% Leave. Most employees are active, as expected.
- **Good:** Reflects employment status distribution.
- **Bad:** Limited insight into reasons for Inactive/Leave status.

#### **14. Performance Score Distribution by Gender (`gender_performance_distribution.png`)**
- **Analysis:** Box plot showing performance scores by gender. All genders have similar median scores (~75), with slight variations in spread.
- **Good:** Validates lack of gender bias in performance scores.
- **Bad:** Outliers may indicate inconsistencies in evaluation.

### Errors Detected
- **Unrealistic Values:**
  - Employees under 18: 18 rows (e.g., EMP000000000007, EMP000000000010).
  - Negative Salaries: None detected in this dataset.
  - Invalid Performance Scores: None detected (all within 0-100).
  - Negative Vacation/Sick Days: None detected.
  - Negative Days of Service: None detected.
- **Duplicate IDs:** None detected in this dataset.
- **Future Dates:** None detected for `birth_date`, `hire_date`, or `last_review_date`.
- **Inconsistent Days of Service:** None detected with the adjusted threshold (>30 days difference).



