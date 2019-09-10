from gym.envs.registration import register
 
register(id='JackOrBetterEnv-v0', 
    entry_point='gym_jackorbetter.envs:JacksEnvironment', 
)