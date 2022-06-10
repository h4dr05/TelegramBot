def returnJson(lst):
    string = ''

    if not lst:
        string = "No matches :(" # none
    elif len(lst) == 1:
        string += f"{list[0].title}\n{list[0].description}" # list[0].title +'\n'+ list[0].description
    else:
        for book in lst:
            string += f"{book.title}\n" # i.title +'\n'
    print(string)
    return string

    