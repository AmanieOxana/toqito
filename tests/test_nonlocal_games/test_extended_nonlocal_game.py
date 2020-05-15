"""Tests for ExtendedNonlocalGame class."""
import unittest
import numpy as np

from toqito.states import basis
from toqito.nonlocal_games.extended_nonlocal_game import ExtendedNonlocalGame


class TestExtendedNonlocalGame(unittest.TestCase):
    """Unit test for ExtendedNonlocalGame."""

    def test_bb84_unentangled_value(self):
        """Calculate the unentangled value of the BB84 game."""
        e_0, e_1 = basis(2, 0), basis(2, 1)
        e_p = (e_0 + e_1) / np.sqrt(2)
        e_m = (e_0 - e_1) / np.sqrt(2)

        dim_x = dim_y = 2
        num_alice_out, num_bob_out = 2, 2
        num_alice_in, num_bob_in = 2, 2

        pred_mat = np.zeros(
            [dim_x, dim_y, num_alice_out, num_bob_out, num_alice_in, num_bob_in]
        )
        pred_mat[:, :, 0, 0, 0, 0] = e_0 * e_0.conj().T
        pred_mat[:, :, 0, 0, 1, 1] = e_p * e_p.conj().T
        pred_mat[:, :, 1, 1, 0, 0] = e_1 * e_1.conj().T
        pred_mat[:, :, 1, 1, 1, 1] = e_m * e_m.conj().T

        prob_mat = 1 / 2 * np.identity(2)

        bb84 = ExtendedNonlocalGame(prob_mat, pred_mat)
        res = bb84.unentangled_value()
        expected_res = np.cos(np.pi / 8) ** 2

        self.assertEqual(np.isclose(res, expected_res), True)

    def test_chsh_unentangled_value(self):
        """Calculate the unentangled value of the CHSH game."""
        dim_x = dim_y = 2
        num_alice_out, num_bob_out = 2, 2
        num_alice_in, num_bob_in = 2, 2

        pred_mat = np.zeros(
            [dim_x, dim_y, num_alice_out, num_bob_out, num_alice_in, num_bob_in]
        )
        pred_mat[:, :, 0, 0, 0, 0] = np.array([[1, 0], [0, 0]])
        pred_mat[:, :, 0, 0, 0, 1] = np.array([[1, 0], [0, 0]])
        pred_mat[:, :, 0, 0, 1, 0] = np.array([[1, 0], [0, 0]])

        pred_mat[:, :, 1, 1, 0, 0] = np.array([[0, 0], [0, 1]])
        pred_mat[:, :, 1, 1, 0, 1] = np.array([[0, 0], [0, 1]])
        pred_mat[:, :, 1, 1, 1, 0] = np.array([[0, 0], [0, 1]])

        pred_mat[:, :, 0, 1, 1, 1] = 1 / 2 * np.array([[1, 1], [1, 1]])
        pred_mat[:, :, 1, 0, 1, 1] = 1 / 2 * np.array([[1, -1], [-1, 1]])

        prob_mat = np.array([[1 / 4, 1 / 4], [1 / 4, 1 / 4]])

        chsh = ExtendedNonlocalGame(prob_mat, pred_mat)
        res = chsh.unentangled_value()
        expected_res = 3 / 4

        self.assertEqual(np.isclose(res, expected_res), True)

    def test_moe_mub_in_4_out_3_unentangled_value(self):
        """
        Calculate the unentanlged value of a monogamy-of-entanglement game.
        """
        prob_mat = 1 / 4 * np.identity(4)

        dim = 3
        e_0, e_1, e_2 = basis(dim, 0), basis(dim, 1), basis(dim, 2)

        eta = np.exp((2 * np.pi * 1j) / dim)
        mub_0 = [e_0, e_1, e_2]
        mub_1 = [
            (e_0 + e_1 + e_2) / np.sqrt(3),
            (e_0 + eta ** 2 * e_1 + eta * e_2) / np.sqrt(3),
            (e_0 + eta * e_1 + eta ** 2 * e_2) / np.sqrt(3),
        ]
        mub_2 = [
            (e_0 + e_1 + eta * e_2) / np.sqrt(3),
            (e_0 + eta ** 2 * e_1 + eta ** 2 * e_2) / np.sqrt(3),
            (e_0 + eta * e_1 + e_2) / np.sqrt(3),
        ]
        mub_3 = [
            (e_0 + e_1 + eta ** 2 * e_2) / np.sqrt(3),
            (e_0 + eta ** 2 * e_1 + e_2) / np.sqrt(3),
            (e_0 + eta * e_1 + eta * e_2) / np.sqrt(3),
        ]

        # List of measurements defined from mutually unbiased basis.
        mubs = [mub_0, mub_1, mub_2, mub_3]

        num_in = 4
        num_out = 3
        pred_mat = np.zeros([dim, dim, num_out, num_out, num_in, num_in], dtype=complex)

        pred_mat[:, :, 0, 0, 0, 0] = mubs[0][0] * mubs[0][0].conj().T
        pred_mat[:, :, 1, 1, 0, 0] = mubs[0][1] * mubs[0][1].conj().T
        pred_mat[:, :, 2, 2, 0, 0] = mubs[0][2] * mubs[0][2].conj().T

        pred_mat[:, :, 0, 0, 1, 1] = mubs[1][0] * mubs[1][0].conj().T
        pred_mat[:, :, 1, 1, 1, 1] = mubs[1][1] * mubs[1][1].conj().T
        pred_mat[:, :, 2, 2, 1, 1] = mubs[1][2] * mubs[1][2].conj().T

        pred_mat[:, :, 0, 0, 2, 2] = mubs[2][0] * mubs[2][0].conj().T
        pred_mat[:, :, 1, 1, 2, 2] = mubs[2][1] * mubs[2][1].conj().T
        pred_mat[:, :, 2, 2, 2, 2] = mubs[2][2] * mubs[2][2].conj().T

        pred_mat[:, :, 0, 0, 3, 3] = mubs[3][0] * mubs[3][0].conj().T
        pred_mat[:, :, 1, 1, 3, 3] = mubs[3][1] * mubs[3][1].conj().T
        pred_mat[:, :, 2, 2, 3, 3] = mubs[3][2] * mubs[3][2].conj().T

        mub = ExtendedNonlocalGame(prob_mat, pred_mat)
        res = mub.unentangled_value()
        expected_res = (3 + np.sqrt(5)) / 8

        self.assertEqual(np.isclose(res, expected_res), True)
