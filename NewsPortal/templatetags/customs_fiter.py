from django import template

register = template.Library()

@register.filter()
def censor(value, filter_word = ''):
    if type(value) == str:
        list_words = value.split()
        res_str = ''

        for word in list_words:
            if word.lower() == filter_word.lower():
                new_word = word[:1]
                for _ in range(len(word)):
                    new_word += '.'

                res_str += new_word if res_str == '' else ' ' + new_word
            else:
                res_str += word if res_str == '' else ' ' + word

        return res_str
    else:
        raise TypeError('Фильтр предназначен только для строкового типа')