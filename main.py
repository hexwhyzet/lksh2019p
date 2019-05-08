import bz2
import time
import re
import collections


def count_links(file_path):
    regex = re.compile(r"\[\[[^(\])]*\]\]")
    """
        Регулярное выражение для поиска обычных ссылок (без вложенных ссылок)
        на страницы википедии:
        [[Литва|Самая лучшая страна...]] Примерно так выгледят ссылки, построены так:
        [[Название страницы на которе ведёт ссылка|Поле для информатции...|Еще поле|...|Текст ссылки]]
        Все поля, кроме первого, не обязаительны.
    """

    double_regex = re.compile(r"(\[\[[^(\])]*(\[\[[^(\])]*\]\])+[^(\])]*\]\])")
    """
        Регулярное выражение для поиска сложных ссылок(со вложенными ссылками)
        на страницы википедии
        Ищет ссылки (почти всегда на страницы с файлами), которые имеют ссылки в своих полях c информацией.
        Они нее обрабатываются первой регуляркой, поэтому нужна дополнительная.
        
    """

    name_extractor_regex = re.compile(r"^\[\[[^(\]\|)]*")
    """
        Извлекает из тела ссылки название статьи, на которое она ведет (это всегда первое поле ссылки).
        
    """

    counter_dict = collections.defaultdict(int)
    """
        Счетчик статей, на которые ведут ссылки.
    """

    with bz2.BZ2File(filename=file_path, mode="r") as source:
        for line in source:
            for matches in re.findall(regex, str(line, "utf-8")):
                counter_dict[re.match(name_extractor_regex, matches).group(0)[2:]] += 1
            for matches in re.findall(double_regex, str(line, "utf-8")):
                counter_dict[re.match(name_extractor_regex, matches[0]).group(0)[2:]] += 1
    return counter_dict


if __name__ == '__main__':
    file_path = input("Введите путь к .bz2 архиву с дампом википедии\n")
    time_start = time.time()
    ans = count_links(file_path)
    time_end = time.time()
    delta = time_end - time_start
    article_names = sorted(filter(lambda x: 2500 <= int(x[1]) <= 5000, ans.items()), key=lambda x: int(x[1]),
                           reverse=True)
    max_width = len(max(article_names, key=lambda x: len(x[0]))[0])
    print("".join(map(lambda x: f"{x[0].ljust(max_width + 2)} {x[1]}\n", article_names)))
    print("%.0f" % (delta // 60), "m", "%.2f" % (delta % 60), "s")
