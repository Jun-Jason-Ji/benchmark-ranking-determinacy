# Directional IUT correction and frozen-data verification

The sign-consistency requirement is now applied before Holm or BH, via two directional intersection-union tests. No episode records or scientific effect-size estimates changed.

## Regression checks

- PASS: Opposite strong signs give p=1.
- PASS: A degenerate zero gap cannot establish strict ordering.
- PASS: Nonzero zero-SE gaps retain the explicitly degenerate working-model behavior.
- PASS: A common sign uses the least significant condition; sign reversal is symmetric.
- PASS: A noisy zero point estimate gives p=1.
- PASS: Mixed-sign evidence cannot occupy an early Holm rank.
- PASS: Empty and invalid variance inputs fail explicitly.

## Counts before and after (identical)

| Method | Point | Envelope | Disagreement |
|---|---:|---:|---:|
| uncorrected | 11 | 10 | 1 |
| Holm | 9 | 5 | 4 |
| BH | 11 | 10 | 1 |

## Per-pair p values

| Task | Policy A | Policy B | Point p (unchanged) | Envelope p before | Envelope p after |
|---|---|---|---:|---:|---:|
| eggplant (ms3) | octo-small | octo-base | 0.0867881885545 | 0.0867881885545 | 0.0867881885545 |
| eggplant (ms3) | octo-small | octo-small@hist1 | 0.0248720945714 | 0.0248720945714 | 0.0248720945714 |
| eggplant (ms3) | octo-small | octo-base@hist1 | 4.75475285225e-05 | 0.020595451555 | 0.020595451555 |
| eggplant (ms3) | octo-small | openvla-7b-4bit | 2.25383861023e-23 | 1.12924481676e-15 | 1.12924481676e-15 |
| eggplant (ms3) | octo-base | octo-small@hist1 | 0.603765148565 | 0.603765148565 | 1 |
| eggplant (ms3) | octo-base | octo-base@hist1 | 0.0242653201334 | 0.987209402167 | 1 |
| eggplant (ms3) | octo-base | openvla-7b-4bit | 8.65141173319e-16 | 2.68983692536e-05 | 2.68983692536e-05 |
| eggplant (ms3) | octo-small@hist1 | octo-base@hist1 | 0.0854058082846 | 0.116664464781 | 1 |
| eggplant (ms3) | octo-small@hist1 | openvla-7b-4bit | 5.60784182663e-14 | 6.7664004218e-07 | 6.7664004218e-07 |
| eggplant (ms3) | octo-base@hist1 | openvla-7b-4bit | 2.59914529431e-09 | 0.0101001299337 | 0.0101001299337 |
| spoon (ms3) | octo-small | octo-base | 4.06215042866e-06 | 0.0184221254541 | 0.0184221254541 |
| carrot (ms3) | octo-small | octo-base | 0.317310507863 | 0.479500122187 | 0.479500122187 |
| eggplant (ms2, original stack) | octo-small | octo-base | 0.438578026081 | 0.466854270823 | 0.466854270823 |
| eggplant (ms2, original stack) | octo-small | openvla-7b-4bit | 2.55962508777e-12 | 2.55962508777e-12 | 2.55962508777e-12 |
| eggplant (ms2, original stack) | octo-base | openvla-7b-4bit | 2.00489608028e-13 | 5.73303143758e-07 | 5.73303143758e-07 |
| spoon (ms2, original stack) | octo-small | octo-base | 0.001565402258 | 0.011412036386 | 0.011412036386 |
| carrot (ms2, original stack) | octo-small | octo-base | 1 | 1 | 1 |

Three mixed-sign rows now have p=1. All reported declaration counts remain unchanged. The full precision values are in DIRECTIONAL_IUT_VERIFICATION.json. The validity of all normal-tail calculations remains conditional on the stated variance model.
