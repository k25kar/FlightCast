import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

df=pd.read_csv('flight-delay-predictor/flights.csv')

# Encode categorical variables
le_origin=LabelEncoder()
le_dest=LabelEncoder()
le_weather=LabelEncoder()
le_airline=LabelEncoder()
le_day=LabelEncoder()

df['Origin']=le_origin.fit_transform(df['Origin'])
df['Dest']=le_dest.fit_transform(df['Dest'])
df['Weather']=le_weather.fit_transform(df['Weather'])
df['Airline']=le_airline.fit_transform(df['Airline'])
df['Day']=le_day.fit_transform(df['Day'])
df['Delayed']=df['Delayed'].map({'No':0,'Yes':1})

X=df[['Origin','Dest','DepTime','Weather','Airline','Duration','Day']]
y=df['Delayed']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

# Hyperparameter tuning
param_grid={
    'n_estimators':[100,200],
    'max_depth':[None,10,20],
    'min_samples_split':[2,5],
    'min_samples_leaf':[1,2],
}

grid_search=GridSearchCV(RandomForestClassifier(random_state=42),param_grid,cv=3,n_jobs=-1,verbose=1)
grid_search.fit(X_train,y_train)

best_model=grid_search.best_estimator_

# Evaluate
y_pred=best_model.predict(X_test)
acc=accuracy_score(y_test,y_pred)

print(f"\nAccuracy: {acc:.4f}\n")
print("Classification Report:")
print(classification_report(y_test,y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test,y_pred))

# Save best model + encoders
pickle.dump(best_model,open('flight_model.pkl','wb'))
pickle.dump((le_origin,le_dest,le_weather,le_airline,le_day),open('encoders.pkl','wb'))

print("\nBest model and encoders saved!")
