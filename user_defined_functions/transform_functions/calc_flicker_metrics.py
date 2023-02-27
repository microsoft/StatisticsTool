import numpy as np

def calc_flicker_metrics(bin_vec):
    seq_len_vec = []
    seq_num = 1
    curr_seq_len = 1
    prev = bin_vec[0]
    for curr in bin_vec[1:]:
        if prev==curr:
            curr_seq_len = curr_seq_len + 1
        else:
            seq_num = seq_num + 1
            seq_len_vec.append(curr_seq_len)
            curr_seq_len = 1
        prev = curr
    
    # Handle last sequence
    if curr_seq_len>1:
        seq_len_vec.append(curr_seq_len)

    avg_seq_len = np.mean(seq_len_vec)
    med_seq_len = np.median(seq_len_vec)

    return seq_num, avg_seq_len, med_seq_len
