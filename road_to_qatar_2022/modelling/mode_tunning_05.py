from sklearn.model_selection import GridSearchCV
import xgboost as xgb
#Add data source for vinesh
import data as src_data
from encoder_02 import prepareTrainingset
from standardScaler_03 import standardScaler
# for other add the prefix folder road_t0....
#from road_to_qatar_2022.modelling.standardScaler_03 import standardScaler
#from road_to_qatar_2022.modelling.encoder_02 import prepareTrainingset


# Parameters list for tuning

def modelTuning():
    X_train_transformed,X_test_transformed,X_hold_test = standardScaler()
    X_hold_test, X_test, y_hold_test, y_test_encoded, X_train, X_val, y_train_encoded, y_val = prepareTrainingset()
    parameters = { 'learning_rate' : [0.001,0.01, 0.1, 1],
                'n_estimators' : [40, 100],
                'max_depth': [3, 6],
                'min_child_weight': [1, 3],
                'gamma':[0.4],
                'subsample' : [0.5, 0.8],
                'colsample_bytree' : [0.8],
                'scale_pos_weight' : [1],
                'reg_alpha':[1e-5]
                }
    clf = xgb.XGBClassifier(seed=2)

    grid_obj = GridSearchCV(clf,
                            param_grid=parameters,
                            cv=5)
    grid_obj = grid_obj.fit(X_train,y_train)
    clf = grid_obj.best_estimator_
    print(clf)
    return
