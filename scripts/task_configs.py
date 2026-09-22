"""Distinct initial-configuration counts of the SIMPLER bridge tasks, and helpers for config-census analysis.

Both stacks map episode_id to a fixed initial state:
  ManiSkill3 (mani_skill/envs/tasks/digital_twins/bridge_dataset_eval/base_env.py:_initialize_episode)
  ManiSkill2_real2sim (envs/custom_scenes/put_on_in_scene.py:_initialize_actors)
    pos  = (episode_id % (n_xy * n_quat)) // n_quat
    quat =  episode_id % n_quat
so episode_id >= n_xy * n_quat repeats an earlier configuration exactly. With a deterministic policy
(OpenVLA: do_sample=False and the per-episode seed is ignored) a repeated config reproduces the episode
bit-for-bit, so such episodes carry no new information and must not be counted as independent samples.
With a stochastic policy (Octo samples its diffusion head from jax.random.PRNGKey(policy_seed)) a repeated
config is a new draw of policy noise on an already-seen configuration.

Verified 2026-09-19: openvla nominal records of seed sets B (20270101) and C (20280101) are identical in
48/48 episodes; seed sets differ for OpenVLA only through run-to-run GPU nondeterminism.
"""

# env_id -> (n_xy_configs, n_quat_configs)
GRIDS = {
    # ManiSkill3 (SimplerEnv-ms3)
    "PutEggplantInBasketScene-v1": (8, 8),
    "PutSpoonOnTableClothInScene-v1": (12, 2),
    "PutCarrotOnPlateInScene-v1": (12, 2),
    "StackGreenCubeOnYellowCubeBakedTexInScene-v1": (24, 1),
    # ManiSkill2_real2sim (original SIMPLER main)
    "PutEggplantInBasketScene-v0": (8, 3),
    "PutSpoonOnTableClothInScene-v0": (12, 2),
    "PutCarrotOnPlateInScene-v0": (12, 2),
    "StackGreenCubeOnYellowCubeBakedTexInScene-v0": (24, 1),
}

# The fractal / google-robot suite enumerates its configurations differently: not (object xy x quaternion)
# indexed by episode_id, but the outer product the official visual-matching script sweeps --
# urdf_version x object orientation x a linspace grid of object xy (scripts/octo_pick_coke_can_visual_matching.sh).
# The published rate is the mean over all of them, so the estimand is an average over a *visual* variation
# (urdf_version) as well as a physical one; see docs/paper_draft_s5 on what a benchmark number averages over.
TOTALS = {
    "GraspSingleOpenedCokeCanInScene-v0": 4 * 3 * (5 * 5),  # urdf variants x can orientations x xy grid = 300
}

DETERMINISTIC_POLICIES = ("openvla",)  # prefix match on the policy name


def n_configs(env_id):
    """Number of distinct initial configurations, or None when the env is unknown."""
    if env_id in TOTALS:
        return TOTALS[env_id]
    g = GRIDS.get(env_id)
    return g[0] * g[1] if g else None


def config_id(env_id, episode_id):
    """The configuration an episode_id lands on (episodes with equal config_id share the initial state)."""
    n = n_configs(env_id)
    return episode_id % n if n else episode_id


def is_deterministic(policy):
    return policy.split("@")[0].startswith(DETERMINISTIC_POLICIES)


def census_episodes(env_id, policy, episode_ids):
    """Episode ids to keep so that each configuration is counted once for a deterministic policy
    (first occurrence wins) and all episodes are kept for a stochastic one."""
    ids = sorted(episode_ids)
    if not is_deterministic(policy):
        return ids
    seen, keep = set(), []
    for e in ids:
        c = config_id(env_id, e)
        if c not in seen:
            seen.add(c)
            keep.append(e)
    return keep
