import os
import time
import torch
import pygame
import numpy as np
from tqdm import tqdm
from snake import Snake
from painter import Painter
from ppo import ReplayBuffer
from agent import AgentDiscretePPO


MAX_EPISODE = 800


def testAgent(test_env, agent):
    ep_reward = 0
    o = test_env.reset()
    for _ in range(650):
        for _ in pygame.event.get():
            pass  # If you don't add this render, it will freeze

        a_int, _ = agent.select_action(o)
        o2, reward, done, _ = test_env.step(a_int)
        ep_reward += reward
        if done:
            break

        o = o2

    return ep_reward


def time_stamp(episode, rwd):
    now = int(round(time.time() * 1000))
    res = time.strftime("_%Y-%m-%d-%H-%M-%S_", time.localtime(now / 1000))
    res += str(episode) + "_" + str(rwd)
    return res


def save_model(episode, ep_reward):
    log_path = "./history/"
    print("Save model!")
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    torch.save(
        agent.act.state_dict(),
        f"{log_path}act-weight{time_stamp(episode, ep_reward)}.pkl",
    )


if __name__ == "__main__":
    env = Snake()
    test_env = Snake()
    act_dim = 4
    obs_dim = 6
    agent = AgentDiscretePPO()
    agent.init(512, obs_dim, act_dim, if_use_gae=True)
    agent.state = env.reset()
    buffer = ReplayBuffer(2**12, obs_dim, act_dim, True)
    batch_size = 256
    rewardList = []
    maxReward = -np.inf

    for episode in tqdm(range(MAX_EPISODE), desc="Training agent..."):
        with torch.no_grad():
            trajectory_list = agent.explore_env(env, 2**12, 1, 0.99)

        buffer.extend_buffer_from_list(trajectory_list)
        agent.update_net(buffer, batch_size, 1, 2**-8)
        ep_reward = testAgent(test_env, agent)
        rewardList.append(ep_reward)
        if episode > MAX_EPISODE / 3 and ep_reward > maxReward:
            maxReward = ep_reward
            save_model(episode, ep_reward)

    pygame.quit()
    rwd_path = f"./history/reward{time_stamp(MAX_EPISODE, maxReward)}.csv"
    painter = Painter(load_csv=True, load_dir=rwd_path)
    painter.addData(rewardList, "PPO")
    painter.saveData(rwd_path)
    painter.setTitle("snake game reward")
    painter.setXlabel("episode")
    painter.setYlabel("reward")
    painter.drawFigure()
