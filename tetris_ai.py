import tetris_game_logic as tgl
import numpy as np
from collections import deque
import random
import sys
import time
import os
import pickle

class TetrisQLearning:
    def __init__(self):
        # Tetris Game
        self.tetris_game = tgl.TetrisGameLogic()
        self.num_actions = 4

        # Epsilon Greedy policy parameters
        self.epsilon = 1
        self.epsilon_min = 0.2
        self.epsilon_decay = 0.99999

        # Q Learning
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.q_table = dict()

        # Memory Buffer
        self.batch_size = 512
        self.memory_max_len = self.batch_size * 100
        self.memory = deque(maxlen=self.memory_max_len)

        # Env Tetris
        self.terminated = False

        # Train
        self.step = 0
        self.action = 0
        self.reward = 0
        self.num_episodes = 0

        # Render
        self.state = np.array(self.tetris_game.get_grid_shape(), dtype=np.uint8)
        self.score = 0

        # Save dir
        self.save_dir = 'train_ql'

    def tetris_reset(self):
        self.tetris_game.new_game()
        self.terminated = False
        self.state = self.tetris_game.get_init_state_ai()
        self.reward = self.tetris_game.get_reward()
        self.score = self.tetris_game.score
        return self.array_2_key(self.state)
    
    def tetris_step(self, action):    
        if action == 0:
            self.tetris_game.move_tetromino_down()
        elif action == 1:
            self.tetris_game.move_tetromino_left()
        elif action == 2:
            self.tetris_game.move_tetromino_right()
        elif action == 3:
            self.tetris_game.rotate_tetromino()

        # self.reward = self.tetris_game.get_reward()
        self.reward = tgl.a_get_reward(self.tetris_game)
        self.state = self.tetris_game.get_state_ai()
        self.score = self.tetris_game.score
        
        if self.tetris_game.game_over:
            self.terminated = True

        return self.array_2_key(self.state)
    
    def ensure_q_values_for_state(self, state_key):
        if state_key in self.q_table:
            return
        # self.q_table[state_key] = np.random.rand(self.num_actions)
        self.q_table[state_key] = np.zeros(self.num_actions)

    def epsilon_greedy_policy(self, state_key):
        if np.random.rand() < self.epsilon:
            return random.choice(range(self.num_actions))
        
        self.ensure_q_values_for_state(state_key)
        return np.argmax(self.q_table[state_key])


    def greedy_policy(self, state_key):
        self.ensure_q_values_for_state(state_key)
        return np.argmax(self.q_table[state_key])        
    
    def init_collect_states(self, num_init_states):
        state_key = self.tetris_reset()
        for i in range(num_init_states):
            print(f'\rColleting {i} states', end='')
            if self.terminated:
                state_key = self.tetris_reset()
            self.action = self.epsilon_greedy_policy(state_key)
            next_state_key = self.tetris_step(self.action)
            self.memory.append((state_key, self.action, self.reward, next_state_key, self.terminated))
            state_key = next_state_key
        print()
    
    def train(self, num_steps):
        print(f'Number of steps: {num_steps}')
        total_score = 0
        self.init_collect_states(self.batch_size*100)
        avg_reward_deque = deque(maxlen=10)
        avg_reward = 0
        acc_reward = 0
        start_time = time.time()
        state_key = self.tetris_reset()
        
        while self.step < num_steps:
            if self.terminated:
                total_score += self.score
                if self.score > 0:
                    print(f'\nEp: {self.num_episodes}, Sc: {self.score}')
                state_key = self.tetris_reset()
                self.num_episodes += 1
                avg_reward_deque.append(acc_reward)
                avg_reward = np.mean(avg_reward_deque)
                acc_reward = 0
                
            self.action = self.epsilon_greedy_policy(state_key)
            next_state_key = self.tetris_step(self.action)
            self.memory.append((state_key, self.action, self.reward, next_state_key, self.terminated))
            state_key = next_state_key
            self.step += 1
            self.update_q_table()
            acc_reward += self.reward
            
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

            if self.step % 1000 == 0:
                print(f'\re: {self.epsilon:.2f}, NEp: {self.num_episodes}, St: {self.step}, TSc: {total_score}, AvgR: {avg_reward:+10.2f}, TiEl: {time.time() - start_time}', end='')
                start_time = time.time()
                if self.step % 1000000 == 0:
                    t_old_time = self.tetris_game._old_time
                    save_info = self.save_data()
                    print('\nSaved:', save_info)
                    self.tetris_game._old_time = t_old_time

            # self.tetris_render_cli(f'Num Episodes: {self.num_episodes}\nStep: {self.step}\nScore: {self.score}\nAction: {self.action}\nReward: {self.reward}\nAvgR: {avg_reward}')

    def update_q_table(self):
        samples = random.sample(self.memory, self.batch_size)
        
        # total_td_error = 0

        for state_key, action, reward, next_state_key, terminated in samples:
            self.ensure_q_values_for_state(state_key)
            self.ensure_q_values_for_state(next_state_key)

            if terminated:
                target_q_value = reward
            else:
                target_q_value = reward + self.discount_factor * np.max(self.q_table[next_state_key])
            
            td_error = target_q_value - self.q_table[state_key][action]
            self.q_table[state_key][action] += self.learning_rate * td_error
            # total_td_error += td_error ** 2

        # return total_td_error / self.batch_size

    def save_data(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        data = {
            'q_table': self.q_table,
            'step': self.step,
            'epsilon': self.epsilon,
        }
        
        filename = os.path.join(self.save_dir, f'tetris_q_learning_data_step_{self.step}.pkl')
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        return f"Data saved at step {self.step} in {filename}"

    def load_data(self, save_dir, step):
        filepath = os.path.join(save_dir, f'tetris_q_learning_data_step_{step}.pkl')

        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.q_table = data['q_table']
        self.step = data['step']
        self.epsilon = data['epsilon']
        print(f"Data loaded from {filepath}")
        time.sleep(1)
            
    def array_2_key(self, array):
        return np.packbits(array > 0).tobytes()
    
    def tetris_render_cli(self, str='\n'):
        # Build the render output
        # result = []
        result = ["\033[H\033[J"]  # Clear the screen
        
        # Render the state
        for row in self.state:
            result.extend('██' if col else '⬛' for col in row)
            result.append("\n")

        # Append score, reward, and other information
        result.append(f'Score: {self.score}\n')
        result.append(str)

        # Write the result to stdout
        sys.stdout.write(''.join(result))
        sys.stdout.flush()

    def evaluate(self, num_episodes):
        rewards = []
        avg_rewards = 0
        for episode in range(num_episodes):
            ep_reward = 0
            state_key = self.tetris_reset()
            while not self.terminated:
                self.action = self.greedy_policy(state_key)
                state_key = self.tetris_step(self.action)
                ep_reward += self.reward
                self.tetris_render_cli(f'Episode: {episode}\nAction: {self.action}\nAvg Rewards: {avg_rewards}\nAcc Reward: {ep_reward}')
                time.sleep(0.01)
            rewards.append(ep_reward)
            avg_rewards = np.mean(rewards)

def main():
    ai = TetrisQLearning()
    # print(f'Save dir: {ai.save_dir}')
    # ai.train(30000000)
    ai.load_data(ai.save_dir, 21000000)
    ai.evaluate(num_episodes=10)

if __name__ == '__main__':
    main()
