from django import template


register = template.Library()

bad_words = [
    'Human',
]

text = "new1.title"

@register.filter()
def censor(text):
    list = text.split()
    censor_list = []
    for word in list:
        if word in bad_words:
            censor_word = word[0] + "***"
            censor_list.append(word.replace(word, censor_word))
        else:
            censor_list.append(word)

    return censor_list
