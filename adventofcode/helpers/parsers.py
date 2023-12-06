import parsy


NUMBER = parsy.decimal_digit.at_least(1).concat().map(int)
NUMBER_LIST = NUMBER.skip(parsy.whitespace.many()).at_least(1)
