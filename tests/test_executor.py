import ast

import numpy as np

import qastle

from func_adl_uproot import ast_executor


def test_ast_executor_select_scalar_branch():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [0, -1]


def test_ast_executor_select_scalar_branch_list():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_branch, row.long_branch])')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast)['0'].tolist() == [0, -1]
    assert ast_executor(python_ast)['1'].tolist() == [0, -2]


def test_ast_executor_select_scalar_branch_tuple():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: (row.int_branch, row.long_branch))')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast)['0'].tolist() == [0, -1]
    assert ast_executor(python_ast)['1'].tolist() == [0, -2]


def test_ast_executor_select_scalar_branch_dict():
    python_source = ("Select(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + " lambda row: {'int_branch': row.int_branch,"
                     + " 'long_branch': row.long_branch})")
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast)['int_branch'].tolist() == [0, -1]
    assert ast_executor(python_ast)['long_branch'].tolist() == [0, -2]


def test_ast_executor_where_scalar_branch():
    python_source = ("Where(EventDataset('tests/scalars_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_branch < 0)'
                     + '.Select(lambda row: row.long_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [-2]


def test_ast_executor_select_vector_branch():
    python_source = ("Select(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [[], [-1, 2, 3], [13]]


def test_ast_executor_selectmany_vector_branch():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: row.int_vector_branch)')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast).tolist() == [-1, 2, 3, 13]


def test_ast_executor_selectmany_vector_branch_list():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: [row.int_vector_branch, row.float_vector_branch])')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast)['0'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['1'], [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_selectmany_vector_branch_tuple():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + ' lambda row: (row.int_vector_branch, row.float_vector_branch))')
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast)['0'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['1'], [-7.7, 8.8, 9.9, 15.15])


def test_ast_executor_selectmany_vector_branch_dict():
    python_source = ("SelectMany(EventDataset('tests/vectors_tree_file.root', 'tree'),"
                     + " lambda row: {'int_vector_branch': row.int_vector_branch,"
                     + " 'float_vector_branch': row.float_vector_branch})")
    python_ast = qastle.insert_linq_nodes(ast.parse(python_source))
    assert ast_executor(python_ast)['int_vector_branch'].tolist() == [-1, 2, 3, 13]
    assert np.allclose(ast_executor(python_ast)['float_vector_branch'], [-7.7, 8.8, 9.9, 15.15])
