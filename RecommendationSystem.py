import pandas as pd
#read in data sets
ratings = pd.read_csv('BX-Book-Ratings.csv', encoding='ISO-8859-1', delimiter=';', on_bad_lines='skip')
users = pd.read_csv('BX-Users.csv',encoding='ISO-8859-1', delimiter=';', on_bad_lines='skip')
books = pd.read_csv('BX_Books.csv', encoding='ISO-8859-1', delimiter=';', quotechar='"', skipinitialspace=True)

# #Remove images, year of publication, & publisher columns from Books dataset
copy_books = books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L', 'Year-Of-Publication','Publisher'], axis=1)
copy_books.to_csv('new_books.csv', index=False, sep=';', encoding='ISO-8859-1', quotechar='"')
# #books csv to df
pd.set_option('display.max_columns', None) #To print entire df
pd.set_option('display.expand_frame_repr', False) #To print entire df
books_df = pd.read_csv('new_books.csv', encoding='ISO-8859-1', delimiter=';', quotechar='"')

#Merge datasets
isbn_merge = pd.merge(ratings, books_df, on='ISBN')
fin_merge = pd.merge(isbn_merge, users, on='User-ID')

#replace na in Age column with median
fin_merge['Age'] = fin_merge['Age'].fillna(fin_merge['Age'].median())

#replace any rows missing a value in location with n/a
def clean_location(location):
    parts = location.split(',')
    if any(part.strip().lower() == 'n/a' for part in parts) or any(part.strip() == '' for part in parts):
        return 'unknown'
    return location
fin_merge['Location'] = fin_merge['Location'].apply(clean_location)

#Replace na in location with unknown
fin_merge['Location'] = fin_merge['Location'].replace('n/a','unknown')

#drop duplcate rows
fin_merge.drop_duplicates(inplace=True)
#create new csv file with cleaned data
fin_merge.to_csv('merged_data.csv', index=False, sep=';', encoding='ISO-8859-1', quotechar='"')
print(fin_merge.head(20))





