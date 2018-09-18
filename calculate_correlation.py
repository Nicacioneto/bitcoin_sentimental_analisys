import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

train_df = pd.read_csv('2018-09-11-tweets-cl.csv')

plt.imshow(train_df.cov())
plt.colorbar()

plt.show()
