t = int(input())
for _ in range(t):
    n = int(input())
    
    if n == 2 or n == 3:
        print(-1)
    else:
        perm = []
        left, right = 1, n
        while left <= right:
            perm.append(right)
            right -= 1
            if left <= right:
                perm.append(left)
                left += 1
        print(*perm)