from sklearn.preprocessing import RobustScaler
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sc = RobustScaler()
model = LogisticRegression(random_state=0, solver='liblinear')

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer['data'], cancer['target'], stratify=cancer['target'], random_state=0)

model.fit(X_train, y_train)

print("標準化前")
print('正解率(train):{:.3f}'.format(model.score(X_train, y_train)))
print('正解率(test):{:.3f}'.format(model.score(X_test, y_test)))

sc.fit(X_train)
X_train_minmax = sc.transform(X_train)
X_test_minmax = sc.transform(X_test)
model.fit(X_train_minmax, y_train)

print("標準化後")
print('正解率(train):{:.3f}'.format(model.score(X_train_minmax, y_train)))
print('正解率(test):{:.3f}'.format(model.score(X_test_minmax, y_test)))
