MY_PHRASE = 'text {key_to_insert} text'
def fun():
    data = 1
    use_phrase(MY_PHRASE.format(key_to_insert=data))

fun()