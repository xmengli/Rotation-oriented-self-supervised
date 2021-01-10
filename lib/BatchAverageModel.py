import torch
from torch.autograd import Function
from torch import nn
import math
import numpy as np



def deleteFrom2D(arr2D, row, column):
    'Delete element from 2D numpy array by row and column position'
    arr2D = arr2D.cpu().data.numpy()
    modArr = np.delete(arr2D, row * arr2D.shape[1] + column)
    modArr = torch.from_numpy(modArr).cuda()
    return modArr

class BatchCriterionModel(nn.Module):
    ''' Compute the loss within each batch
    '''

    def __init__(self, negM, T, batchSize, args):
        super(BatchCriterionModel, self).__init__()
        self.negM = negM
        self.T = T
        self.domain = args.domain
        # self.stripe = stripe
        num = 4 if self.domain else 2
        self.diag_mat = 1 - torch.eye(batchSize * num).cuda()

    def forward(self, x, targets):
        batchSize = x.size(0)

        # get positive innerproduct

        losses = []
        for i in range(0, 2):
            reordered_x = torch.cat((x.narrow(0, batchSize // 2, batchSize // 2), \
                                     x.narrow(0, 0, batchSize // 2)), 0)

            if i==1:
                idx = list(np.arange(1, int(batchSize), 2))
                idx1 = np.array([item - 1 for item in idx])
                # idx2 = np.array([item + 2 for item in idx])
                # idx3 = np.array([item - 1 for item in idx])
                idx = np.array(idx)
                index = np.stack([idx, idx1])
                index = list(index.flatten("F"))
                reordered_x = reordered_x[index,:]

            # elif i == 2:
            #     idx = list(np.arange(2, int(batchSize), 4))
            #     idx1 = np.array([item + 1 for item in idx])
            #     idx2 = np.array([item - 2 for item in idx])
            #     idx3 = np.array([item - 1 for item in idx])
            #     idx = np.array(idx)
            #     index = np.stack([idx, idx1, idx2, idx3])
            #     index = list(index.flatten("F"))
            #     reordered_x = reordered_x[index,:]
            # elif i == 3:
            #     idx = list(np.arange(3, int(batchSize), 4))
            #     idx1 = np.array([item - 3 for item in idx])
            #     idx2 = np.array([item - 2 for item in idx])
            #     idx3 = np.array([item - 1 for item in idx])
            #     idx = np.array(idx)
            #     index = np.stack([idx, idx1, idx2, idx3])
            #     index = list(index.flatten("F"))
            #     reordered_x = reordered_x[index,:]

            # reordered_x = reordered_x.data
            print ("x", x)
            print ("reord", reordered_x.data)
            pos = (x * reordered_x.data).sum(1).div_(self.T).exp_()

            # get all innerproduct, remove diag
            all_prob = torch.mm(x, x.t().data).div_(self.T).exp_() * self.diag_mat


            if self.negM == 1:
                all_div = all_prob.sum(1)
                print ("all_prob", all_prob)
                print ("all", all_div)
                exit(0)
            else:
                # remove pos for neg
                all_div = (all_prob.sum(1) - pos) * self.negM + pos

            lnPmt = torch.div(pos, all_div)

            # negative probability
            Pon_div = all_div.repeat(batchSize, 1)
            lnPon = torch.div(all_prob, Pon_div.t())
            lnPon = -lnPon.add(-1)

            # equation 7 in ref. A (NCE paper)
            lnPon.log_()
            # also remove the pos term
            lnPon = lnPon.sum(1) - (-lnPmt.add(-1)).log_()
            lnPmt.log_()

            lnPmtsum = lnPmt.sum(0)
            lnPonsum = lnPon.sum(0)

            # negative multiply m
            lnPonsum = lnPonsum * self.negM
            loss = - (lnPmtsum + lnPonsum) / batchSize

            # losses += loss
            losses.append(loss)
        losses = losses[0] + 0.5*losses[1]

        return losses

