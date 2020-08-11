from rune import Rune


def main():
    r = Rune()
    r.get_champion()
    r.parse_page()
    r.get_images()
    r.print_runes_on_desktop()


if __name__ == '__main__':
    main()
