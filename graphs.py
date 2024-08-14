# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Data (up to SKU013 as provided in the correct format)

# # Read the data into a pandas DataFrame
# df = pd.read_csv("D:\walmart_sparkathon\data_mul_encode\processed_data_test.csv")

# # Set a consistent style for all plots
# #plt.style.use('seaborn')

# # 1. Scatter plot: Current Price vs Sales Volume
# plt.figure(figsize=(12, 8))
# sns.scatterplot(x='Current_Price', y='Sales_Volume', data=df, size='Production_Capability', 
#                 hue='Rate_of_Sale', palette='viridis', sizes=(50, 200))
# plt.title('Current Price vs Sales Volume')
# plt.xlabel('Current Price')
# plt.ylabel('Sales Volume')
# plt.savefig('price_vs_sales.png')
# plt.close()

# # 2. Bar plot: Sales Volume by Product
# plt.figure(figsize=(14, 8))
# sns.barplot(x='Product_Name', y='Sales_Volume', data=df, palette='coolwarm')
# plt.title('Sales Volume by Product')
# plt.xlabel('Product')
# plt.ylabel('Sales Volume')
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.savefig('sales_by_product.png')
# plt.close()

# # 3. Pie chart: Production Capability Distribution
# production_counts = df['Production_Capability'].value_counts()
# plt.figure(figsize=(10, 10))
# plt.pie(production_counts.values, labels=production_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
# plt.title('Production Capability Distribution')
# plt.axis('equal')
# plt.savefig('production_capability_distribution.png')
# plt.close()

# # 4. Histogram: Rate of Sale Distribution
# plt.figure(figsize=(10, 6))
# sns.histplot(df['Rate_of_Sale'], bins=5, kde=True, color='skyblue')
# plt.title('Rate of Sale Distribution')
# plt.xlabel('Rate of Sale')
# plt.ylabel('Frequency')
# plt.savefig('rate_of_sale_distribution.png')
# plt.close()

# # 5. Heatmap: Correlation between numeric variables
# numeric_cols = ['Current_Price', 'Competitor_Price', 'Sales_Volume', 'Production_Capability', 'Payment_Terms', 'Rate_of_Sale']
# correlation = df[numeric_cols].corr()
# plt.figure(figsize=(12, 10))
# sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
# plt.title('Correlation Heatmap')
# plt.tight_layout()
# plt.savefig('correlation_heatmap.png')
# plt.close()

# # 6. Grouped bar plot: Client Types by Product
# client_types = df[['Product_Name', 'Client_Type_Bulk', 'Client_Type_Regular', 'Client_Type_New']]
# client_types_melted = pd.melt(client_types, id_vars=['Product_Name'], var_name='Client_Type', value_name='Value')
# plt.figure(figsize=(14, 8))
# sns.barplot(x='Product_Name', y='Value', hue='Client_Type', data=client_types_melted, palette='Set2')
# plt.title('Client Types by Product')
# plt.xlabel('Product')
# plt.ylabel('Client Type (0 or 1)')
# plt.xticks(rotation=45, ha='right')
# plt.legend(title='Client Type')
# plt.tight_layout()
# plt.savefig('client_types_by_product.png')
# plt.close()

# print("All graphs have been generated and saved as PNG files.")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def price_vs_sales(df):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Current_Price', y='Sales_Volume', data=df, size='Production_Capability', 
                    hue='Rate_of_Sale', palette='viridis', sizes=(50, 200))
    plt.title('Current Price vs Sales Volume')
    plt.xlabel('Current Price')
    plt.ylabel('Sales Volume')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf

def sales_by_product(df):
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Product_Name', y='Sales_Volume', data=df, palette='coolwarm')
    plt.title('Sales Volume by Product')
    plt.xlabel('Product')
    plt.ylabel('Sales Volume')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf

def production_capability_distribution(df):
    production_counts = df['Production_Capability'].value_counts()
    plt.figure(figsize=(10, 10))
    plt.pie(production_counts.values, labels=production_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
    plt.title('Production Capability Distribution')
    plt.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf

def rate_of_sale_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Rate_of_Sale'], bins=5, kde=True, color='skyblue')
    plt.title('Rate of Sale Distribution')
    plt.xlabel('Rate of Sale')
    plt.ylabel('Frequency')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf

def correlation_heatmap(df):
    numeric_cols = ['Current_Price', 'Competitor_Price', 'Sales_Volume', 'Production_Capability', 'Payment_Terms', 'Rate_of_Sale']
    correlation = df[numeric_cols].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf

def client_types_by_product(df):
    client_types = df[['Product_Name', 'Client_Type_Bulk', 'Client_Type_Regular', 'Client_Type_New']]
    client_types_melted = pd.melt(client_types, id_vars=['Product_Name'], var_name='Client_Type', value_name='Value')
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Product_Name', y='Value', hue='Client_Type', data=client_types_melted, palette='Set2')
    plt.title('Client Types by Product')
    plt.xlabel('Product')
    plt.ylabel('Client Type (0 or 1)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Client Type')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf