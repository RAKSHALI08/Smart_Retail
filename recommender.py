import pandas as pd
import ast
# Load data
customer_data = pd.read_csv("customer_data_collection.csv")
product_data = pd.read_csv("product_recommendation_data.csv")

# Parse list-like columns
customer_data['Browsing_History'] = customer_data['Browsing_History'].apply(ast.literal_eval)
customer_data['Purchase_History'] = customer_data['Purchase_History'].apply(ast.literal_eval)
product_data['Similar_Product_List'] = product_data['Similar_Product_List'].apply(ast.literal_eval)

# Recommend function
def recommend_products(customer_id, top_n=5):
    if customer_id not in customer_data['Customer_ID'].values:
        print(f"\nCustomer ID '{customer_id}' not found in data.\n")
        return pd.DataFrame()

    customer = customer_data[customer_data['Customer_ID'] == customer_id].iloc[0]
    interests = set(customer['Browsing_History'] + customer['Purchase_History'])

    def match_interest(row):
        return any(
            interest in row['Similar_Product_List'] or
            interest == row['Subcategory'] or
            interest == row['Category']
            for interest in interests
        )

    recommendations = product_data[product_data.apply(match_interest, axis=1)]
    recommendations = recommendations.sort_values(by='Probability_of_Recommendation', ascending=False)

    return recommendations[['Product_ID', 'Category', 'Subcategory', 'Brand', 'Price', 'Probability_of_Recommendation']].head(top_n)

# Get input from the user
user_input = input("Enter Customer ID (e.g., C1000): ").strip()
recommended_results = recommend_products(user_input)

if not recommended_results.empty:
    print(f"\nTop recommendations for Customer {user_input}:\n")
    print(recommended_results)
