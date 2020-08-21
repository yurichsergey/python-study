import math
import sys

PAYMENT_TYPE_DIFF = 'diff'

PAYMENT_TYPE_ANNUITY = 'annuity'


def calculate_annuity_count_of_months():
    print('Enter the credit principal:')
    principal = float(input())
    print('Enter the monthly payment:')
    monthly_annuity_payment = float(input())
    print('Enter the credit interest:')
    annual_interest_percent = float(input())
    annual_interest = annual_interest_percent / 100.
    monthly_interest = annual_interest / 12  # nominal (monthly) interest rate.
    x_pow = monthly_annuity_payment / (monthly_annuity_payment - monthly_interest * principal)
    period_in_months = math.ceil(math.log(x_pow, 1 + monthly_interest))
    years = period_in_months // 12
    months = period_in_months % 12
    result = f'You need'
    if years > 0:
        result += f' {years} year' + ('s' if years > 1 else '')
    if years > 0 and months > 0:
        result += ' and'
    if months > 0:
        result += f' {months} month' + ('s' if months > 1 else '')
    result += f' to repay the credit!'
    print(result)


def calculate_annuity_monthly_payment():
    print('Enter the credit principal:')
    principal = float(input())
    print('Enter the number of periods:')
    period_in_months = int(input())
    print('Enter the credit interest:')
    annual_interest_percent = float(input())
    annual_interest = annual_interest_percent / 100.
    monthly_interest = annual_interest / 12  # nominal (monthly) interest rate.

    interest_pow = math.pow(1 + monthly_interest, period_in_months)
    monthly_annuity_payment = math.ceil(principal * monthly_interest * interest_pow / (interest_pow - 1))

    result = f'Your annuity payment = {monthly_annuity_payment}'
    # last_monthly_payment = principal - (period_in_months - 1) * monthly_annuity_payment
    # if monthly_annuity_payment != last_monthly_payment:
    #     result += f' with last monthly payment = {last_monthly_payment}'
    result += '!'
    print(result)


def calculate_annuity_principal():
    print('Enter the monthly payment:')
    monthly_payment = float(input())
    print('Enter the count of periods:')
    period_in_months = int(input())
    print('Enter the credit interest:')
    annual_interest_percent = float(input())
    annual_interest = annual_interest_percent / 100.
    monthly_interest = annual_interest / 12  # nominal (monthly) interest rate.

    interest_pow = math.pow(1 + monthly_interest, period_in_months)
    divider = monthly_interest * interest_pow / (interest_pow - 1)
    principal = math.floor(monthly_payment / divider)

    result = f'Your credit principal = {principal}!'
    print(result)


def parse_console_params(args_input):
    parsed_params = {}
    for indArgv in range(1, len(args_input)):
        param = args_input[indArgv]  # str
        parsed_param = param[2:].split('=')
        param_name = parsed_param[0]
        param_value = parsed_param[1] if len(parsed_param) > 1 else None
        parsed_params[param_name] = param_value
    return parsed_params


def cast_console_params(parsed_params):
    int_params = ['periods', ]
    for int_param in int_params:
        int_value = parsed_params.get(int_param)  # str
        if type(int_value) == str and is_int(int_value):
            parsed_params[int_param] = int(int_value)

    float_params = ['interest', 'principal', 'payment', ]
    for float_param in float_params:
        float_value = parsed_params.get(float_param)
        if type(float_value) == str and is_float(float_value):
            parsed_params[float_param] = float(float_value)
    return parsed_params


def is_float(val):
    result = True
    try:
        float(val)
    except ValueError:
        result = False
    return result


def is_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def check_console_params(parsed_params, debug=False):
    is_correct = True
    print(str(parsed_params)) if debug else None
    correct_types = [PAYMENT_TYPE_ANNUITY, PAYMENT_TYPE_DIFF, ]
    payment_type = parsed_params.get('type')
    principal = parsed_params.get('principal')
    periods = parsed_params.get('periods')
    interest = parsed_params.get('interest')
    payment = parsed_params.get('payment')

    if payment_type not in correct_types:
        print('payment_type not in correct_types') if debug else None
        is_correct = False
    # if payment is different each month, so we cannot calculate
    # a number of periods or the principal, therefore, its
    # combination with --payment is invalid
    # For --type=diff, the payment is different each month,
    # so we cannot calculate a number of periods or the principal
    if payment_type == PAYMENT_TYPE_DIFF and payment is not None:
        print('payment is not None for different type') if debug else None
        is_correct = False
    # --interest is specified without the percentage sign. Note that it may
    # accept a floating-point value.
    # Our credit calculator can't calculate the interest.
    if (type(interest) != int and type(interest) != float) or (interest < 0):
        print(f'interest is required. But we got {interest} with type {type(interest)}') if debug else None
        is_correct = False
    # periods is only integer
    if periods is not None and (type(periods) != int or (type(periods) == int and periods <= 0)):
        print('periods is only integer (if defined)') if debug else None
        is_correct = False
    numbers = [interest, principal, payment, periods, ]

    # For differentiated payments we need 3 out of 4 parameters
    # (excluding payment), and the same is true for annuity payments
    # (missing either a number of periods, the payment, or the principal).
    count_numbers = 0
    for number1 in numbers:
        if type(number1) == float or type(number1) == int:
            count_numbers += 1
    if count_numbers != 3:
        print(f'we need exactly 3 arguments, but got: {count_numbers}') if debug else None
        is_correct = False

    # numbers are only positive
    for number2 in numbers:
        if (type(number2) == float or type(number2) == int) and (number2 < 0):
            print(f'number {number2} must only positive') if debug else None
            is_correct = False

    return is_correct


def calculate_diff_monthly_payment(params):
    principal = params.get('principal')
    periods = params.get('periods')
    interest = params.get('interest')
    average_principal = principal / periods
    nominal_interest_rate = interest / 100. / 12.
    payments = []
    for month1 in range(1, periods + 1):
        month_payment = math.ceil(average_principal * (1. + nominal_interest_rate * (periods - (month1 - 1))))
        payments.append(month_payment)
    for i in range(len(payments)):
        month2 = i + 1
        print(f'Month {month2}: paid out {payments[i]}')
    overpayment = math.ceil(sum(payments) - principal)
    print(f'\nOverpayment = {overpayment}')


def process_params(args_input):
    params = cast_console_params(parse_console_params(args_input))
    if not check_console_params(params, debug=False):
        print('Incorrect parameters')
        # exit(-1)
        return
    if params['type'] == PAYMENT_TYPE_DIFF:
        calculate_diff_monthly_payment(params)
    # calculate_annuity_monthly_payment()
    # calculate_annuity_count_of_months()
    # calculate_annuity_principal()


def test_parse_params():
    for args in get_test_cases():
        params = check_console_params(cast_console_params(parse_console_params(args)), debug=True)
        print('Result==> ' + str(params))


def test_run_params():
    for args in get_test_cases():
        process_params(args)


def get_test_cases():
    script_name = __file__
    test_args = [
        # [script_name, '--type=diff', '--principal=1000000', '--periods=10', '--interest=10', ],
        [script_name, '--type=diff', '--principal=1000000', '--periods=10', '--interest=10', ],
        # [script_name, '--type=annuity', '--principal=1000000', '--periods=60', '--interest=10', ],
        # [script_name, '--type=diff', '--principal=500000', '--periods=8', '--interest=7.8', ],
        # [script_name, '--type=annuity', '--payment=8722', '--periods=120', '--interest=5.6', ],
        # [script_name, '--type=annuity', '--principal=500000', '--payment=23000', '--interest=7.8', ],
        # # ] incorrect_args = [
        # [script_name, '--incorrect_args', ],
        # [script_name, '--principal=1000000', '--periods=60', '--interest=10', ],
        # [script_name, '--type=diff', '--principal=1000000', '--interest=10', '--payment=100000', ],
        # [script_name, '--type=annuity', '--principal=100000', '--payment=10400', '--periods=8', ],
        # [script_name, '--type=annuity', '--principal=1000000', '--payment=104000', ],
        # [script_name, '--type=diff', '--principal=30000', '--periods=-14', '--interest=10', ],
    ]
    return test_args


# test_parse_params()
test_run_params()

# process_params(sys.argv)
