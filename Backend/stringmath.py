inp = "2+12*4+50+2*2"

def multiply_list(lst):
    mult_total = 1
    for i in lst:
        mult_total *= i
    return mult_total

plusses = inp.split("+")
mults = [plus.split('*') for plus in plusses]
[total := total * num for num in numbers]
print(sum([multiply_list([int(ll) for ll in lst]) for lst in mults]))


