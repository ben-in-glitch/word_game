from settings.chapters import intro, all_chapters,chapters_transform,hidden_chapter_wind_city
from settings.characters import load_game

def main():
    player = intro()
    load_game(player)
    undone_chapters = []
    for chapter in all_chapters:
        if chapters_transform[chapter] not in player.finished_chapters:
            undone_chapters.append(chapter)
    for chapter in undone_chapters:
        input(f'press enter to continue...\n')
        chapter(player)
        if player.hp <= 0:
            print('game over')
            break
        player.finished_chapters.append(chapters_transform[chapter])
        hidden_chapter_wind_city(player)

    print('Thank you for playing')


if __name__ == "__main__":
    main()