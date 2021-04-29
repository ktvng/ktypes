from ktypes import types
def clear():
    x = input()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

print("press enter to cycle through the demo")
clear()


################################################################################
# Defining a type with a predicate
types.nan = types.str.where(lambda x: x == "--")



################################################################################
# Defining a coproduct type
types.maybe_age = types.int | types.nan



################################################################################
# Defining a product type
types.site_user = {
    "id": types.int,
    "first_name": types.str.where(ends_on=","),
    "last_name": types.str.where(ends_on=","),
    "email": types.str.where(ends_on=","),
    "age": types.maybe_age,
    "ip_address": types.str.where(ends_on="\n")
}



################################################################################
# Parsing
format = "$id$,$first_name$,$last_name$,$email$,$age$,$ip_address$"
parser = types.parser(types.site_user, format)

tokens = None
with open("demo/demo_data.csv") as f:
    for line in f:
        tokens = parser.parse_stream(line)

for i in range(0, 5):
    print(tokens[i])
clear()



################################################################################
# Defining a function on coproduct types
@types.function
def a(x : types.int) -> types.str:
    return types.str(x.value)

@types.function
def b(x : types.nan) -> types.str:
    return types.str("unknown age")

age_to_str = a | b

print(age_to_str)
clear()



################################################################################
# Typecasting between convertable types
@types.function
def typecast_str(x : types.str.where(ends_on=",")) -> types.str:
    return types.str(x.value)



################################################################################
# Defining a curried function
@types.function
def add(x : types.int, y : types.int) -> types.int:
    return x + y

add5 = add(types.int(5))

print(add)
print(add5)

print(add5(types.int(15)))
clear()



@types.function
def stringify(
        id : types.int, 
        f_name : types.str.where(ends_on=","),
        l_name : types.str.where(ends_on=","),
        email : types.str.where(ends_on=","),
        age : types.maybe_age,
        ip : types.str.where(ends_on="\n")) -> types.str:
    return typecast_str(f_name) + types.str(" is ") + age_to_str(age)

f = types.ind_prod(stringify)

print(stringify)
print(f)
clear()

print(f(tokens[0]))
print(f(tokens[1]))
clear()
