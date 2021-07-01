"""Location Encoder"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

__author__ = 'patohdzs'


class LocationEncoder(BaseEstimator, TransformerMixin):
    """Hierarchical target encoding for location features in Shakes and Quakes project.

    Supported targets:  polynomial.

    For the case of categorical target: features are replaced with a blend of posterior probability of the target
    given particular categorical value and the prior probability of the target over all the training data.
    

    Parameters
    ----------

    verbose: int
        integer indicating verbosity of the output. 0 for none.
    cols: list
        a list of columns to encode, if None, all string columns will be encoded.
    drop_invariant: bool
        boolean for whether or not to drop columns with 0 variance.
    return_df: bool
        boolean for whether to return a pandas DataFrame from transform (otherwise it will be a numpy array).
    handle_missing: str
        options are 'error', 'return_nan'  and 'value', defaults to 'value', which returns the target mean.
    handle_unknown: str
        options are 'error', 'return_nan' and 'value', defaults to 'value', which returns the target mean.
    min_samples_leaf: int
        minimum samples to take category average into account.
    smoothing: float
        smoothing effect to balance categorical average vs prior. Higher value means stronger regularization.
        The value must be strictly bigger than 0.


    References
    ----------

    .. [1] A Preprocessing Scheme for High-Cardinality Categorical Attributes in Classification and Prediction Problems, from
    https://dl.acm.org/citation.cfm?id=507538

    """

    def __init__(self, min_samples_leaf=1, smoothing=1.0, categories='auto', 
                 handle_unknown='error', unknown_value=None, cols, hierarchies):
        self.cols = cols
        self.hierarchies = hierarchies
        self.min_samples_leaf = min_samples_leaf
        self.smoothing = float(smoothing)  # Make smoothing a float so that python 2 does not treat as integer division
        self._dim = None
        self.mapping = None
        self._means = None

    def fit(self, X, y):
        """Fit encoder according to X and y.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.

        Returns
        -------
        self : encoder
            Returns self.

        """

        # unite the input into pandas types
        X = pd.DataFrame(X)
        y = pd.DataFrame(y, X.index)

        if X.shape[0] != y.shape[0]:
            raise ValueError("The length of X is " + str(X.shape[0]) + " but length of y is " + str(y.shape[0]) + ".")

        self._dim = X.shape[1]

        # if columns aren't passed, just use every string column
        if self.cols is None:
            self.cols = util.get_obj_cols(X)
        else:
            self.cols = util.convert_cols_to_list(self.cols)

        if X[self.cols].isnull().any().any():
            raise ValueError('Columns to be encoded can not contain null')
            
        self.mapping = self.fit_target_encoding(X, y)
        
        X_temp = self.transform(X, override_return_df=True)
        return self

    
    def fit_target_encoding(self, X, y, col):
        # This function creates map between current categories and new encoded vals
        # For each 1,..., K categories, determines what replacement val is
        # We want that, but 3, maybe recursive????
        # Input col
        #
        
        mapping = {}
        # Indices are target values: prior[1] is proportion of obsvs. with target==1
        prior = self._means = y.value_counts(normalize=True)
        for p in prior:
            ## TODO, insTEAD OF mean, get proportion for that p (maybe even get rid of for loop)
            stats = y.groupby(X[col]).agg(['count', 'mean'])
            
            if col = 1:
                smoove = 1 / (1 + np.exp(-(stats['count'] - self.min_samples_leaf) / self.smoothing))
                smoothing = prior * (1 - smoove) + stats['mean'] * smoove
                smoothing[stats['count'] == 1] = prior
                mapping[col] = smoothing #Change!!!!!
            else:
                smoove = 1 / (1 + np.exp(-(stats['count'] - self.min_samples_leaf) / self.smoothing))
                smoothing = prior * (1 - smoove) + stats['mean'] * smoove
                smoothing[stats['count'] == 1] = prior
            
        #--------------------------------------------------------------------------------------------------------

        for switch in self.ordinal_encoder.category_mapping:
            col = switch.get('col')
            values = switch.get('mapping')
            
            # Indices are target values: prior[1] is proportion of obsvs. with target==1
            prior = self._means = y.value_counts(normalize=True)
            
            stats = y.groupby(X[col]).agg(['count', 'mean'])

            smoove = 1 / (1 + np.exp(-(stats['count'] - self.min_samples_leaf) / self.smoothing))
            smoothing = prior * (1 - smoove) + stats['mean'] * smoove
            smoothing[stats['count'] == 1] = prior
            
            mapping[col] = smoothing

        return mapping
    
    
    
    
    

    
    

