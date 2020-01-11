get_similar(keyword):
    similar = model.similar_by_word(keyword)
    for word in similar:
        if count < 10:
            for line in quran:
                if word in line:
                    count++
                    print line
                    get_similar(word)
                    get_translation(word)

get_translation(keyword):
    for line in qruan:
        if keyword in line:
            print line

keyword = input() 
get_similar(keyword)
get_translation(keyword)