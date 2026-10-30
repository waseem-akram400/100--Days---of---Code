import numpy as np

# 1. Apne 100 din wali mehnat ka data
days = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
hours = np.array([2, 3, 1, 2, 2, 3, 2, 2, 1, 3])


print("Total din:", len(days))
print("Total hours parhay:", np.sum(hours))
print("Roz ka average:", np.mean(hours))
print("Sab se zyada ek din me:", np.max(hours))

# 2. Thora sa AI wala kaam
# Agar aise hi chalte rahe to 30 din me kitne ghante ho jayenge?
print("30 din me andaza:", np.mean(hours) * 30)
