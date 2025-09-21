a = float(input())
b = float(input())
c = float(input())

numbers = {a, b, c}
nums = []

for num in numbers:
    if num % 3 == 0:
        nums.append(num)
    else:
        pass

if len(nums) != 0:
    print(max(nums))
else:
    print('NO')
    print(min((a+b, b+c, a+c)))
