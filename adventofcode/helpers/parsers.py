import parsy


NEWLINE = parsy.string('\n')
NEWLINES = NEWLINE.at_least(1)

SPACE = parsy.string(' ')
SPACES = SPACE.at_least(1)

DIGIT = parsy.decimal_digit.map(int)

NUMBER = parsy.regex(r'-?\d+').map(int)
NUMBER_LIST = NUMBER.sep_by(SPACES)
