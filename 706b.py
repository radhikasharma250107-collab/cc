n = int(input())
prices = list(map(int, input.split()))
prices.sort()
q = int(input())
for i in range(q):
    m = int(input())

    l = 0
    r = n-1
    ans = 0
    while l<r:
        mid = l + (r-l)/2
        if prices[n] <= m:
            ans = mid+1
            l = mid+1
        else:
            r = mid-1
    print(ans)