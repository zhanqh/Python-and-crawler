# for n in range(2, 10):
#     for x in range(2, n):
#         print('先输出', n)
#         break
#         if n % x == 0:
#             print('tag', x)
#             print(n, '非素数')
#             break
#     else:
#         print(n, '素数')
#         

def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

