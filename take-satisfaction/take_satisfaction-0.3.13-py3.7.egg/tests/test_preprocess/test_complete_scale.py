__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import pandas as pd

from take_satisfaction.preprocess import complete_scale


def test_fill_scale_completed():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    mock_actions = ('Nao Ajudou', 'Ajudou')
    mock_missing_quantity = 0
    mock_answer_column = 'Action'
    mock_quantities_column = 'qtd'
    
    expected_result = mock_df
    
    result = complete_scale(mock_df, mock_answer_column, mock_quantities_column, mock_actions, mock_missing_quantity)
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_fill_scale_missing():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            ])
    mock_actions = ('Nao Ajudou', 'Ajudou')
    mock_missing_quantity = 0
    mock_answer_column = 'Action'
    mock_quantities_column = 'qtd'
    
    expected_result = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                                    {'Action': 'Ajudou', 'qtd': 0}
                                    ])
    
    result = complete_scale(mock_df, mock_answer_column, mock_quantities_column, mock_actions, mock_missing_quantity)
 
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result)


def test_fill_scale_no_actions():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    mock_actions = ''
    mock_missing_quantity = 0
    mock_answer_column = 'Action'
    mock_quantities_column = 'qtd'
    
    expected_result = mock_df
    
    result = complete_scale(mock_df, mock_answer_column, mock_quantities_column, mock_actions, mock_missing_quantity)
    
    pd.testing.assert_frame_equal(result, expected_result)
