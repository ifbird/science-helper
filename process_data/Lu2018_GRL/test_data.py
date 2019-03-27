import numpy as np

old = np.load('/homeappl/home/putian/scripts/tm5-mp/prepare_MH_input/data1_reg11.npz')
# print(old['lu2018_pi'][()].keys())
cvl_pi_old = old['lu2018_pi'][()]['cvl_dom_avg_reg11']

new = np.load('data1_pi.npz')
cvl_pi_new = new['cvl_dom_avg_11']

print(np.max(np.abs(cvl_pi_new - cvl_pi_old)))
