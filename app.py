import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from bot2 import create_rec_csv
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from graphs import (price_vs_sales, sales_by_product, production_capability_distribution,
                             rate_of_sale_distribution, correlation_heatmap, client_types_by_product)
def financial_analyst_recommendations(df):
    features = ['Current_Price', 'Sales_Volume', 'Production_Capability', 'Rate_of_Sale']
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['Group'] = kmeans.fit_predict(X_scaled)
    
    group_centroids = kmeans.cluster_centers_
    
    def generate_recommendation(row, group_centroid):
        recommendations = []
        
        # Price strategy
        price_diff = row['Current_Price'] - group_centroid[0]
        if price_diff > 10:
            price_reduction = min(price_diff * 0.7, row['Current_Price'] * 0.15)
            recommendations.append(f"Implement a strategic price reduction of ${price_reduction:.2f} to optimize market positioning.")
        elif 5 < price_diff <= 10:
            recommendations.append(f"Consider a moderate price adjustment of ${price_diff/2:.2f} to align with market trends.")
        elif -5 <= price_diff <= 5:
            recommendations.append("Current pricing is competitive. Monitor market dynamics for potential micro-adjustments.")
        elif price_diff < -5:
            potential_increase = min(abs(price_diff) * 0.5, row['Current_Price'] * 0.08)
            recommendations.append(f"Product is undervalued. Explore a gradual price increase of up to ${potential_increase:.2f}.")
        
        # Sales volume strategy
        sales_diff = row['Sales_Volume'] - group_centroid[1]
        if sales_diff < -100:
            discount = min(15, abs(sales_diff) / 20)
            recommendations.append(f"Initiate a limited-time {discount:.1f}% discount campaign to boost sales volume.")
        elif -100 <= sales_diff < -50:
            recommendations.append("Implement targeted marketing initiatives to stimulate demand.")
        elif -50 <= sales_diff < 0:
            recommendations.append("Sales are slightly below average. Enhance product visibility through strategic placement.")
        elif 0 <= sales_diff < 50:
            recommendations.append("Sales performance is solid. Focus on customer retention strategies.")
        elif 50 <= sales_diff < 100:
            recommendations.append("Strong sales momentum. Explore cross-selling opportunities with complementary products.")
        else:
            recommendations.append("Exceptional sales performance. Consider expanding product line or entering new markets.")
        
        # Production capability adjustment
        prod_diff = row['Production_Capability'] - group_centroid[2]
        if prod_diff < -1:
            increase = min(25, abs(prod_diff) * 15)
            recommendations.append(f"Critical: Increase production capacity by {increase:.1f}% to meet demand and prevent stockouts.")
        elif -1 <= prod_diff < -0.5:
            increase = min(15, abs(prod_diff) * 10)
            recommendations.append(f"Gradually increase production capacity by {increase:.1f}% to optimize inventory levels.")
        elif -0.5 <= prod_diff < 0:
            recommendations.append("Production capacity is slightly below optimal. Monitor closely and prepare for potential upgrades.")
        elif 0 <= prod_diff < 0.5:
            recommendations.append("Production capacity is well-balanced. Maintain current levels and focus on efficiency improvements.")
        elif 0.5 <= prod_diff < 1:
            recommendations.append("Production capacity exceeds current demand. Explore opportunities to utilize excess capacity.")
        else:
            reduction = min(20, prod_diff * 10)
            recommendations.append(f"Significant overcapacity detected. Consider reallocating {reduction:.1f}% of production resources.")
        
        # Rate of sale tactics
        ros_diff = row['Rate_of_Sale'] - group_centroid[3]
        if ros_diff < -1:
            recommendations.append("Critically low sales velocity. Implement aggressive promotional strategies and reassess product positioning.")
        elif -1 <= ros_diff < -0.5:
            recommendations.append("Below-average sales rate. Enhance product appeal through packaging upgrades or bundle offers.")
        elif -0.5 <= ros_diff < 0:
            recommendations.append("Sales rate is slightly below par. Optimize online presence and search engine visibility.")
        elif 0 <= ros_diff < 0.5:
            recommendations.append("Healthy sales rate. Focus on maintaining consistent inventory levels to meet steady demand.")
        elif 0.5 <= ros_diff < 1:
            recommendations.append("Above-average sales velocity. Implement dynamic pricing strategies to maximize revenue.")
        else:
            recommendations.append("Exceptionally high sales rate. Prioritize supply chain optimization to maintain momentum.")
        
        # Financial metrics
        gross_margin = (row['Current_Price'] - row['Competitor_Price']) / row['Current_Price'] * 100
        if gross_margin < 10:
            recommendations.append(f"Critical gross margin alert: {gross_margin:.1f}%. Immediate action required to reassess pricing and cost structure.")
        elif 10 <= gross_margin < 20:
            recommendations.append(f"Low gross margin of {gross_margin:.1f}%. Identify cost-saving opportunities and consider strategic price increases.")
        elif 20 <= gross_margin < 30:
            recommendations.append(f"Moderate gross margin of {gross_margin:.1f}%. Explore opportunities to enhance operational efficiency.")
        elif 30 <= gross_margin < 40:
            recommendations.append(f"Healthy gross margin of {gross_margin:.1f}%. Balance competitive pricing with profitability goals.")
        else:
            recommendations.append(f"Excellent gross margin of {gross_margin:.1f}%. Focus on maintaining competitive advantage and market share.")
        
        return " ".join(recommendations)

    df['Financial_Recommendations'] = df.apply(lambda row: generate_recommendation(row, group_centroids[row['Group']]), axis=1)
    
    return df[['SKU_ID', 'Product_Name', 'Current_Price', 'Sales_Volume', 'Production_Capability', 'Rate_of_Sale', 'Financial_Recommendations']]

def kmeans_recommendations(df):
    features = ['Current_Price', 'Sales_Volume', 'Production_Capability', 'Rate_of_Sale']
    X = df[features]
    
    # Feature Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # K-Means Clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Analyze Cluster Centroids to Generate Recommendations
    cluster_centroids = kmeans.cluster_centers_
    cluster_recommendations = {}
    
    for i, centroid in enumerate(cluster_centroids):
        recommendation = []
        
        # Price strategy
        if centroid[0] > np.mean(X['Current_Price']):
            recommendation.append(f"Cluster {i}: High-priced group. Consider premium positioning or gradual price reduction.")
        else:
            recommendation.append(f"Cluster {i}: Competitively priced group. Maintain pricing or explore slight increases.")

        # Sales volume strategy
        if centroid[1] > np.mean(X['Sales_Volume']):
            recommendation.append(f"High sales volume in Cluster {i}. Focus on inventory management and supply chain optimization.")
        else:
            recommendation.append(f"Lower sales volume in Cluster {i}. Implement targeted marketing and promotional campaigns.")

        # Production capability strategy
        if centroid[2] == 2:
            recommendation.append(f"Cluster {i} has high production capability. Explore new market opportunities or product variations.")
        elif centroid[2] == 0:
            recommendation.append(f"Cluster {i} has limited production capability. Consider outsourcing or increasing capacity.")
        else:
            recommendation.append(f"Cluster {i} has balanced production capability. Monitor demand fluctuations closely.")

        # Rate of sale strategy
        if centroid[3] == 2:
            recommendation.append(f"Fast-moving products in Cluster {i}. Implement dynamic pricing and ensure consistent stock levels.")
        elif centroid[3] == 0:
            recommendation.append(f"Slow-moving products in Cluster {i}. Consider product bundling or seasonal promotions.")
        else:
            recommendation.append(f"Average-moving products in Cluster {i}. Optimize product placement and explore cross-selling opportunities.")

        # Store the cluster strategy
        cluster_recommendations[i] = recommendation

    # Product-specific recommendations
    for index, row in df.iterrows():
        cluster_id = row['Cluster']
        general_recommendations = cluster_recommendations[cluster_id]
        personalized_recommendation = []

        # Determine proximity to the centroid
        product_position = X_scaled[index]
        distance_from_centroid = np.linalg.norm(product_position - cluster_centroids[cluster_id])

        # Cluster-specific recommendation
        personalized_recommendation.append(f"Product belongs to Cluster {cluster_id}. {general_recommendations[0]}")

        # Price recommendation
        if row['Current_Price'] > X['Current_Price'].mean():
            personalized_recommendation.append("Consider a competitive pricing strategy or highlight premium features.")
        else:
            personalized_recommendation.append("Maintain current pricing or explore gradual increases based on demand.")

        # Sales volume recommendation
        if row['Sales_Volume'] < X['Sales_Volume'].mean():
            personalized_recommendation.append("Boost sales through targeted marketing campaigns or promotional offers.")
        else:
            personalized_recommendation.append("Maintain strong sales performance. Focus on customer retention and upselling.")

        # Production capability recommendation
        if row['Production_Capability'] == 0:
            personalized_recommendation.append("Increase production capacity or explore partnerships to meet demand.")
        elif row['Production_Capability'] == 2:
            personalized_recommendation.append("High production capability. Ensure efficient inventory management.")

        # Rate of sale recommendation
        if row['Rate_of_Sale'] == 0:
            personalized_recommendation.append("Implement stock clearance strategies or consider product repositioning.")
        elif row['Rate_of_Sale'] == 2:
            personalized_recommendation.append("Fast-selling product. Ensure consistent stock levels and explore line extensions.")

        # Proximity-based recommendation
        if distance_from_centroid > 1:
            personalized_recommendation.append("This product shows unique characteristics within its cluster. Consider tailored strategies.")
        else:
            personalized_recommendation.append("Product aligns well with cluster average. Follow general cluster strategy.")

        # Combine all personalized recommendations into one string
        df.at[index, 'Recommendations'] = " ".join(personalized_recommendation)
    
    return df

def random_forest_recommendations(df):
    X = df.drop(['SKU_ID', 'Product_Name', 'Sales_Volume'], axis=1)
    y = df['Sales_Volume']
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    def generate_recommendation(row):
        top_feature = feature_importance.iloc[0]['feature']
        if row[top_feature] > df[top_feature].mean():
            return f"Focus on maintaining high {top_feature}"
        else:
            return f"Consider improving {top_feature}"
    
    df['Recommendations'] = df.apply(generate_recommendation, axis=1)
    return df

st.set_page_config(
    layout="wide", 
    page_title="Product Analysis Tool", 
    page_icon="📊"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
    }
    .stApp {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stDataFrame {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #343a40;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    h2, h3 {
        color: #343a40;
    }
    .header {
        background-color: #007BFF;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .footer {
        background-color: #007BFF;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        margin-top: 20px;
    }
    .footer a {
        color: white;
        text-decoration: none;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# Header section
st.markdown("<div class='header'><h1>Product Analysis Tool</h1></div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Original Data:")
    st.dataframe(df)

    recommendation_method = st.selectbox(
        "Choose recommendation method",
        ("Rule-based", "K-Means Clustering", "Random Forest", "Generative Pre Trained")
    )

    if st.button('Generate Recommendations'):
        with st.spinner('Generating recommendations...'):
            if recommendation_method == "Rule-based":
                recommendations_df = financial_analyst_recommendations(df)
                st.write("### Financial Recommendations:")
                st.dataframe(recommendations_df)
            elif recommendation_method == "K-Means Clustering":
                recommendations_df = kmeans_recommendations(df)
            elif recommendation_method == "Random Forest":
                recommendations_df = random_forest_recommendations(df)
            else:  # GPT
                recommendations_df = create_rec_csv(df)
        
        st.write("### Recommendations:")
        st.dataframe(recommendations_df)

        # Create a download button for the recommendations CSV
        csv = recommendations_df.to_csv(index=False)
        st.download_button(
            label="Download Recommendations as CSV",
            data=csv,
            file_name="recommendations.csv",
            mime="text/csv",
        )

    if st.button('Generate Graphs'):
        st.write("### Data Visualizations:")
    
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Price vs Sales Volume")
            st.image(price_vs_sales(df).getvalue(), use_column_width=True)
            
            st.subheader("Production Capability Distribution")
            st.image(production_capability_distribution(df).getvalue(), use_column_width=True)
            
            st.subheader("Correlation Heatmap")
            st.image(correlation_heatmap(df).getvalue(), use_column_width=True)
        
        with col2:
            st.subheader("Sales by Product")
            st.image(sales_by_product(df).getvalue(), use_column_width=True)
            
            st.subheader("Rate of Sale Distribution")
            st.image(rate_of_sale_distribution(df).getvalue(), use_column_width=True)
            
            st.subheader("Client Types by Product")
            st.image(client_types_by_product(df).getvalue(), use_column_width=True)

else:
    st.write("Please upload a CSV file to begin analysis.")

# Footer section
st.markdown("""
    <div class='footer'>
        <p>Developed by UltraAnalysers 🚀🚀</p>
    </div>
    """, unsafe_allow_html=True)