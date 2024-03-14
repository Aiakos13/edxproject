#include <cs50.h>
#include <stdio.h>
#include <math.h>

int get_digit(long num, int idx);
int get_int_len(long num);

// Ask for credit card number
// Find every other digit starting with the second to last digit
// Multiply each by 2
// Add all of the digits together

int main(void)
{
    const long credit_num = get_long("Number: ");

    // digit stores the current digit of the credit card number
    int digit;

    // final stores the sum of the all the digits multiplied by two
    int final = 0;

    // Loops over every second digit, starting with the second to last one
    for (int i = 1; (digit = get_digit(credit_num, i)) != -1; i += 2)
    {
        // Multiplies the current digit by 2
        digit *= 2;
        // Adds every digit of the digit to the final sum
        for (int j = 0; get_digit(digit, j) != -1; j++)
        {
            final += get_digit(digit, j);
        }
    }

    // Loops over every second digit, starting with the last one
    // and adds that digit to the final sum
    for (int i = 0; (digit = get_digit(credit_num, i)) != -1; i += 2)
    {
        final += digit;
    }

    const int credit_len = get_int_len(credit_num);
    const int first_num = get_digit(credit_num, credit_len - 1);
    const int second_num = get_digit(credit_num, credit_len - 2);
    if (get_digit(final, 0) == 0)
    {
        if (first_num == 4 && (credit_len == 13 || credit_len == 16))
        {
            printf("VISA\n");
        }
        else if (credit_len == 15 && first_num == 3 && (second_num == 4 || second_num == 7))
        {
            printf("AMEX\n");
        }
        else if (credit_len == 16 && first_num == 5 && second_num >= 1 && second_num <= 5)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

int get_digit(long num, int idx)
{
    const long power = pow(10, idx + 1);
    return power / 10 > num ? -1 : (num % power) / (power / 10);
}

int get_int_len(long num)
{
    int len;
    for (len = 0; pow(10, len) < num; len++)
        ;
    return len;
}
