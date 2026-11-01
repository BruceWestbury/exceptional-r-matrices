# Ordinary A(3) relation inventory

[manifest.json](manifest.json) contains 150 checks. Each check specifies an
identifier, ordered generator words, exact coefficients and the representations
to which it applies. The inventory includes defining relations and their local
or polynomial consequences, with repeated identities serving distinct checks.

| Category | Checks |
|---|---:|
| H,K,U defining equality | 30 |
| Braid prescription or inverse | 8 |
| Local multiplication table | 68 |
| Local identity or consequence | 26 |
| Polynomial prescription | 4 |
| Braid or quintic relation | 3 |
| Quintic consequence | 2 |
| Top-quotient identity | 9 |

All eleven ordinary representations are tested. The nine top-quotient checks
apply to X3, Y3, Y3_star, A, C and C_star. This gives 1,605 applicable checks.

## Identifiers

| Identifier | Role | Applies to |
|---|---|---|
| `HK1` | H,K,U defining equality | All eleven |
| `KH1` | H,K,U defining equality | All eleven |
| `HU1` | H,K,U defining equality | All eleven |
| `UH1` | H,K,U defining equality | All eleven |
| `KK1` | H,K,U defining equality | All eleven |
| `KU1` | H,K,U defining equality | All eleven |
| `UK1` | H,K,U defining equality | All eleven |
| `UU1` | H,K,U defining equality | All eleven |
| `cubic1` | H,K,U defining equality | All eleven |
| `inverse_left1` | Braid prescription or inverse | All eleven |
| `inverse_right1` | Braid prescription or inverse | All eleven |
| `S_polynomial1` | Braid prescription or inverse | All eleven |
| `Sinv_polynomial1` | Braid prescription or inverse | All eleven |
| `HK2` | H,K,U defining equality | All eleven |
| `KH2` | H,K,U defining equality | All eleven |
| `HU2` | H,K,U defining equality | All eleven |
| `UH2` | H,K,U defining equality | All eleven |
| `KK2` | H,K,U defining equality | All eleven |
| `KU2` | H,K,U defining equality | All eleven |
| `UK2` | H,K,U defining equality | All eleven |
| `UU2` | H,K,U defining equality | All eleven |
| `cubic2` | H,K,U defining equality | All eleven |
| `inverse_left2` | Braid prescription or inverse | All eleven |
| `inverse_right2` | Braid prescription or inverse | All eleven |
| `S_polynomial2` | Braid prescription or inverse | All eleven |
| `Sinv_polynomial2` | Braid prescription or inverse | All eleven |
| `local1_literal_U_U` | Local multiplication table | All eleven |
| `local1_literal_U_K` | Local multiplication table | All eleven |
| `local1_literal_U_H` | Local multiplication table | All eleven |
| `local1_literal_K_U` | Local multiplication table | All eleven |
| `local1_literal_K_K` | Local multiplication table | All eleven |
| `local1_literal_K_H` | Local multiplication table | All eleven |
| `local1_literal_H_U` | Local multiplication table | All eleven |
| `local1_literal_H_K` | Local multiplication table | All eleven |
| `local1_literal_H_H` | Local multiplication table | All eleven |
| `local1_completed_one_one` | Local multiplication table | All eleven |
| `local1_completed_one_H` | Local multiplication table | All eleven |
| `local1_completed_one_H2` | Local multiplication table | All eleven |
| `local1_completed_one_K` | Local multiplication table | All eleven |
| `local1_completed_one_U` | Local multiplication table | All eleven |
| `local1_completed_H_one` | Local multiplication table | All eleven |
| `local1_completed_H_H` | Local multiplication table | All eleven |
| `local1_completed_H_H2` | Local multiplication table | All eleven |
| `local1_completed_H_K` | Local multiplication table | All eleven |
| `local1_completed_H_U` | Local multiplication table | All eleven |
| `local1_completed_H2_one` | Local multiplication table | All eleven |
| `local1_completed_H2_H` | Local multiplication table | All eleven |
| `local1_completed_H2_H2` | Local multiplication table | All eleven |
| `local1_completed_H2_K` | Local multiplication table | All eleven |
| `local1_completed_H2_U` | Local multiplication table | All eleven |
| `local1_completed_K_one` | Local multiplication table | All eleven |
| `local1_completed_K_H` | Local multiplication table | All eleven |
| `local1_completed_K_H2` | Local multiplication table | All eleven |
| `local1_completed_K_K` | Local multiplication table | All eleven |
| `local1_completed_K_U` | Local multiplication table | All eleven |
| `local1_completed_U_one` | Local multiplication table | All eleven |
| `local1_completed_U_H` | Local multiplication table | All eleven |
| `local1_completed_U_H2` | Local multiplication table | All eleven |
| `local1_completed_U_K` | Local multiplication table | All eleven |
| `local1_completed_U_U` | Local multiplication table | All eleven |
| `local1_square_square` | Local identity or consequence | All eleven |
| `local1_cubic` | Local identity or consequence | All eleven |
| `local1_reduce_H3` | Local identity or consequence | All eleven |
| `local1_reduce_H4` | Local identity or consequence | All eleven |
| `local1_skein` | Local identity or consequence | All eleven |
| `local1_inverse_right` | Local identity or consequence | All eleven |
| `local1_inverse_left` | Local identity or consequence | All eleven |
| `local1_S_polynomial` | Local identity or consequence | All eleven |
| `local1_Sinv_polynomial` | Local identity or consequence | All eleven |
| `local1_jacobi_commute_S` | Local identity or consequence | All eleven |
| `local1_jacobi_commute_Sinv` | Local identity or consequence | All eleven |
| `local1_jacobi_S` | Local identity or consequence | All eleven |
| `local1_jacobi_Sinv` | Local identity or consequence | All eleven |
| `local1_K_from_H` | Polynomial prescription | All eleven |
| `local1_U_from_H` | Polynomial prescription | All eleven |
| `local2_literal_U_U` | Local multiplication table | All eleven |
| `local2_literal_U_K` | Local multiplication table | All eleven |
| `local2_literal_U_H` | Local multiplication table | All eleven |
| `local2_literal_K_U` | Local multiplication table | All eleven |
| `local2_literal_K_K` | Local multiplication table | All eleven |
| `local2_literal_K_H` | Local multiplication table | All eleven |
| `local2_literal_H_U` | Local multiplication table | All eleven |
| `local2_literal_H_K` | Local multiplication table | All eleven |
| `local2_literal_H_H` | Local multiplication table | All eleven |
| `local2_completed_one_one` | Local multiplication table | All eleven |
| `local2_completed_one_H` | Local multiplication table | All eleven |
| `local2_completed_one_H2` | Local multiplication table | All eleven |
| `local2_completed_one_K` | Local multiplication table | All eleven |
| `local2_completed_one_U` | Local multiplication table | All eleven |
| `local2_completed_H_one` | Local multiplication table | All eleven |
| `local2_completed_H_H` | Local multiplication table | All eleven |
| `local2_completed_H_H2` | Local multiplication table | All eleven |
| `local2_completed_H_K` | Local multiplication table | All eleven |
| `local2_completed_H_U` | Local multiplication table | All eleven |
| `local2_completed_H2_one` | Local multiplication table | All eleven |
| `local2_completed_H2_H` | Local multiplication table | All eleven |
| `local2_completed_H2_H2` | Local multiplication table | All eleven |
| `local2_completed_H2_K` | Local multiplication table | All eleven |
| `local2_completed_H2_U` | Local multiplication table | All eleven |
| `local2_completed_K_one` | Local multiplication table | All eleven |
| `local2_completed_K_H` | Local multiplication table | All eleven |
| `local2_completed_K_H2` | Local multiplication table | All eleven |
| `local2_completed_K_K` | Local multiplication table | All eleven |
| `local2_completed_K_U` | Local multiplication table | All eleven |
| `local2_completed_U_one` | Local multiplication table | All eleven |
| `local2_completed_U_H` | Local multiplication table | All eleven |
| `local2_completed_U_H2` | Local multiplication table | All eleven |
| `local2_completed_U_K` | Local multiplication table | All eleven |
| `local2_completed_U_U` | Local multiplication table | All eleven |
| `local2_square_square` | Local identity or consequence | All eleven |
| `local2_cubic` | Local identity or consequence | All eleven |
| `local2_reduce_H3` | Local identity or consequence | All eleven |
| `local2_reduce_H4` | Local identity or consequence | All eleven |
| `local2_skein` | Local identity or consequence | All eleven |
| `local2_inverse_right` | Local identity or consequence | All eleven |
| `local2_inverse_left` | Local identity or consequence | All eleven |
| `local2_S_polynomial` | Local identity or consequence | All eleven |
| `local2_Sinv_polynomial` | Local identity or consequence | All eleven |
| `local2_jacobi_commute_S` | Local identity or consequence | All eleven |
| `local2_jacobi_commute_Sinv` | Local identity or consequence | All eleven |
| `local2_jacobi_S` | Local identity or consequence | All eleven |
| `local2_jacobi_Sinv` | Local identity or consequence | All eleven |
| `local2_K_from_H` | Polynomial prescription | All eleven |
| `local2_U_from_H` | Polynomial prescription | All eleven |
| `braid` | Braid or quintic relation | All eleven |
| `HKH` | H,K,U defining equality | All eleven |
| `KUK1` | H,K,U defining equality | All eleven |
| `KUH1` | H,K,U defining equality | All eleven |
| `KUU1` | H,K,U defining equality | All eleven |
| `UUK1` | H,K,U defining equality | All eleven |
| `UUU1` | H,K,U defining equality | All eleven |
| `KUK2` | H,K,U defining equality | All eleven |
| `KUH2` | H,K,U defining equality | All eleven |
| `KUU2` | H,K,U defining equality | All eleven |
| `UUK2` | H,K,U defining equality | All eleven |
| `UUU2` | H,K,U defining equality | All eleven |
| `quartic_full` | H,K,U defining equality | All eleven |
| `S_quintic1` | Braid or quintic relation | All eleven |
| `H_quintic1` | Quintic consequence | All eleven |
| `S_quintic2` | Braid or quintic relation | All eleven |
| `H_quintic2` | Quintic consequence | All eleven |
| `top_cubic1` | Top-quotient identity | Six top representations |
| `top_cubic2` | Top-quotient identity | Six top representations |
| `top_quartic_a` | Top-quotient identity | Six top representations |
| `top_quartic_aa` | Top-quotient identity | Six top representations |
| `top_quartic_b` | Top-quotient identity | Six top representations |
| `quotient_zero_K1` | Top-quotient identity | Six top representations |
| `quotient_zero_K2` | Top-quotient identity | Six top representations |
| `quotient_zero_U1` | Top-quotient identity | Six top representations |
| `quotient_zero_U2` | Top-quotient identity | Six top representations |

## Extending the inventory

An explicit word-and-coefficient formula for the degree-seven braid relation
would extend the braid-generator checks. The manifest records this as an open
encoding task. The displayed six-generator H,K,U equalities are covered by the
checks above; [REPORT.md](REPORT.md) describes their scope and reproduction.
