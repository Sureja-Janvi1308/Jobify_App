def words_to_number(num1):
    '''
    Function converts word to number as string format.
    param num1: taken string as parameter.
    return: return the converted string from word to number.
    '''
    if 'zero' in num1:
        num1 = num1.replace("zero", "0")
    if 'one' in num1:
        num1 = num1.replace('one', '1')
    if 'two' in num1:
        num1 = num1.replace('two', '2')
    if 'three' in num1:
        num1 = num1.replace('three', '3')
    if 'four' in num1:
        num1 = num1.replace('four', '4')
    if 'five' in num1:
        num1 = num1.replace('five', '5')
    if 'six' in num1:
        num1 = num1.replace('six', '6')
    if 'seven' in num1:
        num1 = num1.replace('seven', '7')
    if 'eight' in num1:
        num1 = num1.replace('eight', '8')
    if 'nine' in num1:
        num1 = num1.replace('nine', '9')
    if num1.isalpha():
        raise ValueError("Input should be between 0 to 9 ")
    return num1


def number_to_word(num1):
    '''
    Function converts number to word as string format.
    param num1: taken string as parameter which have numbers in string format.
    return: return the converted string from number to word.
    '''
    if '0' in num1:
        num1 = num1.replace("0", "zero")
    if '1' in num1:
        num1 = num1.replace('1', 'one')
    if '2' in num1:
        num1 = num1.replace('2', 'two')
    if '3' in num1:
        num1 = num1.replace('3', 'three')
    if '4' in num1:
        num1 = num1.replace('4', 'four')
    if '5' in num1:
        num1 = num1.replace('5', 'five')
    if '6' in num1:
        num1 = num1.replace('6', 'six')
    if '7' in num1:
        num1 = num1.replace('7', 'seven')
    if '8' in num1:
        num1 = num1.replace('8', 'eight')
    if '9' in num1:
        num1 = num1.replace('9', 'nine')
    return num1


def gcd(a: int, b: int):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


if __name__ == "__main__":
    try:
        user_input1 = input("Enter number one: ")
        if user_input1.isnumeric():
            raise ValueError("Enter Input in Words Format")

        num_word1 = words_to_number(user_input1)

        user_input2 = input("Enter number two: ")
        if user_input2.isnumeric():
            raise ValueError("Enter Input in Words Format")
        num_word2 = words_to_number(user_input2)

        result = gcd(int(num_word1), int(num_word2))
        result = number_to_word(str(result))

        print(f"The GCD of {user_input1} and {user_input2} is {result}")
    except Exception as e:
        print("Invalid Input:",e)
