import pandas as pd 

#Load the dataset
df = pd.read_csv('All_Diets.csv')

#Handle missing data (fill missing values with mean)
df.fillna(df.mean(numeric_only=True), inplace=True)
#prevents non-numeric columns from being affected, ignores text columns

#Calculate the average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)','Carbs(g)', 'Fat(g)']].mean()
print("\n=== Average Macronutrient Content by Diet Type ===")
print(avg_macros)

#Find the top 5 protein-rich recipes for each diet type
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print("\n=== Top 5 Protein-Rich Recipes per Diet Type ===")
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']])

#Find diet type with highest protein content
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
print(f"\nDiet type with highest average protein content: {highest_protein_diet}")

#Most common cuisine for each diet type
most_common_cuisine = df.groupby('Diet_type')['Cuisine_type'].agg(lambda x: x.value_counts().index[0])
print("\n=== Most Common Cuisine per Diet Type ===")
print(most_common_cuisine)

#Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

print("\n=== Added New Columns===")
print(df[['Recipe_name', 'Protein_to_Carbs_ratio', 'Carbs_to_Fat_ratio']].head())


import seaborn as sns
import matplotlib.pyplot as plt

#Bar chart for average macronutrients per diet type - Protein
plt.figure(figsize=(10,6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.xlabel('Diet Type')
plt.ylabel('Average Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Bar chart for average macronutrients per diet type - Carbs
plt.figure(figsize=(10,6))
sns.barplot(x=avg_macros.index, y=avg_macros['Carbs(g)'])
plt.title('Average Carbs by Diet Type')
plt.xlabel('Diet Type')
plt.ylabel('Average Carbs (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Bar chart for average macronutrients per diet type - Fat
plt.figure(figsize=(10,6))
sns.barplot(x=avg_macros.index, y=avg_macros['Fat(g)'])
plt.title('Average Fat by Diet Type')  
plt.xlabel('Diet Type')
plt.ylabel('Average Fat (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(avg_macros, annot=True, cmap="YlGnBu")
plt.title('Heatmap: Macronutrient Distribution by Diet Type')
plt.xlabel('Macronutrient Type')
plt.ylabel('Diet Type')
plt.tight_layout()
plt.show()

#Top 5 Protein-Rich Recipes
plt.figure(figsize=(10,6))
sns.scatterplot(data=top_protein, x='Carbs(g)', y='Protein(g)', hue='Cuisine_type', style='Diet_type', s=100,)
plt.title('Top 5 Protein-Rich Recipes by Cuisine')
plt.xlabel('Carbs (g)')
plt.ylabel('Protein (g)')
plt.legend(title='Cuisine_type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
