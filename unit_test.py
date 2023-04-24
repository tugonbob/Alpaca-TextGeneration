from ml_context_generator import MLContextGenerator
from context_generator import ContextGenerator
import time

# ml = MLContextGenerator('Tiffany.pkl')
# context = ml.generate_context("What are you symptoms")
# print(context)

cg = ContextGenerator()
start = time.time()
context = cg.generate_context("What are you symptoms")
print(context)
print(time.time() - start)
