import os
import sys
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm

class DamaNet(nn.Module):
    def __init__(self, game, args):
        super(DamaNet, self).__init__()
        
        # Game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args
        
        # Neural Net
        # Input: 4 kanal (beyaz taşlar, siyah taşlar, beyaz damalar, siyah damalar)
        self.conv1 = nn.Conv2d(4, 512, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        
        self.bn1 = nn.BatchNorm2d(512)
        self.bn2 = nn.BatchNorm2d(512)
        self.bn3 = nn.BatchNorm2d(512)
        
        # 2 fully connected layer
        self.fc1 = nn.Linear(512*8*8, 1024)
        self.fc2 = nn.Linear(1024, 512)
        
        # Policy head
        self.fc_policy = nn.Linear(512, self.action_size)
        
        # Value head
        self.fc_value = nn.Linear(512, 1)
        
    def forward(self, s):
        s = s.view(-1, 4, self.board_x, self.board_y)
        
        # Convolution layers
        s = F.relu(self.bn1(self.conv1(s)))
        s = F.relu(self.bn2(self.conv2(s)))
        s = F.relu(self.bn3(self.conv3(s)))
        s = s.view(-1, 512 * self.board_x * self.board_y)
        
        # Fully connected layers
        s = F.relu(self.fc1(s))
        s = F.relu(self.fc2(s))
        
        # Policy head
        pi = self.fc_policy(s)
        
        # Value head
        v = self.fc_value(s)
        
        return F.log_softmax(pi, dim=1), torch.tanh(v)

class NNetWrapper:
    def __init__(self, game, args):
        self.nnet = DamaNet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args
        
        if args.cuda:
            self.nnet.cuda()

    def train(self, examples):
        optimizer = torch.optim.Adam(self.nnet.parameters())
        
        for epoch in range(self.args.epochs):
            self.nnet.train()
            pi_losses = []
            v_losses = []
            
            batch_count = int(len(examples) / self.args.batch_size)
            t = tqdm(range(batch_count), desc=f'Epoch {epoch+1}')
            
            for _ in t:
                sample_ids = np.random.randint(len(examples), size=self.args.batch_size)
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))
                
                if self.args.cuda:
                    boards, target_pis, target_vs = boards.cuda(), target_pis.cuda(), target_vs.cuda()
                    
                out_pi, out_v = self.nnet(boards)
                
                l_pi = -torch.sum(target_pis * out_pi) / target_pis.size()[0]
                l_v = torch.sum((target_vs - out_v.view(-1)) ** 2) / target_vs.size()[0]
                total_loss = l_pi + l_v
                
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()
                
                pi_losses.append(float(l_pi))
                v_losses.append(float(l_v))
                
                t.set_postfix(Loss_pi=np.mean(pi_losses), Loss_v=np.mean(v_losses))

    def predict(self, board):
        board = torch.FloatTensor(board.astype(np.float64))
        if self.args.cuda:
            board = board.cuda()
            
        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(board)
            
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        torch.save({
            'state_dict': self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise Exception(f"No model in path {filepath}")
            
        checkpoint = torch.load(filepath)
        self.nnet.load_state_dict(checkpoint['state_dict'])