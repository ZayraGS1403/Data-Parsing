import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def ensure_plot_directory(directory="plotsBig"):
    """
    Ensure that the directory for saving plotsBig exists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def load_and_clean_data(file_path):
    """
    Load and clean employee data from CSV, with improved error detection.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned employee data.
    """
    try:
        # Read CSV
        data = pd.read_csv(file_path, low_memory=False)

        # Validate required columns
        required_columns = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'department',
            'job_title', 'hire_date', 'days_service', 'base_salary', 'bonus_percentage',
            'status', 'birth_date', 'address', 'city', 'state', 'zip_code', 'country',
            'gender', 'education', 'performance_score', 'last_review_date', 'employee_level',
            'vacation_days', 'sick_days', 'work_location', 'shift', 'emergency_contact',
            'ssn', 'bank_account'
        ]
        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Clean data
        data = data.copy()

        # Error Detection (before any conversions)
        # 1. Duplicate employee IDs
        duplicate_ids = data[data['employee_id'].duplicated(keep=False)]
        if not duplicate_ids.empty:
            logging.warning(
                f"Found {len(duplicate_ids)} duplicate employee IDs:\n{duplicate_ids[['employee_id']].head()}")

        # 2. Invalid employee_id format (should be EMP followed by 9 digits)
        invalid_ids = data[~data['employee_id'].apply(lambda x: bool(re.match(r'EMP\d{9}', str(x))))]
        if not invalid_ids.empty:
            logging.warning(f"Found {len(invalid_ids)} invalid employee IDs:\n{invalid_ids[['employee_id']].head()}")

        # 3. Future birth dates, hire dates, and last review dates
        current_date = pd.Timestamp('2025-05-01')

        # Convert dates for error detection (but keep raw values)
        data['birth_date_raw'] = data['birth_date']
        data['hire_date_raw'] = data['hire_date']
        data['birth_date'] = pd.to_datetime(data['birth_date'], errors='coerce')
        data['hire_date'] = pd.to_datetime(data['hire_date'], errors='coerce')
        data['last_review_date'] = pd.to_datetime(data['last_review_date'], errors='coerce')

        future_birth_dates = data[data['birth_date'].notna() & (data['birth_date'] > current_date)]
        if not future_birth_dates.empty:
            logging.warning(
                f"Found {len(future_birth_dates)} future birth dates:\n{future_birth_dates[['employee_id', 'birth_date']].head()}")

        future_hire_dates = data[data['hire_date'].notna() & (data['hire_date'] > current_date)]
        if not future_hire_dates.empty:
            logging.warning(
                f"Found {len(future_hire_dates)} future hire dates:\n{future_hire_dates[['employee_id', 'hire_date']].head()}")

        future_review_dates = data[data['last_review_date'].notna() & (data['last_review_date'] > current_date)]
        if not future_review_dates.empty:
            logging.warning(
                f"Found {len(future_review_dates)} future last review dates:\n{future_review_dates[['employee_id', 'last_review_date']].head()}")

        # 4. Negative salaries and other numerical errors
        data['base_salary_raw'] = data['base_salary']
        data['performance_score_raw'] = data['performance_score']
        data['vacation_days_raw'] = data['vacation_days']
        data['sick_days_raw'] = data['sick_days']
        data['days_service_raw'] = data['days_service']

        # Convert numerical columns after error detection
        data['base_salary'] = pd.to_numeric(data['base_salary'], errors='coerce')
        data['performance_score'] = pd.to_numeric(data['performance_score'], errors='coerce')
        data['vacation_days'] = pd.to_numeric(data['vacation_days'], errors='coerce')
        data['sick_days'] = pd.to_numeric(data['sick_days'], errors='coerce')
        data['days_service'] = pd.to_numeric(data['days_service'], errors='coerce')
        data['bonus_percentage'] = pd.to_numeric(data['bonus_percentage'], errors='coerce')

        # Detect negative salaries
        negative_salaries = data[data['base_salary'].notna() & (data['base_salary'] < 0)]
        if not negative_salaries.empty:
            logging.warning(
                f"Found {len(negative_salaries)} negative salaries:\n{negative_salaries[['employee_id', 'base_salary']].head()}")

        # Detect invalid performance scores
        invalid_performance = data[
            (data['performance_score'].notna()) &
            ((data['performance_score'] < 0) | (data['performance_score'] > 100))
            ]
        if not invalid_performance.empty:
            logging.warning(
                f"Found {len(invalid_performance)} invalid performance scores:\n{invalid_performance[['employee_id', 'performance_score']].head()}")

        # Detect negative vacation and sick days
        negative_vacation_days = data[data['vacation_days'].notna() & (data['vacation_days'] < 0)]
        if not negative_vacation_days.empty:
            logging.warning(
                f"Found {len(negative_vacation_days)} negative vacation days:\n{negative_vacation_days[['employee_id', 'vacation_days']].head()}")

        negative_sick_days = data[data['sick_days'].notna() & (data['sick_days'] < 0)]
        if not negative_sick_days.empty:
            logging.warning(
                f"Found {len(negative_sick_days)} negative sick days:\n{negative_sick_days[['employee_id', 'sick_days']].head()}")

        # Detect negative days_service
        negative_days_service = data[data['days_service'].notna() & (data['days_service'] < 0)]
        if not negative_days_service.empty:
            logging.warning(
                f"Found {len(negative_days_service)} negative days_service:\n{negative_days_service[['employee_id', 'days_service']].head()}")

        # Calculate age (handle future dates)
        data['age'] = np.nan
        valid_birth_dates = data['birth_date'].notna() & (data['birth_date'] <= current_date)
        data.loc[valid_birth_dates, 'age'] = (current_date - data.loc[valid_birth_dates, 'birth_date']).dt.days / 365.25
        data['age'] = data['age'].round().astype('Int64')

        # 5. Employees under 18 (only for valid ages)
        under_18 = data[data['age'].notna() & (data['age'] < 18)]
        if not under_18.empty:
            logging.warning(
                f"Found {len(under_18)} employees under 18:\n{under_18[['employee_id', 'age', 'birth_date']].head()}")

        # Clean categorical columns
        for col in ['department', 'job_title', 'status', 'gender', 'education', 'employee_level', 'work_location',
                    'shift']:
            data[col] = data[col].str.strip().replace('', np.nan) if data[col].dtype == 'object' else data[col]

        # 6. Inconsistent days_service vs hire_date
        data['calculated_days_service'] = np.nan
        valid_hire_dates = data['hire_date'].notna() & (data['hire_date'] <= current_date)
        data.loc[valid_hire_dates, 'calculated_days_service'] = (
                    current_date - data.loc[valid_hire_dates, 'hire_date']).dt.days
        # Adjust threshold to detect more significant inconsistencies
        inconsistent_days = data[
            data['calculated_days_service'].notna() &
            data['days_service'].notna() &
            (abs(data['days_service'] - data['calculated_days_service']) > 30)  # Aumentar umbral a 30 días
            ]
        if not inconsistent_days.empty:
            logging.warning(
                f"Found {len(inconsistent_days)} inconsistent days_service vs hire_date:\n{inconsistent_days[['employee_id', 'days_service', 'calculated_days_service']].head()}")

        # Log missing values
        logging.info(f"Missing values:\n{data.isna().sum()}")

        # Remove rows with critical missing data
        critical_cols = ['base_salary', 'hire_date']
        data = data.dropna(subset=critical_cols)

        # Filter out invalid data before visualizations
        # Remove rows with negative salaries
        data = data[data['base_salary'].notna() & (data['base_salary'] >= 0)]
        # Remove rows with invalid performance scores
        data = data[
            data['performance_score'].notna() & (data['performance_score'] >= 0) & (data['performance_score'] <= 100)]
        # Remove rows with employees under 18
        data = data[data['age'].notna() & (data['age'] >= 18)]
        # Remove rows with future birth dates
        data = data[data['birth_date'].notna() & (data['birth_date'] <= current_date)]

        # Detect outliers in base_salary
        Q1 = data['base_salary'].quantile(0.25)
        Q3 = data['base_salary'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data['base_salary'] < Q1 - 1.5 * IQR) | (data['base_salary'] > Q3 + 1.5 * IQR)]
        if not outliers.empty:
            logging.warning(f"Found {len(outliers)} salary outliers after cleaning")

        logging.info(f"Data shape after cleaning: {data.shape}")
        return data

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


# Funciones de visualización existentes
def plot_salary_vs_age(data, output_dir="plotsBig"):
    if data.empty:
        logging.warning("Cannot plot salary vs age: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='age', y='base_salary', hue='gender', data=data, alpha=0.6)
    plt.title("Salary vs. Age by Gender", fontsize=16)
    plt.xlabel("Age", fontsize=12)
    plt.ylabel("Base Salary ($)", fontsize=12)
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(output_dir, "salary_vs_age.png"))
    plt.close()


def plot_days_service_vs_vacation(data, output_dir="plotsBig"):
    if data.empty:
        logging.warning("Cannot plot days_service vs vacation_days: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='days_service', y='vacation_days', hue='employee_level', data=data, alpha=0.6)
    plt.title("Days of Service vs. Vacation Days by Employee Level", fontsize=16)
    plt.xlabel("Days of Service", fontsize=12)
    plt.ylabel("Vacation Days", fontsize=12)
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(output_dir, "days_service_vs_vacation.png"))
    plt.close()


def plot_salary_distribution(data, output_dir="plotsBig"):
    if data.empty:
        logging.warning("Cannot plot salary distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.histplot(data['base_salary'].dropna(), kde=True, color='blue', bins=50)
    plt.title("Salary Distribution", fontsize=16)
    plt.xlabel("Base Salary ($)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True)

    salary_data = data['base_salary'].dropna()
    if len(salary_data) >= 50:
        sample_size = min(5000, len(salary_data))
        stat, p_value = stats.shapiro(salary_data.sample(sample_size))
        plt.annotate(f"Shapiro-Wilk p-value: {p_value:.4f}", xy=(0.05, 0.95), xycoords='axes fraction')
    else:
        logging.warning("Dataset too small for reliable Shapiro-Wilk test")

    plt.savefig(os.path.join(output_dir, "salary_distribution.png"))
    plt.close()


def plot_gender_salary_distribution(data, output_dir="plotsBig"):
    if data.empty:
        logging.warning("Cannot plot gender salary distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='gender', y='base_salary', data=data)
    plt.title("Salary Distribution by Gender", fontsize=16)
    plt.xlabel("Gender", fontsize=12)
    plt.ylabel("Base Salary ($)", fontsize=12)
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, "gender_salary_distribution.png"))
    plt.close()


def plot_gender_performance_distribution(data, output_dir="plotsBig"):
    if data.empty:
        logging.warning("Cannot plot gender performance distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='gender', y='performance_score', data=data)
    plt.title("Performance Score Distribution by Gender", fontsize=16)
    plt.xlabel("Gender", fontsize=12)
    plt.ylabel("Performance Score", fontsize=12)
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, "gender_performance_distribution.png"))
    plt.close()


def plot_performance_distribution(data, output_dir="plotsBig"):
    if data.empty:
        logging.warning("Cannot plot performance distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.histplot(data['performance_score'].dropna(), kde=True, color='green', bins=50)
    plt.title("Performance Score Distribution", fontsize=16)
    plt.xlabel("Performance Score", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True)

    performance_data = data['performance_score'].dropna()
    if len(performance_data) >= 50:
        sample_size = min(5000, len(performance_data))
        stat, p_value = stats.shapiro(performance_data.sample(sample_size))
        plt.annotate(f"Shapiro-Wilk p-value: {p_value:.4f}", xy=(0.05, 0.95), xycoords='axes fraction')
    else:
        logging.warning("Dataset too small for reliable Shapiro-Wilk test")

    plt.savefig(os.path.join(output_dir, "performance_distribution.png"))
    plt.close()


# Nuevas funciones de visualización
def plot_department_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by department using a bar chart.
    """
    if data.empty:
        logging.warning("Cannot plot department distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(12, 6))
    sns.countplot(x='department', data=data, order=data['department'].value_counts().index)
    plt.title("Distribution of Employees by Department", fontsize=16)
    plt.xlabel("Department", fontsize=12)
    plt.ylabel("Number of Employees", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "department_distribution.png"))
    plt.close()


def plot_gender_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by gender using a pie chart.
    """
    if data.empty:
        logging.warning("Cannot plot gender distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(8, 8))
    gender_counts = data['gender'].value_counts()
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Employees by Gender", fontsize=16)
    plt.savefig(os.path.join(output_dir, "gender_distribution.png"))
    plt.close()


def plot_education_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by education level using a bar chart.
    """
    if data.empty:
        logging.warning("Cannot plot education distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(10, 6))
    sns.countplot(x='education', data=data, order=data['education'].value_counts().index)
    plt.title("Distribution of Employees by Education Level", fontsize=16)
    plt.xlabel("Education Level", fontsize=12)
    plt.ylabel("Number of Employees", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "education_distribution.png"))
    plt.close()


def plot_city_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by city (top 10 cities) using a bar chart.
    """
    if data.empty:
        logging.warning("Cannot plot city distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(12, 6))
    top_cities = data['city'].value_counts().nlargest(10)
    sns.barplot(x=top_cities.index, y=top_cities.values)
    plt.title("Distribution of Employees by City (Top 10)", fontsize=16)
    plt.xlabel("City", fontsize=12)
    plt.ylabel("Number of Employees", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "city_distribution.png"))
    plt.close()


def plot_state_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by state using a bar chart.
    """
    if data.empty:
        logging.warning("Cannot plot state distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(12, 6))
    sns.countplot(x='state', data=data, order=data['state'].value_counts().index)
    plt.title("Distribution of Employees by State", fontsize=16)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Number of Employees", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "state_distribution.png"))
    plt.close()


def plot_employee_level_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by employee level using a pie chart.
    """
    if data.empty:
        logging.warning("Cannot plot employee level distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(8, 8))
    level_counts = data['employee_level'].value_counts()
    plt.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Employees by Employee Level", fontsize=16)
    plt.savefig(os.path.join(output_dir, "employee_level_distribution.png"))
    plt.close()


def plot_work_location_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by work location using a pie chart.
    """
    if data.empty:
        logging.warning("Cannot plot work location distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(8, 8))
    location_counts = data['work_location'].value_counts()
    plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Employees by Work Location", fontsize=16)
    plt.savefig(os.path.join(output_dir, "work_location_distribution.png"))
    plt.close()


def plot_shift_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by shift using a pie chart.
    """
    if data.empty:
        logging.warning("Cannot plot shift distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(8, 8))
    shift_counts = data['shift'].value_counts()
    plt.pie(shift_counts, labels=shift_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Employees by Shift", fontsize=16)
    plt.savefig(os.path.join(output_dir, "shift_distribution.png"))
    plt.close()


def plot_status_distribution(data, output_dir="plotsBig"):
    """
    Plot the distribution of employees by status using a pie chart.
    """
    if data.empty:
        logging.warning("Cannot plot status distribution: DataFrame is empty")
        return

    ensure_plot_directory(output_dir)
    plt.figure(figsize=(8, 8))
    status_counts = data['status'].value_counts()
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Employees by Status", fontsize=16)
    plt.savefig(os.path.join(output_dir, "status_distribution.png"))
    plt.close()


def analyze_data(data):
    if data.empty:
        logging.warning("Cannot analyze data: DataFrame is empty")
        return {}

    analysis = {}
    analysis['salary_stats'] = data['base_salary'].describe()
    analysis['performance_stats'] = data['performance_score'].describe()
    analysis['vacation_days_stats'] = data['vacation_days'].describe()

    analysis['normality'] = {
        'base_salary': {'p_value': np.nan, 'is_normal': False},
        'performance_score': {'p_value': np.nan, 'is_normal': False},
        'vacation_days': {'p_value': np.nan, 'is_normal': False}
    }
    salary_data = data['base_salary'].dropna()
    performance_data = data['performance_score'].dropna()
    vacation_data = data['vacation_days'].dropna()
    if len(salary_data) >= 50:
        sample_size = min(5000, len(salary_data))
        stat, p_salary = stats.shapiro(salary_data.sample(sample_size))
        analysis['normality']['base_salary'] = {'p_value': p_salary, 'is_normal': p_salary > 0.05}
    if len(performance_data) >= 50:
        sample_size = min(5000, len(performance_data))
        stat, p_performance = stats.shapiro(performance_data.sample(sample_size))
        analysis['normality']['performance_score'] = {'p_value': p_performance, 'is_normal': p_performance > 0.05}
    if len(vacation_data) >= 50:
        sample_size = min(5000, len(vacation_data))
        stat, p_vacation = stats.shapiro(vacation_data.sample(sample_size))
        analysis['normality']['vacation_days'] = {'p_value': p_vacation, 'is_normal': p_vacation > 0.05}

    return analysis


def main():
    try:
        file_path = "data13_big.csv"
        logging.info("Loading data...")
        data = load_and_clean_data(file_path)

        if data.empty:
            logging.error("No data available after cleaning. Check CSV file and data integrity.")
            return

        logging.info("Analyzing data...")
        analysis_results = analyze_data(data)

        logging.info("Generating visualizations...")
        # Existing visualizations
        plot_salary_vs_age(data)
        plot_days_service_vs_vacation(data)
        plot_salary_distribution(data)
        plot_gender_salary_distribution(data)
        plot_gender_performance_distribution(data)
        plot_performance_distribution(data)
        # New visualizations
        plot_department_distribution(data)
        plot_gender_distribution(data)
        plot_education_distribution(data)
        plot_city_distribution(data)
        plot_state_distribution(data)
        plot_employee_level_distribution(data)
        plot_work_location_distribution(data)
        plot_shift_distribution(data)
        plot_status_distribution(data)
        logging.info("All visualizations have been saved in the 'plotsBig' directory.")

    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise
if __name__ == "__main__":
    main()