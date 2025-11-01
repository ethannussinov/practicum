# Data Acquisition and Cleaning

1. All data was obtained from Project Gutenberg, open source and publicly available.

All books were downloaded in plain text UTF-8 to ensure consistency. Books were downloaded in the format XY_foo_bar, with XY representing the initials of the author, and _foo_bar representing the full name of the book (all lowercase, spaces replaced by '_')

The list of raw book files is structured as below:

|--data/
    |--raw/
        |--Aldous Huxley
            |--AH_antic_hay.txt
            |--AH_crome_yellow.txt
            |--AH_limbo.txt
            |--AH_mortal_coils.txt
            |--AH_those_barren_leaves.txt
        |--D.H. Lawrence
            |--DL_lady_chatterleys_lover.txt
            |--DL_sea_and_sardinia.txt
            |--DL_sons_and_lovers.txt
            |--DL_the_rainbow.txt
            |--DL_women_in_love.txt
        |--E.M. Forster
            |--EF_a_passage_to_india.txt
            |--EF_a_room_with_a_view.txt
            |--EF_howards_end.txt
            |--EF_the_longest_journey.txt
            |--EF_women_in_love.txt
        |--George Orwell
            |--GO_animal_farm.txt
            |--GO_burmese_days.txt
            |--GO_coming_up_for_air.txt
            |--GO_down_and_out_in_paris_and_london.txt
            |--GO_nineteen_eighty_four.txt
        |--Virginia Woolf
            |--VW_jacobs_room.txt
            |--VW_monday_or_tuesday.txt
            |--VW_mrs_dalloway.txt
            |--VW_night_and_day.txt
            |--VW_the_voyage_out.txt

