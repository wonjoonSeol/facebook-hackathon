import datetime
import numpy as np
import pandas as pd
import random

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def split_data(ids, docs, target_values, perc_train, shuffle_data):
    """Split the document and classification data into training and testing sets."""

    # get a list of all valid indexes relating to the docs array
    ndx_shuffle = list(range(len(docs)))
    # Shuffle list of indexes
    if shuffle_data:
        random.shuffle(ndx_shuffle)

    # determine which index should be used to split the list of indexes into
    # training / test sets
    num_train = int(len(docs) * perc_train)

    # get 'ranges' (actually sublists) for training / test sets
    trainingRange = ndx_shuffle[:num_train]
    testRange = ndx_shuffle[num_train:]

    # get n=num_train docs (by randomised index) 
    docs_train = [str(docs[i]).lower() for i in trainingRange]
    docs_test = [str(docs[i]).lower() for i in testRange]

    target_values_train = [target_values[i] for i in trainingRange]
    target_values_test = [target_values[i] for i in testRange]

    ids_train = [ids[i] for i in trainingRange]
    ids_test = [ids[i] for i in testRange]

    return ids_train, ids_test, docs_train, docs_test, target_values_train, target_values_test


def split_word(word):
    word = word.replace(' ', '')
    return ' '.join(list(word))

def train_classifier(
        docs,
        targets,
        perc_train=0.81,
        shuffle_data=True,
        ngram_range=(1, 1),
        filter_params={},
        limit_data=None,
        cross_val_folds=10,
        min_df=0.0,
        max_df=1.0):
    
    ids = range(len(docs))

    ids_train, ids_test, docs_train, docs_test, y_train, y_test = split_data(ids, docs, targets, perc_train, shuffle_data)

    vect = CountVectorizer(min_df=min_df, max_df=max_df, ngram_range=ngram_range, stop_words='english')

    X_train = vect.fit_transform(docs_train)
    X_test = vect.transform(docs_test)

    lr_classifier = LogisticRegression(solver='newton-cg', penalty='l2', multi_class='multinomial').fit(X_train, y_train)

    if cross_val_folds > 0:
        
        cv_precision = cross_val_score(lr_classifier, X_train, y_train, cv=cross_val_folds, scoring='precision')
        cv_recall = cross_val_score(lr_classifier, X_train, y_train, cv=cross_val_folds, scoring='recall')
        
        print("\t%d-fold cross validation scores:\n\t\tPrecision:%.4f\n\t\tRecall:%.4f" 
            % (cross_val_folds, cv_precision.mean(), cv_recall.mean()))

    def get_top_feats(feature_names, classifier, plot=True, N=10, bar_height=0.5):

        sorted_feats = np.argsort(classifier.coef_[0])  # Sorted by coefficients (descending)
        sorted_coeffs = classifier.coef_[0][sorted_feats]

        return sorted_feats, sorted_coeffs

    features = np.array(vect.get_feature_names())
    feat_ids, coeffs = get_top_feats(features, lr_classifier, plot=False, N=20)

    if len(docs_test) > 0:
        print('\t'
            + 'Test set: %s'
            % len(docs_test))

        X_test = vect.transform(docs_test)
        # Predict test data
        y_test_predicted = lr_classifier.predict(X_test)

        print('\t' 
            + predictive_attribute 
            + ' classifier has precision %.3f and recall %.3f over the test set' 
            % (metrics.precision_score(y_test, y_test_predicted), metrics.recall_score(y_test, y_test_predicted)))

    stats_obj = {}

    def get_top_feats(feature_names, classifier, plot=True, N=10, bar_height=0.5):
        """Sort keywords by their coefficients"""
        sorted_feats = np.argsort(classifier.coef_[0])  # Sorted by coefficients (descending)
        sorted_coeffs = classifier.coef_[0][sorted_feats]

        return sorted_feats, sorted_coeffs

    features = np.array(vect.get_feature_names())
    feat_ids, coeffs = get_top_feats(features, lr_classifier, plot=False, N=20)

    stats_obj['model'] = lr_classifier
    stats_obj['vect'] = vect
    
    return {'stats': stats_obj, 'features': list(zip(features[feat_ids], coeffs))}

if __name__ == '__main__':

    import pandas
    df = pandas.read_csv('QueryResults.csv')
    df.dropna(subset=['Tags'])
    print(df.shape[0])
    docs = list(df['Body'])
    targets = list(map(lambda t: t.lstrip('<').rstrip('>').split('><'), df['Tags']))

    summary_dict = train_classifier(
        docs, targets,
        perc_train=0.81,
        ngram_range=(2,3),
        min_df=1,
        max_df=1.0,
        cross_val_folds=10)
