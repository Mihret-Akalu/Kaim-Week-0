import pandas as pd

# Load datasets
datasets = {
    "Benin": "data/benin-malanville.csv",
    "Sierra Leone": "data/sierraleone-bumbuna.csv",
    "Togo": "data/togo-dapaong_qc.csv"
}

for name, path in datasets.items():
    print(f"\n--- {name} Dataset ---")
    try:
        # Load the dataset
        data = pd.read_csv(path)
        
        # Display basic info
        print("Dataset Overview:")
        print(data.info())
        print("\nSummary Statistics:")
        print(data.describe())

        # Check for missing values
        print("\nMissing Values:")
        print(data.isnull().sum())
    except Exception as e:
        print(f"Error loading {name} dataset: {e}")
# Summary statistics
print(f"\n--- Summary Statistics for {name} ---")
print(data.describe())
# Check for missing values
print(f"\n--- Missing Values for {name} ---")
print(data.isnull().sum())
# Check for negative values
columns_to_check = ['GHI', 'DNI', 'DHI']
for col in columns_to_check:
    if col in data.columns:
        print(f"{col}: {sum(data[col] < 0)} negative values")
# Correlation matrix
if data.select_dtypes(include='number').shape[1] > 1:
    corr_matrix = data.corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.title(f"Correlation Heatmap for {name}")
    plt.show()
# Plot histograms for numeric columns
data.hist(bins=20, figsize=(12, 8))
plt.suptitle(f"Histograms for {name}")
plt.show()
if 'Timestamp' in data.columns:
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data.set_index('Timestamp', inplace=True)

    # Plot GHI over time
    if 'GHI' in data.columns:
        data['GHI'].plot(title=f"GHI Over Time in {name}")
        plt.xlabel('Time')
        plt.ylabel('GHI')
        plt.show()
if {'GHI', 'Temperature'}.issubset(data.columns):
    sns.scatterplot(x=data['Temperature'], y=data['GHI'])
    plt.title(f"GHI vs Temperature in {name}")
    plt.show()
from windrose import WindroseAxes

if {'WS', 'WD'}.issubset(data.columns):
    ax = WindroseAxes.from_ax()
    ax.bar(data['WD'], data['WS'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    plt.title(f"Wind Rose for {name}")
    plt.show()

data['GHI'].fillna(data['GHI'].mean(), inplace=True)
data.drop('Comments', axis=1, inplace=True)
from scipy.stats import zscore
z_scores = zscore(data['GHI'])
data_cleaned = data[(z_scores > -3) & (z_scores < 3)]
data_cleaned.to_csv(f"data/{name}_cleaned.csv", index=False)
