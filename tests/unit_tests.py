from ktypes import types
from ktypes._error import ErrorHandler, Error
import random

tests = []

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = "\033[33m"
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

g_reports = None

def run(*args):
    ErrorHandler.set_response_instruct("pass")
    failed_tests = []
    successes = 0
    total = 0
    # random.shuffle(tests)
    for test in tests:
        if args:
            if not test.__name__ in args:
                continue
        global g_reports
        g_reports = []
        test()
        total += len(g_reports)
        for r in g_reports:
            if not r:
                failed_tests.append(test.__doc__)
                print(colors.RED + "." + colors.END, end="")
            else:
                print(colors.GREEN + "." + colors.END, end="")
                successes += 1
    if total == 0:
        print(colors.YELLOW + "no tests reporting" + colors.END)
        return
    print()
    print(colors.YELLOW + f"{total} reporting, " + \
        colors.GREEN + f"{successes} succeeded ({int(100*successes/total)}%), " + \
        colors.RED + f"{len(failed_tests)} failed" + colors.END)

    for failed_test in failed_tests:
        print(colors.YELLOW + ">> " + colors.RED + failed_test + colors.END)


def reports(val):
    g_reports.append(val)

def unit_test(f):
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    tests.append(wrapper)

    return None

def context(f):
    f()


class expect():
    def __init__(self, result):
        self.result = result
        self._knot = False

    def to_equal(self, val):
        if self._knot:
            reports(self.result != val)
        else:
            reports(self.result == val)

    def to_be(self, val):
        self.to_equal(val)

    def is_instance(self, type):
        if self._knot:
            reports(not isinstance(self.result, type))
        else:
            reports(isinstance(self.result, type))


    def knot(self):
        self._knot = True
        return self




################################################################################
# helpers
def is_hello(raw_data):
    return raw_data == "hello"

def contains_hello(raw_data):
    return "hello" in raw_data

def is_dash(raw_data):
    return raw_data == "-"

@types.function
def f(a : types.int, b : types.int, c: types.str) -> types.str:
    sum_str = str(a.value + b.value)
    return types.str(sum_str + c.value)

product_ktype = types.product({
    "a": types.int,
    "b": types.int,
    "c": types.str,
})

bounded_product_ktype = types.product({
    "a": types.int,
    "b": types.int.where(size_eq=5),
    "c": types.str.where(ends_on="\n"),
})
    
################################################################################
# tests
@unit_test
def construct_int():
    "tests the construction of an int type"
    result = types.int("100")
    expect(result.value).to_equal(100)

@unit_test
def construct_int_token():
    "tests the construction of an int type returns a token"
    result = types.int("100")
    expect(type(result)).to_equal(types.Token)

@unit_test
def construct_str():
    "tests the construction of a string type"
    result = types.str("hello")
    expect(result.value).to_equal("hello")

@unit_test
def custom_predicate():
    "tests creating a type with custom predicate"
    result = types.str.where(predicate=is_hello)
    expect(result.matches("hello")).to_be(True)
    expect(result.matches("not hello")).to_be(False)

@unit_test
def predicates_are_unique():
    "tests that adding predicates only creates a new type once"
    pred1 = types.str.where(predicate=is_hello) 
    pred2 = types.str.where(predicate=is_hello)
    expect(pred1).to_be(pred2)

@unit_test
def inbuilt_predicates():
    "tests size_eq and ends_on predicates"
    pred1 = types.str.where(ends_on=" ")
    expect(pred1.matches("hello")).to_be(True)
    expect(pred1.matches("hello ")).to_be(False)

    pred2 = types.str.where(size_eq=4)
    expect(pred2.matches("four")).to_be(True)
    expect(pred2.matches("not four")).to_be(False)

    expect(pred1).knot().to_be(pred2)

@unit_test
def multipe_predicates():
    "tests multiple predicates on a type"
    pred1 = types.str.where(ends_on=" ", predicate=contains_hello)
    expect(pred1.matches("hello ")).to_be(False)
    expect(pred1.matches("hi ")).to_be(False)
    expect(pred1.matches("hello")).to_be(True)

    pred2 = types.str.where(ends_on=" ", predicate=contains_hello)
    expect(pred1).to_equal(pred2)

    pred3 = types.str.where(ends_on=".", predicate=contains_hello, size_eq=7)
    expect(pred3.matches("hello.7")).to_be(False)
    expect(pred3.matches("hello67")).to_be(True)

@unit_test
def coproduct_type():
    "tests defining a named coproduct type"
    types.coproduct_type = types.int | types.str.where(size_eq=5)
    expect(types.coproduct_type.matches("445")).to_be(True)
    expect(types.coproduct_type.matches("hello")).to_be(True)

    expect(types.coproduct_type).to_equal(types.int | types.str.where(size_eq=5))

@unit_test
def coproduct_type_ignores_order():
    "tests that a coproduct type ignores the order of component types"
    prod1 = types.int | types.str.where(size_eq=5)
    prod2 = types.str.where(size_eq=5) | types.int
    expect(prod1).to_be(prod2)

    prod3 = prod1 | types.int.where(predicate=is_hello)
    prod4 = types.str.where(size_eq=5) | types.int.where(predicate=is_hello) | types.int
    expect(prod3).to_be(prod4)

@unit_test
def allow_named_types():
    "tests the syntax to define named types"
    types.allow_named_types_int = types.int
    expect(types.allow_named_types_int.matches("1004")).to_be(True)
    expect(types.allow_named_types_int).to_be(types.int)

@unit_test
def curry_functions():
    "tests function currying"
    expect(str(f)).to_equal("f : int -> int -> str -> str")
    result = types.str("210 is the sum")
    a = types.int(10)
    b = types.int(200)
    c = types.str(" is the sum")
    expect(f(a, b, c)).to_equal(result)
    expect(f(a)(b)(c)).to_equal(result)
    expect(f(a, b, c).type).to_be(types.str)

    expect(str(f(a, b))).to_be("klambda<f> : str -> str")

    g = f(a)
    expect(g(b, c)).to_equal(result)
    expect(g(b)(c)).to_equal(result)

@unit_test
def product_inductor():
    "tests inducing a function on product types"
    f_prod = types.ind_prod(f)
    
    instance_dict = {
        "a": types.int(10),
        "b": types.int(200),
        "c": types.str(" is the sum")
    }
    p = product_ktype(instance_dict)

    expect(f_prod(p).value).to_equal("210 is the sum")

@context
def product_type():
    @unit_test
    def product_type_error_handling():
        "tests failure to construct product type"
    
        bad_instance_dict = {
            "a": types.int(10),
            "b": types.int(200),
            "d": types.str(" is the sum")
        }

        expect(product_ktype(bad_instance_dict)).is_instance(Error.OfTypeMismatch)
        expect(product_ktype([])).is_instance(Error.OfArgument)    

@unit_test
def uncallable_types():
    "tests that basic types are uncallable"
    x = types.int(45) 
    expect(x()).is_instance(Error.OfUncallable)
    y = types.str("hello")
    expect(y()).is_instance(Error.OfUncallable)

@unit_test
def instance_parser():
    "tests the auto generated parser for single instances"
    parse_format = "$a$ $b$, $c$\n"
    parser = types.parser(bounded_product_ktype, parse_format)
    result = parser.parse_instance("1245 43454, hello there\n extraneous")
    expect(type(result)).to_be(types.Token)
    expect(result.type).to_be(bounded_product_ktype)
    expect(result.c.value).to_be("hello there")
    expect(result.a.value).to_be(1245)

@unit_test
def stream_parser():
    "tests the auto generated parser for stream inputs"
    parse_format = "$a$ $b$, $c$\n"
    parser = types.parser(bounded_product_ktype, parse_format)
    result = parser.parse_stream("1245 43454, hello there\n434 44922, something word\n")
    expect(type(result[0])).to_be(types.Token)
    expect(result[0].c.value).to_be("hello there")
    expect(result[1].a.value).to_be(434)

@unit_test
def token_equality():
    "tests proper equality behavior on token objects"
    int1 = types.int("1200")
    int2 = types.int("1200")
    expect(int1).to_be(int2)
    
    instance_dict1 = {
        "a": types.int(10),
        "b": types.int(200),
        "c": types.str(" is the sum")
    }
    instance_dict2 = {
        "a": types.int(10),
        "b": types.int(200),
        "c": types.str(" is the sum")
    }
    prod1 = product_ktype(instance_dict1)
    prod2 = product_ktype(instance_dict2)
    expect(prod1).to_be(prod2)

    or_type = types.int | types.str
    or_token1 = or_type("594")
    or_token2 = or_type("594")
    expect(or_token1).to_be(or_token2)

@context
def coproducts_on_functions():
    @types.function
    def f(a : types.int) -> types.str:
        return types.str(-a.value)
    
    @types.function
    def g(b : types.str.where(size_eq=4)) -> types.str:
        return types.str(b.value)

    @types.function
    def h(b : types.str.where(predicate=is_dash)) -> types.str:
        return types.str("NULL")

    @types.function
    def a(x : types.str, y : types.str) -> types.str:
        return y

    @types.function
    def b(x : types.int) -> types.str:
        return types.str("-")

    @types.function
    def c(x : types.int) -> types.int:
        return x

    @unit_test
    def coproduct_function_failure_cases():
        "tests function or constructor failure cases"
        expect(a | f).is_instance(Error.OfOrConstructorFailure)
        expect(b | f).is_instance(Error.OfOrConstructorFailure)
        expect(c | g).is_instance(Error.OfOrConstructorFailure)

    @unit_test
    def coproduct_function():
        "tests creating a coproduct function"
        coprod = types.int | types.str.where(size_eq=4) | types.str.where(predicate=is_dash)
        coprod_func = f | g | h
        expect(coprod_func.type.signature[0]).to_be(coprod)
        expect(coprod_func.type.signature[1]).to_be(types.str)

        t1 = coprod("-")
        expect(coprod_func(t1)).to_be(types.str("NULL"))
        t2 = coprod("four")
        expect(coprod_func(t2)).to_be(types.str("four"))
        t3 = coprod("4403")
        expect(coprod_func(t3)).to_be(types.str("-4403"))

@context
def basic_ops():
    int1 = types.int(10)
    int2 = types.int(15)

    str1 = types.str("hello")
    str2 = types.str(" world")

    @unit_test
    def addition():
        "tests adding basic types"
        expect(int1 + int2).to_be(types.int(25))
        expect(str1 + str2).to_be(types.str("hello world"))
        expect(int1 + str1).is_instance(Error.OfBinaryOperation)

    @unit_test
    def subtraction():
        "tests subtracting basic types"
        expect(int1 - int2).to_be(types.int(-5))
        expect(str1 - str2).is_instance(Error.OfBinaryOperation)

    @unit_test
    def multiplication():
        "tests multipyling basic types"
        expect(int1 * int2).to_be(types.int(150))
        expect(str1 * str2).is_instance(Error.OfBinaryOperation)

    @unit_test
    def division():
        "tests dividing basic types"
        expect(types.int(30) / int2).to_be(types.int(2))
        expect(str1 / str2).is_instance(Error.OfBinaryOperation)



@unit_test
def sandbox():
    "sandbox test"
    expect(True).to_be(True)