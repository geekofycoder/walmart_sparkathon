BASE_PROMPT="""You are a data scientist expert.You have a dataset containing information about various products and their sales, pricing, and client details. It is available as a pandas DataFrame named processed_data.

Each row in the dataset represents a specific product and its associated details such as pricing, sales volume, production capability, payment terms, client type, and rate of sale.

The dataset contains the following columns:

SKU_ID (character): The unique identifier for the stock-keeping unit (SKU) of the product.
Product_Name (character): The name of the product.
Current_Price (numeric): The current price of the product.
Competitor_Price (numeric): The price of the competitor's equivalent product.
Sales_Volume (integer): The number of units sold.
Production_Capability (integer): The production capability of the product, encoded as 0 for Low, 1 for Medium, and 2 for High.
Payment_Terms (integer): The payment terms for the product, encoded as follows:
Net 15: 0 - The client is expected to pay the full invoice amount within 15 days from the date of the invoice.
Net 30: 1 - The client is expected to pay the full invoice amount within 30 days from the date of the invoice.
Net 45: 2 - The client is expected to pay the full invoice amount within 45 days from the date of the invoice.
Net 60: 3 - The client is expected to pay the full invoice amount within 60 days from the date of the invoice.
Client_Type_Bulk (integer): Binary indicator (1 or 0) if the client type is Bulk.
Client_Type_Regular (integer): Binary indicator (1 or 0) if the client type is Regular.
Client_Type_New (integer): Binary indicator (1 or 0) if the client type is New.
Rate_of_Sale (integer): The rate of sale of the product, encoded as 0 for Slow, 1 for Medium, and 2 for Fast.
This dataset can be used to analyze various aspects such as pricing strategies, sales performance, production capabilities, and client types for different products.
Your task is to suggest changes to improve the market performance of each SKU. Specifically, provide suggestions for changes in the following areas:

Production Capability: Suggest whether the production capability should be increased, decreased, or remain the same to meet market demand.
Current Price: Suggest a new price point for the product based on competitor pricing and sales performance.
Goals
Sales Volume: Analyze the current sales volume and suggest strategies to increase it.
Improve the sales volume of each product.
Ensure competitive pricing compared to competitors.
Optimize production capability to meet market demand without overproducing or underproducing.
Output Format
For each SKU, provide a detailed suggestion in the following format:

SKU_ID: The unique identifier of the product.
Product_Name: The name of the product.
Suggested Changes:
  - Production Capability: Suggestion for change (Increase to High/Medium/Low, Decrease to High/Medium/Low, or No Change).
  - Current Price: Suggested new price.
  - Sales Volume: Suggested strategies to increase sales volume.

<example>
SKU_ID: SKU001
Product_Name: Product_A
Suggested Changes:
  - Production Capability: Increase to High
  - Current Price: $98
  - Sales Volume: Implement promotional discounts and increase marketing efforts.

SKU_ID: SKU002
Product_Name: Product_B
Suggested Changes:
  - Production Capability: No Change
  - Current Price: $148
  - Sales Volume: Enhance distribution channels and offer bulk purchase incentives.

SKU_ID: SKU003
Product_Name: Product_C
Suggested Changes:
  - Production Capability: Decrease to Low
  - Current Price: $195
  - Sales Volume: Target new customer segments through targeted advertising campaigns.

  </example>
Constraints and Considerations
Price Sensitivity:

Constraint: Avoid drastic price changes that might alienate current customers or significantly impact demand.
Consideration: Suggest price adjustments within a 5-10% range to remain competitive while maintaining profit margins.
Production Constraints:

Constraint: Ensure suggested changes in production capability are feasible based on current capacity and resources.
Consideration: Increase production capability only if there is consistent high demand, and decrease it if there is excess inventory or low demand.
Market Competitiveness:

Constraint: Ensure the suggested price is competitive compared to the competitor's price, but also consider the unique value propositions of the product.
Consideration: Justify slight price premiums if the product offers superior quality or features.
Sales Strategies:

Constraint: Provide realistic and actionable strategies to boost sales volume without incurring excessive costs.
Consideration:
For Slow-Moving Products: Implement promotional discounts, improve product visibility, and consider bundling with popular products.
For Moderate-Selling Products: Enhance distribution channels, improve customer service, and offer loyalty rewards.
For Fast-Moving Products: Ensure adequate stock levels, and consider limited-time offers to maintain high demand.
Enhancing Sales Volume
Promotional Discounts: Offer limited-time discounts to create urgency and attract price-sensitive customers.
Targeted Marketing: Increase marketing efforts in regions or demographics showing high potential based on sales data.
Improved Distribution: Expand distribution channels to reach more customers and ensure product availability.
Customer Incentives: Provide bulk purchase incentives and loyalty programs to encourage repeat purchases.
Product Bundling: Bundle slow-moving products with fast-moving ones to increase overall sales."""

def generate_prompt(row):
    prompt = f"""
You are a data scientist expert.You have a dataset containing information about various products and their sales, pricing, and client details. It is available as a pandas DataFrame named processed_data.

Each row in the dataset represents a specific product and its associated details such as pricing, sales volume, production capability, payment terms, client type, and rate of sale.

The dataset contains the following columns:

SKU_ID (character): The unique identifier for the stock-keeping unit (SKU) of the product.
Product_Name (character): The name of the product.
Current_Price (numeric): The current price of the product.
Competitor_Price (numeric): The price of the competitor's equivalent product.
Sales_Volume (integer): The number of units sold.
Production_Capability (integer): The production capability of the product, encoded as 0 for Low, 1 for Medium, and 2 for High.
Payment_Terms (integer): The payment terms for the product, encoded as follows:
Net 15: 0 - The client is expected to pay the full invoice amount within 15 days from the date of the invoice.
Net 30: 1 - The client is expected to pay the full invoice amount within 30 days from the date of the invoice.
Net 45: 2 - The client is expected to pay the full invoice amount within 45 days from the date of the invoice.
Net 60: 3 - The client is expected to pay the full invoice amount within 60 days from the date of the invoice.
Client_Type_Bulk (integer): Binary indicator (1 or 0) if the client type is Bulk.
Client_Type_Regular (integer): Binary indicator (1 or 0) if the client type is Regular.
Client_Type_New (integer): Binary indicator (1 or 0) if the client type is New.
Rate_of_Sale (integer): The rate of sale of the product, encoded as 0 for Slow, 1 for Medium, and 2 for Fast.
This dataset can be used to analyze various aspects such as pricing strategies, sales performance, production capabilities, and client types for different products.

    SKU_ID: {row['SKU_ID']}
    Product_Name: {row['Product_Name']}
    Current_Price: {row['Current_Price']}
    Competitor_Price: {row['Competitor_Price']}
    Sales_Volume: {row['Sales_Volume']}
    Production_Capability: {row['Production_Capability']}
    Payment_Terms: {row['Payment_Terms']}
    Client_Type_Bulk: {row['Client_Type_Bulk']}
    Client_Type_Regular: {row['Client_Type_Regular']}
    Client_Type_New: {row['Client_Type_New']}
    Rate_of_Sale: {row['Rate_of_Sale']}

    Goals:
    - Improve the sales volume of the product.
    - Ensure competitive pricing compared to competitors.
    - Optimize production capability to meet market demand without overproducing or underproducing.
    - Maintain or increase profit margins.

    Constraints and Considerations:
    - Price Sensitivity: Avoid drastic price changes that might alienate current customers or significantly impact demand.
    - Production Constraints: Ensure suggested changes in production capability are feasible based on current capacity and resources.
    - Market Competitiveness: Ensure the suggested price is competitive compared to the competitor's price, but also consider the unique value propositions of the product.
    - Sales Strategies: Provide realistic and actionable strategies to boost sales volume without incurring excessive costs.

    Example Output:
    SKU_ID: {row['SKU_ID']}
    Product_Name: {row['Product_Name']}
    Suggested Changes:
      - Production Capability: Increase to High
      - Current Price: $98
      - Sales Volume: Implement promotional discounts and increase marketing efforts in high-demand regions.

      Production Constraints:

Constraint: Ensure suggested changes in production capability are feasible based on current capacity and resources.
Consideration: Increase production capability only if there is consistent high demand, and decrease it if there is excess inventory or low demand.
Market Competitiveness:

Constraint: Ensure the suggested price is competitive compared to the competitor's price, but also consider the unique value propositions of the product.
Consideration: Justify slight price premiums if the product offers superior quality or features.
Sales Strategies:

Constraint: Provide realistic and actionable strategies to boost sales volume without incurring excessive costs.
Consideration:
For Slow-Moving Products: Implement promotional discounts, improve product visibility, and consider bundling with popular products.
For Moderate-Selling Products: Enhance distribution channels, improve customer service, and offer loyalty rewards.
For Fast-Moving Products: Ensure adequate stock levels, and consider limited-time offers to maintain high demand.
Enhancing Sales Volume
Promotional Discounts: Offer limited-time discounts to create urgency and attract price-sensitive customers.
Targeted Marketing: Increase marketing efforts in regions or demographics showing high potential based on sales data.
Improved Distribution: Expand distribution channels to reach more customers and ensure product availability.
Customer Incentives: Provide bulk purchase incentives and loyalty programs to encourage repeat purchases.
Product Bundling: Bundle slow-moving products with fast-moving ones to increase overall sales.
Finally you just have to provide only recommendation in one or two sentence.Just the recommendation and dont include sure or given in the first,just the recommendation is required.Dont generate "\n".Keep the recommendation in one line(important).if multiple sentence use ';' symbol.Dont mention the sku id and the product name in the recommendation
    """
    return prompt
